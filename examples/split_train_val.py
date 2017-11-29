from shutil import copyfile
import glob
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('input')
parser.add_argument('output')
args = parser.parse_args()

depth_paths = glob.glob('./{:s}/depth*'.format(args.input))

trainAdir = '{:s}/A/train'.format(args.output)
testAdir = '{:s}/A/test'.format(args.output)
trainBdir = '{:s}/B/train'.format(args.output)
testBdir = '{:s}/B/test'.format(args.output)
os.makedirs(trainAdir)
os.makedirs(testAdir)
os.makedirs(trainBdir)
os.makedirs(testBdir)

i = 0
for depth_path in depth_paths:
    base, ext = os.path.splitext(os.path.basename(depth_path))
    postfix = base[5:]
    pano_path = os.path.join(args.input, 'pano{:s}.jpg'.format(postfix))
    if i < 1300:
        out_depth_path = os.path.join(trainAdir, 'im{:s}.jpg'.format(postfix))
        out_pano_path = os.path.join(trainBdir, 'im{:s}.jpg'.format(postfix))
    else:
        out_depth_path = os.path.join(testAdir, 'im{:s}.jpg'.format(postfix))
        out_pano_path = os.path.join(testBdir, 'im{:s}.jpg'.format(postfix))
    copyfile(depth_path, out_depth_path)
    copyfile(pano_path, out_pano_path)
    i += 1
