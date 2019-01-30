#!/bin/bash

# Usage:   separateS1Google.sh original_data_path
# Example: separateS1Google.sh /datacube/original_data/S1_Google_Sample
# Assumptions: There is only one tif file and one associated csv file in the original_data_path dir
data_path=$1
COG_FLAGS_A='-co TILED=YES -co COMPRESS=DEFLATE'
COG_FLAGS_B='-co TILED=YES -co COPY_SRC_OVERVIEWS=YES -co BLOCKXSIZE=512 -co BLOCKYSIZE=512 --config GDAL_TIFF_OVR_BLOCKSIZE 512'


tCount=`ls -1 ${data_path}/*.tif 2>/dev/null | wc -l`
if [ $tCount != 1 ]
then 
echo "There needs to be only one tif file to process"
  exit 1
fi

cCount=`ls -1 ${data_path}/*.csv 2>/dev/null | wc -l`
if [ $cCount != 1 ]
then 
echo "There needs to be only one csv file to process"
  exit 1
fi

TotalAcquisitionCount=`tail -n+2 ${data_path}/*.csv | cut -d, -f1 | wc -l`
TotalBandCount=$((2 * ${TotalAcquisitionCount}))

#echo ${TotalAcquisitionCount}
#echo ${TotalBandCount}

bandCounter=1

for sceneid in `tail -n+2 ${data_path}/*.csv | cut -d, -f1`; do
  #echo $sceneid

  mkdir out/${sceneid};
  gdal_translate -b ${bandCounter} ${data_path}/*.tif tmp/${sceneid}_Gamma0_VV.tif ${COG_FLAGS_A}
  gdaladdo -r average tmp/${sceneid}_Gamma0_VV.tif 2 4 8 16 32
  gdal_translate tmp/${sceneid}_Gamma0_VV.tif out/${sceneid}/${sceneid}_Gamma0_VV.tif ${COG_FLAGS_B}
  rm tmp/${sceneid}_Gamma0_VV.tif
  bandCounter=$((${bandCounter} + 1))

  gdal_translate -b ${bandCounter} ${data_path}/*.tif tmp/${sceneid}_Gamma0_VW.tif ${COG_FLAGS_A}
  gdaladdo -r average tmp/${sceneid}_Gamma0_VW.tif 2 4 8 16 32
  gdal_translate tmp/${sceneid}_Gamma0_VW.tif out/${sceneid}/${sceneid}_Gamma0_VW.tif ${COG_FLAGS_B}
  tmp/${sceneid}_Gamma0_VW.tif
  bandCounter=$((${bandCounter} + 1))

  python3 ingest/prepare_scripts/sentinel_1/prepareS1Google.py out/${sceneid};
  exit 1
done


