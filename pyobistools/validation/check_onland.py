# Problems with importing the obisqc solution, use pyxylookup directly.
import pyxylookup as xy
import warnings
import geopandas as gpd
import pandas as pd

# alternate idea for shapefiles from Bio Mobilization workshop module 6 example
import cartopy.io.shapereader as shpreader
from shapely.ops import unary_union
from shapely.prepared import prep


def check_onland(data, land=None, report=False, buffer=0, offline=False):
    """
    Check which points are likely to be located on land

    @param data         a Pandas dataframe with the data
    @param land         A custom land polygon to check against. If not provided, use Natural Earth.
    @param report       If True, errors returned instead of records
    @param buffer       Set how far inland points are still to be deemed valid
    @param offline      if True, a local simplified shoreline is used, otherwise an OBIS webservice is used. Default is False

    @return Errors or problematic records
    """

    # Catch any troubles with the lat/lon data itself first
    # errors = check_lonlat(data, report)
    errors = []
    if len(errors) > 0 and report:
        return errors

    # Make a geopandas GeoSeries of the now confirmed not-bad data.
    gdf = gpd.GeoDataFrame(
        data, geometry=gpd.points_from_xy(data.decimalLongitude, data.decimalLatitude)
    )

    if land is not None and (not offline):
        warnings.warn("land parameter not supported when in offline mode")

    if buffer != 0 and offline:
        warnings.warn("buffer parameter not used when in online mode")

    # Offline with no specified land polygons - set up the default land polygon set
    if offline and land is None:
        land_shp_fname = shpreader.natural_earth(
            resolution="10m", category="physical", name="land"
        )
        land_geom = unary_union(list(shpreader.Reader(land_shp_fname).geometries()))
        land = prep(land_geom)

    # TODO: what if we have specified a land polygon?

    # Offline in all cases

    if offline:
        # spatial query to find overlaps between each lat/lon in my dataset and the land polygons
        # try using geopandas.GeoSeries.contains()
        for index, row in gdf.iterrows():
            gdf.loc[index, "on_land"] = land.contains(row.geometry)

    else:  # we're in online mode - use xylookup.lookup()
        shoredistance = xy.lookup(
            data[["decimalLongitude", "decimalLatitude"]].to_numpy(),
            shoredistance=True,
            grids=True,
            areas=True,
            asdataframe=True,
        )
        # gdf on_land needs to be a boolean series.
        # multiply by the buffer amount, defaults to zero so right side evals zero without a buffer value
        gdf["on_land"] = shoredistance["shoredistance"] < (-1 * buffer)
    # Are we returning a report or the offending data?
    if report:
        if len(gdf) > 0:
            return gdf[
                gdf["on_land"]
            ]
        else:   # the function returns an empty dataframe
            return pd.DataFrame(index=data.index, columns=data.columns)  # return empty dataframe in the same shape, as per the R implementation
    else:  # if we are not returning a report, return the offending rows themselves.
        return gdf[gdf["on_land"]]
