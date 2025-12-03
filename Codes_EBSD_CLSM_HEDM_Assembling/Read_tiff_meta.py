from PIL import Image
from PIL.TiffTags import TAGS

path = '/home/NFOLASTRE/Documents/Codes_EBSD_CLSM_HEDM_Assembling/data/SC3_Project 1 Specimen 2 Site 1 Map Data 4_EBSD_tilted_32b_Euler3.tif'


with Image.open(path) as img:
    meta_dict = {TAGS[key] : img.tag[key] for key in img.tag.iterkeys()}
    print(meta_dict)