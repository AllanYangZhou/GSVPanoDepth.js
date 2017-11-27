#!/bin/bash

# http://vinayhacks.blogspot.com/2010/11/converting-equirectangular-panorama-to.html

# Make a new folder where you want the output images stored
# cd into that new folder
# Run '../equi2cubic.sh ../input_images'
# Where input_images is the folder with the panoramas.


for file in $1/*; do
    echo "[*] Processing: $file"
    filename=$(basename "$file")
    echo "$filename"
    erect2cubic --erect=$1/$file --ptofile=${filename::-4}.pto
    nona -o ${filename::-4}_cube ${filename::-4}.pto
    rm ${filename::-4}.pto
done

# Only care about forward and backwards cube faces
rm ./*0001.tif
rm ./*0003.tif
rm ./*0004.tif
rm ./*0005.tif

# Convert to jpg and resize
mogrify -format jpg -resize 264x264 -quality 100 depth*.tif
mogrify -format jpg -quality 100 pano*.tif
rm *.tif
