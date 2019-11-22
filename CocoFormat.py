import os
import argparse
import json
import urllib.error
import urllib.request
from PIL import Image
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
import xml.etree.ElementTree as ET

parser = argparse.ArgumentParser(description = 'collect FCDBv2 from YFCC100M')
parser.add_argument('--yfcc', default='../YFCC100Mpart0', type=str, help='path for yfcc100m metadata')
parser.add_argument('--id_dict', default='../image_id_list.json', type=str, help='path for image id list')
parser.add_argument('--save_dir', default='../COCO_format', type=str, help='path for save dir')
args = parser.parse_args()

# make save dirs
os.mkdir(args.save_dir)
os.mkdir(os.path.join(args.save_dir, 'images'))

# infomation
info = {
    "description": "FCDBv2",
    "url": "http://",
    "version": "1.0",
    "year": 2019,
    "contributor": "AIST",
    "date_created": "2019/12/01"
}
categories = [
    {"supercategory": "human", "id": 1, "name": "person"}
]
images = []
annotations = []

# Load metadata and ImageID list
print('Loading Data...')
f1 = open(args.yfcc)
lines = f1.readlines()
f2 = open(args.id_dict, 'r')
ids = json.load(f2)

err = 0
obj_id = 1
all = len(ids.items())
# Start Main loop
print('Start!!')
for img_id, (k, v) in enumerate(ids.items()):
    line = lines[int(k)]
    line_split = line.strip().split('\t')
    photo_id = line_split[1]
    photo_url = line_split[16]

    # Download Images
    save_img_path = os.path.join(args.save_dir, 'images', photo_id + '.jpg')
    if os.path.exists(save_img_path) == True: continue
    try:
        with urllib.request.urlopen(photo_url) as web_file:
            data = web_file.read()
            with open(save_img_path, mode='wb') as local_file:
                local_file.write(data)
    except:
        err += 1
        continue
    
    try:
        img = Image.open(save_img_path)
        size = img.size
    except:
        os.remove(save_img_path)
        err += 1
        continue

    # Make COCO format
    img_data = {
        #"license": 4,
        "file_name": photo_id + '.jpg',
        #"coco_url": "http://images.cocodataset.org/val2017/000000397133.jpg",
        "height": size[1],
        "width": size[0],
        #"date_captured": "2013-11-14 17:02:52",
        #"flickr_url": "http://farm7.staticflickr.com/6116/6255196340_da26cf2c9e_z.jpg",
        "id": img_id
    }
    images.append(img_data)

    for box in v:
        anno_data = {
            #"segmentation": [[510.66,423.01,511.72,420.03,...,510.45,423.01]],
            #"area": 702.1057499999998,
            #"iscrowd": 0,
            "image_id": img_id,
            "bbox": [box[0], box[1], box[2] - box[0], box[3] - box[1]],
            "category_id": 1,
            "id": obj_id
        }
        obj_id += 1
        annotations.append(anno_data)



    if (img_id + 1) % 10000:
        print('Progress:', img_id, '/', all)
        break

dict_ = {}
dict_["info"] = info
dict_["images"] = images
dict_["annotations"] = annotations
dict_["categories"] = categories

save_path = os.path.join(args.save_dir, 'FCDBv2_train.json')
fw = open(save_path,'w')
json.dump(dict_, fw)

print('Saved :', i + 1 - err)
print('Error :', err)
print('Finish!!')
