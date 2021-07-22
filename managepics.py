

import configparser
import glob
import re
import os

from PIL import Image
from PIL.ExifTags import TAGS

def check_output_directories(output_dirs):
    for dir in output_dirs:
        if not os.path.exists(output_dirs[dir]):
            os.makedirs(output_dirs[dir])

def get_filename(image_datetime, extension='jpg'):
    
    # remove ':' from the date time string
    output_filename = re.sub(':', '', image_datetime)

    # replace space with underscore 
    output_filename = re.sub(' ', '_', output_filename)
 
    return f'{output_filename}.{extension}'

def get_image_datetime(filename, datetime_tag=306):
    image = Image.open(filename)
    exifdata = image.getexif()

    datetime = ''

    # tag 306 is DateTime
    if datetime_tag in exifdata.keys():
        datetime = exifdata.get(datetime_tag)
    
    return datetime


def main():

    # read the configurations
    configs = configparser.ConfigParser()
    configs.read('configs.ini')

    input_files_pattern = f"{configs['INPUT']['pics.directory']}\**\*.jpg"

    # check if output directories exist, it not create them
    check_output_directories(configs['OUTPUT'])

    for filename in glob.iglob(input_files_pattern, recursive=True):
        image_datetime = get_image_datetime(filename)
        output_filename = ''
        if image_datetime:
            output_filename = get_filename(image_datetime)

        print(f'{filename}: {output_filename}')    


if __name__ == '__main__':
    main()