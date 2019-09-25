"""
Folder Tree:
./data/<Dataset Name>/images.jpg or png formats

TO RUN:
python cropping.py <dataset> <pixel_number> <split> <training_image_number> <validation_image_number> --rename
"""

import os
import sys
import time
import random
import argparse
import numpy as np
from PIL import Image
from shutil import rmtree

def sampling(arguments):
    if not os.path.isdir(os.path.join('./data', arguments.dataset)):
        print("Dataset '{0}' Does Not Exist!! \nSampling Aborted.".format(arguments.dataset))
        sys.exit(1)

    # Image Directory
    image_directroy = './data/{0}'.format(arguments.dataset)

    # Check validity of number
    if arguments.split > 100:
        print("Validation Image Number Can Not Over Whole Images!")
        sys.exit(1)

    # Input Image Directories
    try:
        split_num = int(round(len([name for name in os.listdir(image_directroy) if os.path.isfile(os.path.join(image_directroy, name)) and name[0] != '.'])*arguments.split / 100 ))
        dataset_names = [name for name in os.listdir(image_directroy) if os.path.isfile(os.path.join(image_directroy, name)) and name[0] != '.'] # Exclude .ds_Store file
        train_image_names = dataset_names[split_num:]
        train_image_names.sort()
        validation_image_names = dataset_names[:split_num]
        validation_image_names.sort()
    except FileNotFoundError:
        print("Image Directories Does Not Exist!")
        sys.exit(1)

    # Parameters for Image Sampling
    pixels = arguments.pixel_num
    train_image_num = arguments.train_num
    validation_image_num = arguments.val_num
    out_dir = './data/{0}_{1:d}pix_{2:d}num_{3:d}%'.format(arguments.dataset, pixels, train_image_num, arguments.split)

    # Get if Dataset Name from User if given rename flag
    if arguments.rename:
        print("Rename flag activated.", "Default dataset name: {0}".format(out_dir[7:]),"", sep='\n')
        prompt = "What would you like to name the new dataset? "
        out_dir_name = input(prompt)
        if out_dir_name is not None:
            out_dir = './data/{0}'.format(out_dir_name)

    # Check if dataset already exists and ask to continue
    if os.path.isdir(out_dir):
        if not query("Dataset directroy already exists. Would you like to continue?"):
            print("Sampling Aborted.")
            sys.exit(1)

    # To time entire process
    start_time = time.time()

    # Output Images Directories
    train_im_out_dir = os.path.join(out_dir, 'train')
    val_im_out_dir = os.path.join(out_dir, 'validate')

    # Create Output Directories if necessary
    if not os.path.isdir(train_im_out_dir):
        os.makedirs(train_im_out_dir)
    if not os.path.isdir(val_im_out_dir):
        os.makedirs(val_im_out_dir)

    # Loop through all Images
    print("Creating Traing Images ({0}): \n".format(train_image_num))
    for num in range(train_image_num):
        start = time.time() * 1000

        # Generate random number for choosing files from directories
        file_num = random.randint(0, len(train_image_names)) - 1

        # Load Images Using PIL and Check the size
        image = Image.open(os.path.join(image_directroy, train_image_names[file_num]))
        if image.size[0] - pixels < 0 and image.size[1]-pixels < 0:
            print("Sampling Images Must be Samller than Full-Sized Images!",
                  "Image Size: {0:s}".format(image.size), sep='\n')
            rmtree(out_dir)
            sys.exit(1)

        # Generate Random Upper-Left Coordinate for Sampling
        x_cord = random.randint(0, image.size[0] - pixels)
        y_cord = random.randint(0, image.size[1] - pixels - 64)

        # Name for Images
        image_format = train_image_names[file_num][-4:]
        image_name = train_image_names[file_num][:-4] + '_x{0:d}_y{1:d}{2:s}'.format(x_cord, y_cord, image_format)

        # Sampling and Saving Images
        print("Sampling Image {0} at x = {1} and y = {2} ...".format(train_image_names[file_num][:-4], x_cord, y_cord))
        image.crop((x_cord, y_cord, x_cord+pixels, y_cord+pixels)).save(os.path.join(train_im_out_dir, image_name))

        print("Done! Time Taken: {0:.3f} milliseconds \n".format(time.time()*1000-start))
    print("Completed Training Images \n")

    # Loop through all validation Images
    print("Creating Traing Images ({0}): \n".format(validation_image_num))
    for num in range(validation_image_num):
        start = time.time() * 1000
        # Generate random number for choosing files from directories
        file_num = random.randint(0, len(validation_image_names)) - 1

        # Load Images Using PIL
        image = Image.open(os.path.join(image_directroy, validation_image_names[file_num]))

        # Generate Random Upper-Left Coordinate for Sampling
        x_cord = random.randint(0, image.size[0] - pixels)
        y_cord = random.randint(0, image.size[1] - pixels -64)

        # Name for Images
        image_format = validation_image_names[file_num][-4:]
        image_name = validation_image_names[file_num][:-4] + '_x{0:d}_y{1:d}{2:s}'.format(x_cord, y_cord, image_format)

        # Sampling and Saving Images
        print("Sampling Image {0} at x = {1} and y = {2} ...".format(validation_image_names[file_num][:-4], x_cord, y_cord))
        image.crop((x_cord, y_cord, x_cord+pixels, y_cord+pixels)).save(os.path.join(val_im_out_dir, image_name))

        print("Done! Time Taken: {0:.3f} milliseconds \n".format(time.time()*1000 - start))
    print("Completed Validation Images \n")

    time_taken = time.time() - start_time
    print("Total Time Taken:{0:<.3f} seconds".format(time_taken))


# Query function for command line input
def query(question):
    valid = {'yes': True, 'ye': True, 'y': True,
             'no': False, 'n': False}
    choice = input(question + '[yes/no]: ').lower()
    if choice in valid.keys():
        return valid[choice]
    else:
        chance = input("Please respond with 'yes' or 'no' ('y' or 'n'): ").lower()
        if chance in valid.keys():
            return valid[chance]
        else:
            print('Exiting...')
            sys.exit(1)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Creation of Datasets of Smaller Images via Random Sampling', usage = 'python sampling.py <dataset> <pixel_number> <training_image_number> <validation_image_number> --rename')
    parser.add_argument('dataset', help='Name of Dataset from which to Crop Images')
    parser.add_argument('pixel_num', type=int, help='Side Length in Pixels of Images in New Dataset')
    parser.add_argument('split', type=int, help='Percentage of Validation Images in New Dataset (1-100)')
    parser.add_argument('train_num', type=int, help='Number of Training Images in New Dataset')
    parser.add_argument('val_num', type=int, help='Number of Validation Images in New Dataset')
    parser.add_argument('-r', '--rename', action='store_true', help='Rename the New Dataset', dest='rename')
    args = parser.parse_args()
    sampling(args)
