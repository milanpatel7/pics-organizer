
# TO-DO list:
# create the output directories if it doesn't exist

import glob
import re

from PIL import Image
from PIL.ExifTags import TAGS

# get timestamp of the image
def get_image_datetime(filename):
    image = Image.open(filename)
    exifdata = image.getexif()

    datetime = ''

    # tag 306 is DateTime
    if 306 in exifdata.keys():
        datetime = exifdata.get(306)
        # if isinstance(datetime, bytes):
        #     datetime = datetime.decode()
    
    return datetime

def get_filename(image_datetime):
    
    # remove ':' from the date time string
    output_filename = re.sub(':', '', image_datetime)

    # replace space with underscore 
    output_filename = re.sub(' ', '_', output_filename)

    return output_filename

for filename in glob.iglob('pics\**\*.jpg', recursive=True):
    image_datetime = get_image_datetime(filename)
    if image_datetime:
        output_filename = get_filename(image_datetime)

    print(f'{filename}: {output_filename}')    


