import numpy as np 

# Just used for plotting, not part of the machine learning.
def imgBufferFromVectors(xData, yData, zData=1, nx=640, ny=480, extent=[],
                         calc_average=True):
    # Create an image buffer of size (nx,ny) from the value of zData at the
    # coordinates (xData,yData)
    #
    # Optional:
    #    extent is the [x1,x2,y1,y2] axis extent of the plot.
    #    calc_average == True means calculate the average at each pixel
    #    calc_average == False means normalise the value at each pixel to between +/- 1
    
    # Remove nans from the data
    xData = np.where(np.isnan(xData), 0, xData)
    yData = np.where(np.isnan(yData), 0, yData)
    
    # Get the extent of data
    if len(extent)==4:  # Extent specified
        xMin = extent[0]
        xMax = extent[1]
        yMin = extent[2]
        yMax = extent[3]
    else:  # Extent not specified
        xMin = np.min(xData)
        xMax = np.max(xData)
        yMin = np.min(yData)
        yMax = np.max(yData)
        if len(extent)!=0:  # Extent incorrectly specified
            print('Warning in imgBufferFromVectors: extent incorrectly specified.')
        
    # Convert the xData into x indices
    width = xMax - xMin
    xLoc = np.round( (nx-1) * (xData - xMin) / width )
    # Convert to integers
    xLoc = xLoc.astype(dtype=np.int32)

    # Convert the y data into y indices
    width = yMax - yMin
    yLoc = np.round( (ny-1) * (yData - yMin) / width )
    # Convert to integers
    yLoc = yLoc.astype(dtype=np.int32)
    
    if len(extent)==4:  # Extent specified
        # Crop extreems
        xLoc = (xLoc >= nx)*(nx-1) + (xLoc < nx)*xLoc
        yLoc = (yLoc >= ny)*(ny-1) + (yLoc < ny)*yLoc
    
    # Create the image buffer (Note transpose)
    buffer = np.zeros((ny,nx),dtype=np.float32)
    
    # Add the zData to each specified (xLoc,yLoc) coordinate (Note transpose)
    np.add.at(buffer,(yLoc,xLoc),zData)
    
    # Create an averaging buffer (Note transpose)
    count = np.zeros((ny,nx),dtype=int)

    # Add 1 to to each specified (xLoc,yLoc) coordinate
    np.add.at(count,(yLoc,xLoc),1)
    
    if calc_average:
        # Calculate the average at each coordinate
        n = np.where(count==0, 1, count)
        buffer /= n
    else:
        # Limit the buffer to have a maximum of +/- 1
        buffer /= np.max(np.abs(buffer))
    
    # Return the extent for plotting
    extent = [xMin, xMax, yMin, yMax]
    
    return buffer, extent, count
