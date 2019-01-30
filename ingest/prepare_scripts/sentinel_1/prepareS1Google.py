"""
Prepare a dataset (specifically an orthorectified Sentinel 1 scene in BEAM-DIMAP format) for datacube indexing.

Note, this script is only an example. For production purposes, more metadata would be harvested.

The BEAM-DIMAP format (output by Sentinel Toolbox/SNAP) consists of an XML header file (.dim)
and a directory (.data) which stores different polarisations (different raster bands) separately,
each as ENVI format, that is, raw binary (.img) with ascii header (.hdr). GDAL can read ENVI
format (that is, when provided an img it checks for an accompanying hdr).
"""

import os
import sys
import uuid
from pathlib import Path
from xml.etree import ElementTree  # should use cElementTree..

import click
import rasterio
import yaml
from dateutil import parser
from dateutil.parser import parse
from osgeo import osr


def get_geometry(path):
    with rasterio.open(path) as img:
        left, bottom, right, top = img.bounds
        crs = str(str(getattr(img, 'crs_wkt', None) or img.crs.wkt))
        corners = {
            'ul': {
                'x': left,
                'y': top
            },
            'ur': {
                'x': right,
                'y': top
            },
            'll': {
                'x': left,
                'y': bottom
            },
            'lr': {
                'x': right,
                'y': bottom
            }
        }
        projection = {'spatial_reference': crs, 'geo_ref_points': corners}

        spatial_ref = osr.SpatialReference(crs)
        t = osr.CoordinateTransformation(spatial_ref, spatial_ref.CloneGeogCS())

        def transform(p):
            lon, lat, z = t.TransformPoint(p['x'], p['y'])
            return {'lon': lon, 'lat': lat}

        extent = {key: transform(p) for key, p in corners.items()}

        return projection, extent


bands = ['vh', 'vv']


def band_name(path):
    # name = path.stem
    # position = name.find('_')
    if 'VH' in str(path):
        layername = 'vh'
    if 'VV' in str(path):
        layername = 'vv'
    return layername


def prep_dataset(path):

    scene_name = str(path)
	
    print("Preparing scent {}".format(scene_name))
    t0=parse(scene_name.split("_")[-5].split(".")[0])
    # print(t0)
    t1=parse(scene_name.split("_")[-4].split(".")[0])
    # print(t1)	

    # TODO: which time goes where in what format?
    # could also read processing graph, or
    # could read production/productscenerasterstart(stop)time

    # get bands
    # TODO: verify band info from csv
    images = {
        band_name(im_path): {
            'path': str(im_path.relative_to(path))
        } for im_path in path.glob('*.tif')
    }
    # print(images)
	
    # trusting bands coaligned, use one to generate spatial bounds for all

    projection, extent = get_geometry('/'.join([str(path), images['vv']['path']]))

    # format metadata (i.e. construct hashtable tree for syntax of file interface)

    return {
        'id': str(uuid.uuid5(uuid.NAMESPACE_URL, scene_name)),
        'processing_level': "GEE_ARD",
        'product_type': "gamma0",
        'creation_dt': t0,
        'platform': {
            'code': 'SENTINEL_1'
        },
        'instrument': {
            'name': 'SAR'
        },
        'extent': {
            'coord': extent,
            'from_dt': str(t0),
            'to_dt': str(t1),
            'center_dt': str(t0 + (t1 - t0) / 2)
        },
        'format': {
            'name': 'GeoTiff'
        },
        'grid_spatial': {
            'projection': projection
        },
        'image': {
            'bands': images
        },
        'lineage': {
            'source_datasets': {},
            'ga_label': scene_name
        }  # TODO!
        # C band, etc...
    }


@click.command(
    help="Prepare S1A/B data processed with GPT in BEAM-DIMAP format dataset for ingestion into the Data Cube.")
@click.argument('datasets', type=click.Path(exists=True, readable=True, writable=True), nargs=-1)
def main(datasets):
    for dataset in datasets:
        path = Path(dataset)
        print("Starting for dataset " + dataset)
        metadata = prep_dataset(path)

        yaml_path = str(path.joinpath('datacube-metadata.yaml'))

        with open(yaml_path, 'w') as stream:
            yaml.dump(metadata, stream)


if __name__ == "__main__":
    main()
