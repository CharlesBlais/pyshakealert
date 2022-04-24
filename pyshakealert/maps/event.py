'''
..  codeauthor:: Charles Blais
'''
from typing import Optional

from cartopy.io.img_tiles import OSM

import cartopy.crs as ccrs

import matplotlib.pyplot as plt

from pyshakealert.message.event.event import Event

from pyshakealert.message.event.gmcontour import GroundMotionContourPrediction

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


def _add_ground_motion_contour(
    ax: plt.Axes,
    gm: GroundMotionContourPrediction,
):
    '''
    Add ground motion to image
    '''
    data_crs = ccrs.PlateCarree()

    df = gm.to_dataframe()

    # add column with MMI colors
    df['color'] = df.apply(lambda row: _mmi_to_color(row['MMI']), axis=1)

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

    imagery = OSM()

    ax = plt.axes(projection=imagery.crs)

    ax.set_title(f'M{mag} {units} - {orig_time} - {event.orig_sys}')

    ax.set_extent([
        lon - dlon, lon + dlon,
        lat - dlat, lat + dlat])

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
        _add_ground_motion_contour(ax, event.gm_info.gmcontour_pred)

    if to_filename:
        plt.savefig(to_filename)

    fp = io.BytesIO()
    plt.savefig(fp)
    return fp.getvalue()
