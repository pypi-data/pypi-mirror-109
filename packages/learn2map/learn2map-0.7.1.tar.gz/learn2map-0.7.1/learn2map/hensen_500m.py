import os
import glob
import sys
import time
import subprocess
from osgeo import gdal
import raster_tools as rt

# data_path = '/Volumes/MyBookThunderboltDuo/hensen_data/2019'
# os.chdir(data_path)
#
# ref_file = '/Volumes/MyBookThunderboltDuo/fire_data/globe_BAF_P_500m_2014.tif'
# in_file = glob.glob('h2019_gfc_lossyear_30m-*')
# out_file = '/Volumes/MyBookThunderboltDuo/hensen_data/2019/globe_hensen_30m.vrt'
# in_file_string = ' '.join('"{}"'.format(i) for i in in_file)
# gdal_expression = 'gdalbuildvrt "{}" {}'.format(out_file, in_file_string)
# print(gdal_expression)
# subprocess.check_output(gdal_expression, shell=True)
# print(in_file)
# output_x = '/Volumes/MyBookThunderboltDuo/gfc_gain_loss_v16/output/global_hensen_500m_pct_2019.tif'
# rt.raster_clip(ref_file, out_file, output_x, resampling_method='average', srcnodata='nan', dstnodata='nan')
# ref_file1='/Volumes/MyBookThunderboltDuo/globbiomass_output/output/globe_baf_10km_2001.tif'
# output_x1= '/Volumes/MyBookThunderboltDuo/gfc_gain_loss_v16/output/globe_hensen_10km_pct_2018.tif'
# rt.raster_clip(ref_file1, out_file, output_x1, resampling_method='average', srcnodata='nan', dstnodata='nan')

# data_path = '/Volumes/MyBookThunderboltDuo/modis'
# os.chdir(data_path)
#
# ref_file = '/Volumes/MyBookThunderboltDuo/fire_data/globe_BAF_P_500m_2014.tif'
# in_file = glob.glob('mcd64_annual_2019-*')
# out_file = '/Volumes/MyBookThunderboltDuo/modis/globe_BA_500m2019.vrt'
# in_file_string = ' '.join('"{}"'.format(i) for i in in_file)
# gdal_expression = 'gdalbuildvrt "{}" {}'.format(out_file, in_file_string)
# print(gdal_expression)
# subprocess.check_output(gdal_expression, shell=True)
# print(in_file)
# output_x = '/Volumes/MyBookThunderboltDuo/modis/global_BA_500m_2019.tif'
# rt.raster_clip(ref_file, out_file, output_x, resampling_method='average', srcnodata='nan', dstnodata='nan')

data_path = '/Volumes/Sassan_Data/global_1km/landsat/original_2019_20'
os.chdir(data_path)
ref_file = '/Volumes/Sassan_Data/global_1km/reference_geo_1km.tif'
in_file = glob.glob('globe_r*')
out_file = '/Volumes/Sassan_Data/global_1km/landsat/output/globe_l8_2019_2020_100m.vrt'
in_file_string = ' '.join('"{}"'.format(i) for i in in_file)
gdal_expression = 'gdalbuildvrt "{}" {}'.format(out_file, in_file_string)
print(gdal_expression)
subprocess.check_output(gdal_expression, shell=True)
print(in_file)
output_x = '/Volumes/Sassan_Data/global_1km/landsat/output/global_l8_1km_2019_2020_med.tif'
rt.raster_clip(ref_file, out_file, output_x, resampling_method='med', srcnodata='nan', dstnodata='nan')
output_x1 = '/Volumes/Sassan_Data/global_1km/landsat/output/global_l8_1km_2019_2020_q1.tif'
rt.raster_clip(ref_file, out_file, output_x1, resampling_method='q1', srcnodata='nan', dstnodata='nan')
output_x2 = '/Volumes/Sassan_Data/global_1km/landsat/output/global_l8_1km_2019_2020_q3.tif'
rt.raster_clip(ref_file, out_file, output_x2, resampling_method='q3', srcnodata='nan', dstnodata='nan')
output_x3 = '/Volumes/Sassan_Data/global_1km/landsat/output/global_l8_1km_2019_2020_min.tif'
rt.raster_clip(ref_file, out_file, output_x3, resampling_method='min', srcnodata='nan', dstnodata='nan')
output_x4 = '/Volumes/Sassan_Data/global_1km/landsat/output/global_l8_1km_2019_2020_max.tif'
rt.raster_clip(ref_file, out_file, output_x4, resampling_method='max', srcnodata='nan', dstnodata='nan')