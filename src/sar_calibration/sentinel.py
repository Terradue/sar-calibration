import os
import sys
import gdal
import logging 
from .output import rescale
from snapista import Graph, Operator
from pystac import Item, extensions, Asset, MediaType

logging.basicConfig(stream=sys.stderr, 
                    level=logging.DEBUG,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%dT%H:%M:%S')

def calibrate(item):

    logging.info(f'Calibrate Sentinel-1 GRD acquisition {item.id}')

    temp_result = f"temp_{item.id}_SIGMA0_DB.tif"
    result = f"{item.id}_SIGMA0_DB.tif"

    g = Graph()

    g.add_node(
        operator=Operator(
            "Read", 
            formatName="SENTINEL-1", 
            file=item.get_assets()['manifest'].get_absolute_href().replace('file://', '')
        ), 
        node_id="read"
    )

    g.add_node(
        operator=Operator("Apply-Orbit-File", continueOnFail="true"),
        node_id="apply-orbit-file",
        source="read",
    )

    g.add_node(
        operator=Operator("Remove-GRD-Border-Noise", borderLimit="2000", trimThreshold="0.2"),
        node_id="noise-removal",
        source="apply-orbit-file",
    )

    g.add_node(
        operator=Operator("Calibration", selectedPolarisations="VV"),
        node_id="calibration",
        source="noise-removal",
    )

    g.add_node(
        operator=Operator("LinearToFromdB", sourceBandNames="Sigma0_VV"),
        node_id="linear",
        source="calibration",
    )

    g.add_node(
        operator=Operator(
            "Terrain-Correction", pixelSpacingInMeter="20.0", demName="SRTM 1Sec HGT"
        ),
        node_id="terrain-correction",
        source="linear",
    )

    g.add_node(
        operator=Operator("Write", file=temp_result, formatName="GeoTIFF-BigTIFF"),
        node_id="write",
        source="terrain-correction",
    )

    g.run()

    rescale(temp_result, result)

    item_out = to_stac(item, result)

    return item_out

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

    band = 'sigma_db_vv'

    item_out.add_asset(key=band.lower(), 
                               asset=Asset(href=in_tiff, 
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

