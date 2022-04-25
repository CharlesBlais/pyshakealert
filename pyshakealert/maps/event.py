'''
..  codeauthor:: Charles Blais
'''
import logging

from typing import Optional, Union

import numpy as np

import cartopy.io.img_tiles as cimgt

import cartopy.crs as ccrs

import matplotlib.pyplot as plt

from pyshakealert.message.event.event import Event

from pyshakealert.message.event.gmcontour import GroundMotionContourPrediction

from pyshakealert.message.event.gmmap import GroundMotionMapPrediction

from pyshakealert.config import get_app_settings

import io


def _mmi_to_color(mmi: float) -> str:
    '''
    Convert mmi to color
    '''
    settings = get_app_settings()

    index = round(mmi)
    if index >= len(settings.mmi_colors):
        return settings.mmi_colors[-1]
    return settings.mmi_colors[index]


def _add_ground_motion(
    ax: plt.Axes,
    gm: Union[GroundMotionContourPrediction, GroundMotionMapPrediction],
):
    '''
    Add ground motion to image
    '''
    data_crs = ccrs.PlateCarree()

    df = gm.to_dataframe()

    # add column with MMI colors
    df['color'] = df.apply(lambda row: _mmi_to_color(row['MMI']), axis=1)

    if isinstance(gm, GroundMotionMapPrediction):
        for _, row in df.iterrows():
            plt.plot(
                row['geometry'].x, row['geometry'].y,
                transform=data_crs,
                color='black',
                marker='o',
                markersize=5)
            plt.plot(
                row['geometry'].x, row['geometry'].y,
                transform=data_crs,
                color=row['color'],
                marker='o',
                markersize=4)
    else:
        ax.add_geometries(
            df['geometry'],
            crs=data_crs,
            facecolor="none",
            linewidth=4,
            edgecolor='black')

        ax.add_geometries(
            df['geometry'],
            crs=data_crs,
            facecolor="none",
            linewidth=3,
            edgecolor=df['color'].to_list())


def generate(
    event: Event,
    dlat: float = 1,
    dlon: float = 2,
    zoom: int = 8,
    to_filename: Optional[str] = None,
) -> bytes:
    '''
    Generate map image from event object
    '''
    data_crs = ccrs.PlateCarree()

    # extract essential informaiton
    lat = event.core_info.lat.value
    lon = event.core_info.lon.value
    orig_time = event.core_info.orig_time.value
    mag = event.core_info.mag.value
    units = event.core_info.mag.units

    imagery = cimgt.OSM()

    logging.debug(f'imagery CRS: {imagery.crs}')
    ax = plt.axes(projection=imagery.crs, label=str(np.random.random()))

    ax.set_title(f'{mag} {units} - {orig_time} - {event.orig_sys}')

    # bounds
    minlat = lat - dlat
    maxlat = lat + dlat
    minlon = lon - dlon
    maxlon = lon + dlon

    logging.debug(f'Setting bounds: {minlon}, {maxlon}, {minlat}, {maxlat}')
    ax.set_extent([minlon, maxlon, minlat, maxlat])

    ax.add_image(imagery, zoom)
    ax.gridlines(draw_labels=True)

    plt.plot(
        lon, lat,
        transform=data_crs,
        color='black', marker='*', markersize=15)
    plt.plot(
        lon, lat,
        transform=data_crs,
        color='red', marker='*', markersize=10)

    # Add contour if defined
    if event.gm_info and event.gm_info.gmcontour_pred:
        _add_ground_motion(ax, event.gm_info.gmcontour_pred)

    if event.gm_info and event.gm_info.gmmap_pred:
        _add_ground_motion(ax, event.gm_info.gmmap_pred)

    if to_filename:
        plt.savefig(to_filename)

    fp = io.BytesIO()
    plt.savefig(fp)
    return fp.getvalue()
