import gdal
import sys
import logging 
from time import sleep
from pystac import Item

logging.basicConfig(stream=sys.stderr, 
                    level=logging.DEBUG,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%dT%H:%M:%S')

def rescale(in_tif, out_tif):
    
    scaling_factor = 10000
    
    ds = gdal.Open(in_tif)
    
    width = ds.RasterXSize
    height = ds.RasterYSize

    input_geotransform = ds.GetGeoTransform()
    input_georef = ds.GetProjectionRef()
    
    in_band = ds.GetRasterBand(1)
    
    in_arr = in_band.ReadAsArray()
    
    driver = gdal.GetDriverByName('GTiff')

    output = driver.Create(out_tif, 
                           width, 
                           height, 
                           1, 
                           gdal.GDT_Int16)

    output.SetGeoTransform(input_geotransform)
    output.SetProjection(input_georef)

    logging.info('Converting band to Int16')

    band = output.GetRasterBand(1)

    band.WriteArray((in_arr * scaling_factor).astype(np.intc))

    output.FlushCache()

    band = None

    output = None

    sleep(5)
    
    del(ds)
    del(output)
    
    in_band = None
    ds = None
    del(ds)
    
    return True

def stac_ify(item, in_tiff):

    out_item = Item(id=item.id,
                    geometry=item.geometry,
                    bbox=item.bbox,
                    datetime=item.datetime,
                    properties=item.properties)
