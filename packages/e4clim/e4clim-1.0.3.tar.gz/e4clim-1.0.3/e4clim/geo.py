"""Geographic-data and mask base definitions."""
import os
from abc import ABC, abstractmethod
import logging
from pkg_resources import resource_stream
import requests
import zipfile
from io import BytesIO
from shapely.geometry import Point
from fiona.crs import from_epsg
import geopandas as gpd
import numpy as np
import pandas as pd
import xarray as xr
import oyaml as yaml
import difflib
from .data_source import DataSourceBase, DataSourceLoaderBase

#: Geographic-variable name.
GEO_VARIABLE = 'border'

#: Logger.
log = logging.getLogger(__name__)


class GeoDataSourceBase(DataSourceBase, ABC):
    """Geographic data-source abstract base class. Requires :py:meth:`make_mask`
    method to be implemented."""

    def __init__(self, med, name, cfg=None, variables=None, **kwargs):
        """Convenience constructor for default geographic data source."""
        variables = variables or [GEO_VARIABLE]
        super(GeoDataSourceBase, self).__init__(
            med, name, cfg=cfg, variables=variables, data_as_dict=True,
            **kwargs)

    @abstractmethod
    def make_mask(self, *args, **kwargs):
        """Make mask for a gridded data source."""
        raise NotImplementedError

    def get_total_bounds(self, epsg=4326, **kwargs):
        """Get array of min and max coordinates on each axis.

        :param epsg: EPSG code specifying output projection.
        :type epsg: int

        :returns: Array with min x, min y, max x, max y.
        :rtype: :py:class:`numpy.array`
        """
        # Ensure that geo data is loaded
        self.med.geo_src.get_data()

        # Get data in right CRS
        geo_data = self.med.geo_src.get(GEO_VARIABLE)
        data = geo_data.to_crs(epsg=epsg) if epsg else geo_data

        # Return total bounds
        return data.total_bounds


class DefaultMaskAPI(DataSourceLoaderBase, ABC):
    """Mask downloading mixin. Requires :py:meth:`get_url_filename` method
    to be implemented."""

    @abstractmethod
    def get_url_filename(self, *args, **kwargs):
        """Get URL and filename of geographical data."""
        raise NotImplementedError

    def download(self, **kwargs):
        """Download shapefile defining regions and
        store geographical data to :py:attr:`data` member.
        """
        # Get URL and file name
        url, sf_name = self.get_url_filename(**kwargs)

        file_dir = self.med.cfg.get_external_data_directory(self, **kwargs)
        src_dir = os.path.join(file_dir, self.med.cfg['area'])
        os.makedirs(src_dir, exist_ok=True)

        # Download
        log.info('Downloading shapefile from {}'.format(url))
        download_shapefile(url, sf_name, src_dir)

    def load(self, **kwargs):
        """Load geographical data.

        :returns: Geographical array with geometries.
        :rtype: :py:class:`geopandas.GeoDataFrame`
        """
        file_dir = self.med.cfg.get_external_data_directory(
            self, makedirs=False, **kwargs)
        src_dir = os.path.join(file_dir, self.med.cfg['area'])
        # Get URL and file name
        _, sf_name = self.get_url_filename(**kwargs)

        # Read geographical file
        sf_path = os.path.join(src_dir, sf_name)
        data = gpd.read_file(sf_path)

        # Handle parent/child columns
        if 'parent_column' in self.cfg:
            # Get country code
            country_code = get_country_code(
                self.med.cfg['area'], code='alpha-2')
            # Select country
            data = data[data.loc[:, self.cfg['parent_column']]
                        == country_code]

        self.update({GEO_VARIABLE: data})

        # Write regions centroid coordinates
        places, place_names, reg_zones = self.get_places(**kwargs)
        self.write_region_coordinates(place_names, reg_zones)

        return {GEO_VARIABLE: data}

    def read(self, **kwargs):
        """Read source dataset as :py:class:`geopandas.GeoDataFrame`
        from shapefile.
        """
        filepath = self.get_data_path(variable=GEO_VARIABLE, makedirs=False,
                                      is_timeseries=False, **kwargs)
        if not self.cfg.get('no_verbose'):
            log.info('Reading {} for {} from {}'.format(
                GEO_VARIABLE, self.name, filepath))
        self[GEO_VARIABLE] = gpd.read_file(filepath)

    def write(self, **kwargs):
        """Write source :py:class:`geopandas.GeoDataFrame` dataset to shapefile.
        """
        filepath = self.get_data_path(
            variable=GEO_VARIABLE, is_timeseries=False, **kwargs)
        if not self.cfg.get('no_verbose'):
            log.info('Writing {} for {} to {}'.format(
                GEO_VARIABLE, self.name, filepath))
        self.get(GEO_VARIABLE).to_file(filepath)


class DefaultMaskMaker(GeoDataSourceBase):
    """Default mask maker."""

    def make_mask(self, data_src, **kwargs):
        """Make mask for a given gridded data source, store the
        regions' geometries to :py:attr:`data` member.

        :param data_src: Gridded data source.
        :type data_src: :py:class:`.grid.GriddedDataSourceBase`

        :returns: Mask dataset.
        :rtype: :py:class:`xarrray.Dataset`
        """
        # Get regions' geometries
        self.get_data(**kwargs)

        # Get places
        places, place_names, reg_zones = self.get_places(**kwargs)

        # Download data to read the grid
        data_src.manage_download(**kwargs)

        # Get data coordinates
        coords = data_src.get_grid(**kwargs)

        # Get point region membership
        log.info('Assigning points to regions')
        ds_mask = get_point_region_membership(
            self.cfg, self.get(GEO_VARIABLE), places, reg_zones, coords)

        # Add mask name
        ds_mask.attrs['area'] = self.med.cfg['area']

        return ds_mask

    def get_places(self, **kwargs):
        """Get zone or region names, ids, mapping, etc."""
        place_names = self.get(GEO_VARIABLE).loc[
            :, self.cfg['child_column']].tolist()

        # Get region to bidding zone membership, if needed
        reg_zones, place_names = self.get_region_zone_membership(place_names)

        # Create dictionary of places (independent of data grid)
        place_ids = list(range(2, len(place_names) + 2))
        places = dict(zip(place_names, place_ids))

        return places, place_names, reg_zones

    def read_region_coordinates(self, **kwargs):
        """Read centroid coordinates of regions.

        :param place_names: Region or zone names.
        :param reg_zones: Region to zone mapping.
        :type place_names: list
        :tye reg_zones: dict

        :returns: Centroid coordinates of regions.
        :rtype: :py:class:`pandas.GeoDataFrame`
        """
        file_dir = self.med.cfg.get_project_data_directory(self, **kwargs)
        filename = 'latlon_{}{}.csv'.format(
            self.med.cfg['area'], self.get_data_postfix(
                with_src_name=True, **kwargs))
        filepath = os.path.join(file_dir, filename)
        with open(filepath, 'r') as f:
            df_coord_zones = pd.read_csv(f, index_col=0)

        return df_coord_zones

    def write_region_coordinates(self, place_names, reg_zones, **kwargs):
        """Write centroid coordinates of regions.

        :param place_names: Region or zone names.
        :param reg_zones: Region to zone mapping.
        :type place_names: list
        :tye reg_zones: dict
        """
        coord_zones = {place_names[k]: np.array([])
                       for k in range(len(place_names))}
        gdf = self.get(GEO_VARIABLE)
        for region, zone in reg_zones.items():
            pt0 = gdf[gdf[self.cfg['child_column']]
                      == region].geometry.centroid
            pt = gpd.GeoSeries(pt0, crs=gdf.crs).to_crs(
                from_epsg(4326)).values[0]
            coord_zones[zone] = np.concatenate(
                [coord_zones[zone], [pt.y, pt.x]])
        for zone, a in coord_zones.items():
            coord_zones[zone] = coord_zones[zone].reshape(-1, 2).mean(0)
        df_coord_zones = pd.DataFrame(coord_zones, index=['lat', 'lon']).T

        file_dir = self.med.cfg.get_project_data_directory(self, **kwargs)
        filename = 'latlon_{}{}.csv'.format(
            self.med.cfg['area'], self.get_data_postfix(
                with_src_name=True, **kwargs))
        filepath = os.path.join(file_dir, filename)
        df_coord_zones.to_csv(filepath)

    def get_region_zone_membership(self, place_names, **kwargs):
        """Assign regions to bidding zones, if needed.

        :param place_names: Names of electricity regions.
        :param place_names: list of str

        :returns: A tuple containing

            * a dictionary assigning a region to a zone,
            * a list of zone (or region) names.

        :rtype: tuple
        """
        if self.med.geo_cfg['zones_from_regions']:
            # Get zones
            zones_desc = self.get_zones(self.med.cfg['area'])
            zone_regs = {k: v['regions'] for k, v in zones_desc.items()}

            # Ensure that regional names from shapefile correspond to zones
            reg_zones = {}
            for z, lreg in zone_regs.items():
                for reg in lreg:
                    regSrc = difflib.get_close_matches(reg, place_names, n=1)
                    # Add region, if found
                    if len(regSrc) > 0:
                        reg_zones[regSrc[0]] = z

            # Update place_names
            place_names = list(zones_desc)
        else:
            # If not bidding zones are asked, just return identity
            reg_zones = dict(zip(place_names, place_names))

        return reg_zones, place_names

    def get_zones(self, area):
        """Get zones for area.

        :param area: Area name.
        :type area: str

        :returns: Zones list.
        :rtype: list
        """
        zones_filepath = self.med.geo_cfg.get('zones_filepath')
        if zones_filepath is not None:
            with open(zones_filepath, 'r') as f:
                zones = yaml.load(f, Loader=yaml.FullLoader)
        else:
            # Try to get zones from resource data.
            filename = 'zones_{}.yaml'.format(area)
            resource_name = 'data/{}/{}'.format(area, filename)
            with resource_stream(__name__, resource_name) as f:
                zones = yaml.load(f, Loader=yaml.FullLoader)

        return zones


def get_point_region_membership(cfg_src, gdf, places, reg_zones, coords):
    """Assign grid-points of dataset to electricity places.

    :param cfg_src: Data source configuration.
    :param gdf: Regions' geometries.
    :param places: Dictionary assigning each plae name to a place ID.
      IDs of places of interest should be larger or equal to 2.
    :param reg_zones: Dictionary assigning each region to a zone
    :param coords: Input data coordinates assigned to telectricity places.
    :type cfg_src: dict
    :type gdf: :py:class:`geopandas.GeoDataFrame`
    :type places: dict
    :type reg_zones: dict
    :type coords: :py:class:`tuple` of pairs of :py:class:`str`
      and :py:class:`numpy.array`

    :returns: Dataset containing mask assigning each grid-point to a place.
    :rtype: :py:class:`xarray.Dataset`
    """
    # Get dims and coords for regular and irregular grids
    try:
        dim_names = coords.dims
        dims = tuple(coords[dim].shape[0] for dim in dim_names)
    except AttributeError:
        dim_names = coords.keys()
        dims = tuple(len(v) for v in coords.values())

    # Create an empty mask
    ds = xr.Dataset()
    ds['mask'] = xr.DataArray(np.zeros(dims, dtype=int),
                              dims=dim_names, coords=coords)

    # Add region indices
    coords = ('region', list(places.keys()))
    ds['region_index'] = xr.DataArray(
        list(places.values()), coords=[coords])

    # Assign points to regions
    for iy in range(ds['mask'].shape[0]):
        for ix in range(ds['mask'].shape[1]):
            # Select point and convert to regions' CRS
            try:
                lat = float(ds.lat[iy, ix].values)
                lon = float(ds.lon[iy, ix].values)
            except IndexError:
                lat = float(ds.lat[iy].values)
                lon = float(ds.lon[ix].values)
            pt = gpd.GeoSeries(
                Point(lon, lat), crs=from_epsg(4326)).to_crs(gdf.crs)

            # Select region to which this point belongs to, if any
            within = gdf.contains(pt[0])
            if within.any():
                reg = gdf[within].loc[:, cfg_src['child_column']].values[0]

                # Get corresponding zone and save zone ID in mask
                # If region in no zone, set to 1
                reg = reg_zones.get(reg)
                ds['mask'][iy, ix] = places[reg] if reg else 1

    # Remove empty regions
    idx_filled = np.in1d(ds.region_index, np.unique(ds.mask))
    ds = ds.loc[{'region': idx_filled}]

    return ds


def download_shapefile(url, sf_name, src_dir):
    """Download shapefile defining electricity regions
    and return regions' geometries.

    :param url: URL from which to download data.
    :param sf_name: Name of shapefile to download.
    :param src_dir: Data destination directory.
    :type url: str
    :type sf_name: str
    :type src_dir: str

    .. note:: This function is not directly called from this module,
      but from API's included in this package(e.g. GISCO).
    """
    # Download shapefile for region
    sf_path = os.path.join(src_dir, sf_name)
    r = requests.get(url)
    if r.status_code != 200:
        raise FileNotFoundError(url)

    # Extract, if needed, or write file
    if url[-4:] == '.zip':
        zip_ref = zipfile.ZipFile(BytesIO(r.content))
        zip_ref.extractall(src_dir)
        zip_ref.close()
    else:
        with open(sf_path, 'wb') as f:
            for chunk in r:
                f.write(chunk)


def get_country_code(region, code='alpha-2'):
    """Get country code of region.

    :param region: Region name.
    :param code: Code name.
    :type region: str
    :type code: str

    :returns: Country code.
    :rtype: str
    """
    # Read country codes
    resource_name = 'data/iso_country_codes.csv'
    with resource_stream(__name__, resource_name) as stream:
        cc_data = pd.read_csv(stream, index_col=0)
    reg_name = difflib.get_close_matches(
        region, cc_data.index.tolist(), n=1)[0]

    return cc_data.loc[reg_name, code]
