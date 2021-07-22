

import configparser
import glob
import re
import os
import shutil

from PIL import Image
from PIL.ExifTags import TAGS

def is_same_size(srcfile, dstfile):
    if os.path.getsize(srcfile) == os.path.getsize(dstfile):
        return True
    else:
        return False

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


    images_organized = set()

    scanned_dir = configs['OUTPUT']['scanned.directory']
    dups_dir = configs['OUTPUT']['duplicates.directory']
    organized_dir = configs['OUTPUT']['organized.directory']

    for filename in glob.iglob(input_files_pattern, recursive=True):
        image_datetime = get_image_datetime(filename)
        output_filename = ''
        if image_datetime:
            output_filename = get_filename(image_datetime)

            if output_filename in images_organized:
                dstfile = f"{organized_dir}\{output_filename}"

                # compare file sizes
                if is_same_size(filename, dstfile):
                    shutil.copy(filename, dups_dir)
                else:
                    print(f'tricky situation {filename}, {output_filename}')
            else:
                images_organized.add(output_filename)

                destfile = f'{organized_dir}\{output_filename}'
                shutil.copyfile(filename, destfile)


            '''
            - check if output_filename already exists in images_organized
                - if its there, then compare the file sizes to be sure we are dealing with diff images
                    - if the file sizes are same, its a duplicate, move the recent image to duplicates dir
                    - if the file sizes are diff, its not a duplicate, move the recent image to organized dir
                - if its not there
                    - add the output_filename in images_organized set
                    - copy the output_filename to organized dir
            '''

        else:
            # its a scanned image
            shutil.copy(filename, scanned_dir)
        
        # print(f'{filename}: {output_filename}')    


if __name__ == '__main__':
    main()