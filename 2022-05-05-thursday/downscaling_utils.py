import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import cartopy
import cartopy.crs as ccrs

# for querying dictionary
def provide_default(dict_in, keyname, default=None, required=False):
    """
    Returns values of key from input dictionary or alternatively its default

    :param dict_in: input dictionary
    :param keyname: name of key which should be added to dict_in if it is not already existing
    :param default: default value of key (returned if keyname is not present in dict_in)
    :param required: Forces existence of keyname in dict_in (otherwise, an error is returned)
    :return: value of requested key or its default retrieved from dict_in
    """

    if not required and default is None:
        raise ValueError("Provide default when existence of key in dictionary is not required.")
        
    if keyname not in dict_in.keys():
        if required:
            print(dict_in)
            raise ValueError("Could not find '{0}' in input dictionary.".format(keyname))
        return default
    else:
        return dict_in[keyname]

# auxiliary function for colormap
def get_colormap_temp(levels = None):
    """
    Get a nice colormap for plotting topographic height
    :param levels: level boundaries
    :return cmap: colormap-object
    :return norm: normalization object corresponding to colormap and levels
    """
    bounds = np.asarray(levels)
        
    nbounds = len(bounds)
    col_obj = mpl.cm.PuOr_r(np.linspace(0., 1., nbounds))
    
    # create colormap and corresponding norm
    cmap = mpl.colors.ListedColormap(col_obj, name="temp" + "_map")
    norm = mpl.colors.BoundaryNorm(bounds, cmap.N)    
    
    return cmap, norm, bounds

# for making plot nice
def decorate_plot(ax_plot, plot_xlabel=True, plot_ylabel=True):
        
    fs = 16
    # add nice features and make plot appear nice
    ax_plot.coastlines(linewidth=0.75)
    ax_plot.coastlines(linewidth=0.75)

    ax_plot.add_feature(cartopy.feature.BORDERS)
    # adjust extent and ticks as well as axis-label
    ax_plot.set_xticks(np.arange(0., 360. + 0.1, 5.))  # ,crs=projection_crs)
    ax_plot.set_yticks(np.arange(-90., 90. + 0.1, 5.))  # ,crs=projection_crs)

    ax_plot.set_extent([3.5, 17., 44.5, 55.])#, crs=prj_crs)
    ax_plot.minorticks_on()
    ax_plot.tick_params(axis="both", which="both", direction="out", labelsize=12)

    # some labels
    if plot_xlabel:
        ax_plot.set_xlabel("Longitude [°E]", fontsize=fs)
    if plot_ylabel:
        ax_plot.set_ylabel("Latitude[°N]", fontsize=fs)
    
    return ax_plot

# for creating plot
def create_plots(data1, data2, opt_plot={}):
    
    # get coordinate data 
    try:
        time, lat, lon = data1["time"].values, data1["lat"].values, data1["lon"].values
        time_stamp = (pd.to_datetime(time)).strftime("%Y-%m-%d %H:00 UTC")
    except Exception as err:
        print("Failed to retrieve coordinates from data1")
        raise err
    # construct array for edges of grid points
    dy, dx = np.round((lat[1] - lat[0]), 2), np.round((lon[1] - lon[0]), 2)
    lat_e, lon_e = np.arange(lat[0]-dy/2, lat[-1]+dy, dy), np.arange(lon[0]-dx/2, lon[-1]+dx, dx)
    
    title1, title2 = provide_default(opt_plot, "title1", "input T2m"), provide_default(opt_plot, "title2", "target T2m")
    title1, title2 = "{0}, {1}".format(title1, time_stamp), "{0}, {1}".format(title2, time_stamp)
    levels = provide_default(opt_plot, "levels", np.arange(-5., 25., 1.))
    
    # get colormap
    cmap_temp, norm_temp, lvl = get_colormap_temp(levels)
    # create plot objects
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12,8), sharex=True, sharey=True, subplot_kw={"projection": ccrs.PlateCarree()})
    
    # perform plotting
    temp1 = ax1.pcolormesh(lon_e, lat_e, np.squeeze(data1.values-273.15), cmap=cmap_temp, norm=norm_temp)
    temp2 = ax2.pcolormesh(lon_e, lat_e, np.squeeze(data2.values-273.15), cmap=cmap_temp, norm=norm_temp)

    ax1, ax2 = decorate_plot(ax1), decorate_plot(ax2, plot_ylabel=False) 

    ax1.set_title(title1, size=14)
    ax2.set_title(title2, size=14)

    # add colorbar
    cax = fig.add_axes([0.92, 0.3, 0.02, 0.4])
    cbar = fig.colorbar(temp2, cax=cax, orientation="vertical", ticks=lvl[1::2])
    cbar.ax.tick_params(labelsize=12)

