import gdal
import sys
import logging 
from time import sleep
from pystac import Item
import numpy as np

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

def to_stac(item, in_tiff):

    item_out = Item(id=item.id,
                    geometry=item.geometry,
                    bbox=item.bbox,
                    datetime=item.datetime,
                    properties=item.properties)

    item_out.common_metadata.set_gsd(20)
    item_out.common_metadata.set_constellation('sentinel-1')
    item_out.common_metadata.set_mission('sentinel-1')
    item_out.common_metadata.set_platform('sentinel-1{}'.format(item.id[2:3].lower()))

    eo_item = extensions.eo.EOItemExt(item_out)

    band = 'sigma_db_vv '

    item_out.add_asset(key=band.lower(), 
                               asset=Asset(href='{}_{}.tif'.format(item.id, band.upper()), 
                                           media_type=MediaType.GEOTIFF,
                                           properties={'sar:polarizations': band.lower().split('_')[1].upper()})) 


    asset = eo_item.item.get_assets()[band.lower()]
            
    description = '{} for polarization channel {}{}'.format(band.lower().split('_')[0].title(), 
                                                                    band.lower().split('_')[1].upper(), 
                                                                    ' in {}'.format(band.lower().split('_')[2]) if len(band.lower().split('_')) == 3 else '')
            
    stac_band = extensions.eo.Band.create(name=band.lower(), 
                                                   common_name=band.lower(),
                                                   description=description)
            #bands.append(stac_band)
            
    eo_item.set_bands([stac_band], asset=asset)

    #eo_item.set_bands(bands)
          
    #eo_item.apply(bands)

    return item_out

