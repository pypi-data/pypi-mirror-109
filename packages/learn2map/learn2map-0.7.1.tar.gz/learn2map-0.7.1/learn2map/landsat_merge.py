import os
import glob
import sys
import time
import subprocess
from osgeo import gdal
import raster_tools as rt

ref_100='/Volumes/osb/dem//global_dem_100m.tif'
data_path='/Volumes/easystore/landsat/original'
out_file ='/Volumes/easystore/landsat/globe_l8_2013_2017.vrt'
os.chdir(data_path)
in_file = glob.glob('*l8sr_100m2013-2017*')
in_file_string = ' '.join('"{}"'.format(i) for i in in_file)
gdal_expression = 'gdalbuildvrt "{}" {}'.format(out_file, in_file_string)
print(gdal_expression)
subprocess.check_output(gdal_expression, shell=True)
print(in_file)
new_file = '/Volumes/easystore/landsat/globe_l8_2013_2017.tif'
rt.raster_clip(ref_100, out_file, new_file, resampling_method='near', srcnodata='nan', dstnodata='nan')