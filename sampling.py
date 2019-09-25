"""
TO RUN:
python cropping.py <dataset> <pixel_number> <training_image_number> <validation_image_number> --rename
"""

import os
import sys
import time
import random
import argparse
import numpy as np
from PIL import Image
from shutil import rmtree

#def npy_img(arguments):

def sampling(arguments):
    if not os.path.isdir(os.path.join('./data', arguments.dataset)):
        print("Dataset '{}' Does Not Exist!! \nSampling Aborted.".format(arguments.dataset))
        sys.exit(1)

    # Training and Validation Directories.
    train_directroy = './data/{0}/train'.format(arguments.dataset)
    validation_directroy = './data/{0}/validate'.format(arguments.dataset)

    # Input Image Directories

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Creation of Datasets of Smaller Images via Random Cropping')
    parser.add_argument('dataset', help='Name of Dataset from which to Crop Images')
    parser.add_argument('pixel_num', type=int, help='Side Length in Pixels of Images in New Dataset')
    #parser.add_argument('train_num', type=int, help='Number of Training Images in New Dataset')
    #parser.add_argument('val_num', type=int, help='Number of Validation Images in New Dataset')
    #parser.add_argument('-r', '--rename', action='store_true', help='Rename the New Dataset', dest='rename')
    args = parser.parse_args()
    sampling(args)
