#!/bin/bash

# http://vinayhacks.blogspot.com/2010/11/converting-equirectangular-panorama-to.html

# Make a new folder where you want the output images stored
# cd into that new folder
# Run '../equi2cubic.sh ../input_images'
# Where input_images is the folder with the panoramas.


for file in $(ls $1); do
    echo "[*] Processing: $1/$file"
    erect2cubic --erect=$1/$file --ptofile=${file::-4}.pto
    nona -o ${file::-4}_cube ${file::-4}.pto
    rm ${file::-4}.pto
done
