"""Gridded-data base definitions."""
import os
from copy import deepcopy
from abc import ABC, abstractmethod
import logging
import numpy as np
import xarray as xr
from .data_source import DataSourceLoaderBase

#: Logger.
log = logging.getLogger(__name__)


class GriddedDataSourceBase(DataSourceLoaderBase, ABC):
    """Gridded data-source abstract base class. Requires :py:meth:`get_grid`
    method to be implemented."""

    def __init__(self, med, name, cfg=None, **kwargs):
        """Build setting gridded to `True`.

        :param med: Mediator.
        :param name: Data source name. Default is `None`.
        :param cfg: Data source configuration. Default is `None`.
        :type med: :py:class:`.mediator.Mediator`
        :type name: str
        :type cfg: dict
        """
        super(GriddedDataSourceBase, self).__init__(
            med, name, cfg=cfg, **kwargs)

        # This is a gridded data set, convenience access to geo source
        self.gridded = True

        # Add get mask task
        self.task_mng['get_mask'] = True

        # Add dimensions name
        self.dims = (self.cfg['dims'] if 'dims' in self.cfg
                     else ['lat', 'lon'])

        # Initialize data members
        self.mask = None
        self.points_in_area = None

    @abstractmethod
    def get_grid(self, *args, **kwargs):
        """Return data source grid."""
        raise NotImplementedError

    def get_mask(self, **kwargs):
        """Get mask from :py:attr:`geo_src` for the given gridded data source
        and store it in :py:attr:`mask` data source member.
        """
        # Make sure that geo data is loaded
        self.med.geo_src.get_data(**kwargs)

        # Get the mask
        if self.task_mng.get('get_mask'):
            # Make the mask
            if not self.cfg.get('no_verbose'):
                log.info('Making {} mask for {}'.format(
                    self.med.geo_src.name, self.name))
            kwargs_new = deepcopy(kwargs)
            kwargs_new['data_src'] = self
            self.mask = self.med.geo_src.make_mask(**kwargs_new)

            # Save the mask
            self.write_mask(**kwargs_new)

            # Update task manager
            self.task_mng['get_mask'] = False
        else:
            # Read mask
            if not self.cfg.get('no_verbose'):
                log.info('{} mask for {} already made'.format(
                    self.med.geo_src.name, self.name))
            self.read_mask(**kwargs)

    def get_grid_postfix(self, **kwargs):
        """Return empty grid postfix string.

        returns: Grid postfix.
        rtype: str
        """
        return ''

    def get_mask_postfix(self, **kwargs):
        """Get mask postfix for data source.

        :returns: Postfix
        :rtype: str
        """
        grid_postfix = self.get_grid_postfix(**kwargs)
        geo_postfix = self.med.geo_src.get_data_postfix(**kwargs)
        zone_str = ('_zone' if self.med.geo_cfg['zones_from_regions']
                    else '')
        postfix = '_{}{}_{}{}_{}{}'.format(
            self.med.cfg['area'], zone_str, self.med.geo_src.name, geo_postfix,
            self.name, grid_postfix)

        return postfix

    def get_mask_path(self, makedirs=True, **kwargs):
        """Get mask file path for data source.

        :param makedirs: Make directories if needed. Default is `True`.
        :type makedirs: bool

        :returns: Filepath.
        :rtype: str
        """
        file_dir = self.med.cfg.get_project_data_directory(
            self, makedirs=makedirs, **kwargs)
        filename = 'mask{}'.format(self.get_mask_postfix(**kwargs))
        filepath = os.path.join(file_dir, filename)

        return filepath

    def read_mask(self, **kwargs):
        """Default implementation: read mask dataset as
        :py:class:`xarray.Dataset`.
        """
        filepath = '{}.nc'.format(self.get_mask_path(makedirs=False, **kwargs))
        if not self.cfg.get('no_verbose'):
            log.info('Reading {} mask for {} from {}'.format(
                self.med.geo_src.name, self.name, filepath))
        with xr.open_dataset(filepath) as ds:
            self.mask = ds.copy(deep=True)

    def write_mask(self, **kwargs):
        """Default implementation: write mask as
        :py:class:`xarray.Dataset` to netcdf.
        """
        filepath = '{}.nc'.format(self.get_mask_path(**kwargs))
        if not self.cfg.get('no_verbose'):
            log.info('Writing {} mask for {} to {}'.format(
                self.med.geo_src.name, self.name, filepath))
        self.mask.to_netcdf(filepath)

    def get_regional_mean(self, ds, **kwargs):
        """Average dataset over regions given by mask.

        :param ds: Dataset to average.
        :type ds: :py:class:`xarray.Dataset`

        :returns: Dataset containing regional means.
        :rtype: :py:class:`xarray.Dataset`
        """
        if not self.cfg.get('no_verbose'):
            log.info('Getting regional averages on {} grid'.format(
                self.name))

        # Get regional mean
        gp = ds.groupby(self.mask['mask'])

        # Group dimensions may either original or stacked ones
        try:
            res = gp.mean(list(self.mask['mask'].dims), keep_attrs=True)
        except ValueError:
            res = gp.mean(gp._stacked_dim, keep_attrs=True)

        # Remove unnecessary regions out of non-empty ones
        # and replace coordinates
        (filled_indices, idx1, idx2) = np.intersect1d(
            self.mask['region_index'].values, list(gp.groups),
            return_indices=True)
        res = res.loc[{'mask': filled_indices}]
        res = res.rename(mask='region')
        res['region'] = self.mask['region'].values[idx1]

        # Transpose region and time dimensions,
        # keeping other dimensions behind
        dim_list = list(res.dims)
        dim_list.remove('region')
        dim_list.insert(0, 'region')
        dim_list.remove('time')
        dim_list.insert(0, 'time')
        res = res.transpose(*dim_list)

        return res

    def get_total_mean(self, ds, **kwargs):
        """Average dataset over all grid points,
        independently of mask.

        :param ds: Dataset to average.
        :type ds: :py:class:`xarray.Dataset`

        :returns: Dataset containing mean.
        :rtype: :py:class:`xarray.Dataset`
        """
        if not self.cfg.get('no_verbose'):
            log.info('Getting {} total mean'.format(self.name))

        # Group dimensions may either original or stacked ones
        try:
            res = ds.mean(self.dims, keep_attrs=True)
        except ValueError:
            res = ds.mean(ds._stacked_dim, keep_attrs=True)

        return res

    def crop_area(self, ds, **kwargs):
        """Crop :py:obj:`ds` for data source
        over area covered by mask regions.

        :param ds: Dataset to crop.
        :type ds: :py:class:`xarray.Dataset`

        :returns: Cropped dataset.
        :rtype: :py:class:`xarray.Dataset`

        .. note:: If :py:attr:`points_in_area` is not `None`,
          use it to mask points inside area covered by regions.
        """
        if not self.cfg.get('no_verbose'):
            log.info('Cropping area for {}'.format(self.name))

        if self.points_in_area is None:
            # Get points in area
            is_in = xr.zeros_like(self.mask['mask'], dtype=bool)
            for reg_idx in self.mask.region_index.astype(float).values:
                is_in |= (self.mask['mask'] == reg_idx)

            # Add points in area mask to regional mask dataset
            self.points_in_area = is_in

        # Select region, removing other points
        is_in_stack = self.points_in_area.stack(stacked_dim=self.dims)
        res = ds.stack(stacked_dim=self.dims)[
            {'stacked_dim': is_in_stack.values}]

        if 'stacked_dim' not in self.mask:
            # Store stacked mask
            self.mask = self.mask.stack(stacked_dim=self.dims)[
                {'stacked_dim': is_in_stack}]

        return res

    # def crop_within_bounds(self, ds, **kwargs):
    #     """Crop :py:obj:`data` dataset for the data source within total
    #     bounds of regions (requires geo data but not data source mask).

    #     :param ds: Dataset to crop.
    #     :type ds: :py:class:`xarray.Dataset`

    #     :returns: Cropped dataset.
    #     :rtype: :py:class:`xarray.Dataset`
    #     """
    #     log.info('Cropping within bounds for {}'.format(self.name))

    #     # Get total bounds
    #     lon_min, lat_min, lon_max, lat_max \
    #         = self.med.geo_src.get_total_bounds(epsg=4326)

    #     # Get points within bounds
    #     any_var = list(list(self.cfg[
    #         'variable_names'].values())[0].values())[0]
    #     is_in = xr.zeros_like(self.ds[any_var], dtype=bool)
    #     for i,
    #         is_in |= (self.mask['mask'] == reg_idx)

    #         # Add points in area mask to regional mask dataset
    #         self.points_in_area = is_in

    #     # Select region, removing other points
    #     is_in_stack = self.points_in_area.stack(stacked_dim=self.dims)
    #     res = ds.stack(stacked_dim=self.dims)[
    #         {'stacked_dim': is_in_stack.values}]

    #     if 'stacked_dim' not in self.mask:
    #         # Store stacked mask
    #         self.mask = self.mask.stack(stacked_dim=self.dims)[
    #             {'stacked_dim': is_in_stack}]

    #     return res
