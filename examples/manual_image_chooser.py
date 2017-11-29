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
    parser.add_argument('--start', type=int, default=0)
    args = parser.parse_args()
    if not os.path.exists(args.out_folder):
        os.makedirs(args.out_folder)
    depth_paths = glob.glob(os.path.join(args.in_folder, 'depth*'))
    depth_paths = sorted(depth_paths)
    num_pairs = len(depth_paths)
    display = None
    for i, depth_path in enumerate(depth_paths):
        base, ext = os.path.splitext(os.path.basename(depth_path))
        postfix = base[5:]
        if i < args.start: # Skip images if they are before the specified start number
            continue
        pano_path = os.path.join(args.in_folder, 'pano{:s}{:s}'.format(postfix, ext))
        if not os.path.exists(pano_path):
            print(pano_path)
            print('Missing corresponding panorama for depth map {:d}, skipping!'.format(i))
            continue
        depth_image = imread(depth_path)
        if depth_image.ndim < 3:
            depth_image = np.stack(3 * [depth_image], axis=2)
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
        response = raw_input('Pair {:d}: Press [Enter] or "y" to accept, type "n" to reject.'.format(i))
        if response == '' or response == 'y':
            print('Accepted.')
            out_depth_path = os.path.join(args.out_folder, 'depth{:s}{:s}'.format(postfix, ext))
            out_pano_path = os.path.join(args.out_folder, 'pano{:s}{:s}'.format(postfix, ext))
            copyfile(depth_path, out_depth_path)
            copyfile(pano_path, out_pano_path)
        else:
            print('Rejected.')
