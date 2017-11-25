import argparse
import glob
import matplotlib.pyplot as plt
from skimage.io import imread
from skimage.transform import resize
from shutil import copyfile
import numpy as np
import os


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('in_folder', type=str)
    parser.add_argument('out_folder', type=str)
    args = parser.parse_args()
    os.makedirs(args.out_folder)
    depth_paths = glob.glob(os.path.join(args.in_folder, 'depth*'))
    num_pairs = len(depth_paths)
    display = None
    for depth_path in depth_paths:
        number = int(os.path.basename(depth_path).split('.')[0][5:])
        pano_path = os.path.join(args.in_folder, 'pano{:d}.png'.format(number))
        if not os.path.exists(pano_path):
            print('Missing corresponding panorama for depth map {:d}, skipping!'.format(number))
            continue
        depth_image = imread(depth_path)
        h, w, _ = depth_image.shape
        pano_image = imread(pano_path)
        pano_image = 255 * resize(pano_image, (h,w))
        pano_image = pano_image.astype('uint8')
        combined_image = np.concatenate([pano_image, depth_image], axis=0)
        if display is None:
            display = plt.imshow(combined_image)
            plt.show(block=False)
        else:
            display.set_data(combined_image)
            plt.draw()
        response = raw_input('Press [Enter] or "y" to accept, type "n" to reject.')
        if response == '' or response == 'y':
            print('Accepting')
            out_depth_path = os.path.join(args.out_folder, 'depth{:d}.png'.format(number))
            out_pano_path = os.path.join(args.out_folder, 'pano{:d}.png'.format(number))
            copyfile(depth_path, out_depth_path)
            copyfile(pano_path, out_pano_path)
        else:
            print('Rejecting')
