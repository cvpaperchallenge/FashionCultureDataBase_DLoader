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
parser.add_argument('--save_dir', default='../VOC_format', type=str, help='path for save dir')
args = parser.parse_args()

# make save dirs
os.mkdir(args.save_dir)
os.mkdir(os.path.join(args.save_dir, 'Annotations'))
os.mkdir(os.path.join(args.save_dir, 'JPEGImages'))
os.mkdir(os.path.join(args.save_dir, 'ImageSets'))
os.mkdir(os.path.join(args.save_dir, 'ImageSets', 'Main'))

# Load metadata and ImageID list
print('Loading Data...')
f1 = open(args.yfcc)
lines = f1.readlines()
f2 = open(args.id_dict, 'r')
ids = json.load(f2)

err = 0
all = len(ids.items())
# Start Main loop
print('Start!!')
for i, (k, v) in enumerate(ids.items()):
    line = lines[int(k)]
    line_split = line.strip().split('\t')
    photo_id = line_split[1]
    photo_url = line_split[16]

    # Download Images
    save_img_path = os.path.join(args.save_dir, 'JPEGImages', photo_id + '.jpg')
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

    # Make VOC format
    annotation_el = Element('annotation')
    folder_el = SubElement(annotation_el, 'folder')
    folder_el.text = 'FCDBv2'
    filename_el = SubElement(annotation_el, 'filename')
    filename_el.text = photo_id

    source_el = SubElement(annotation_el, 'source')
    database_el = SubElement(source_el, 'database')
    database_el.text = 'Fashion Culture DataBase V2'
    size_el = SubElement(annotation_el, 'size')
    width_el = SubElement(size_el, 'width')
    width_el.text = str(size[0])
    height_el = SubElement(size_el, 'height')
    height_el.text = str(size[1])

    for box in v:
        object_el = SubElement(annotation_el, 'object')
        name_el = SubElement(object_el, 'name')#name
        name_el.text = 'person'
        diff_el = SubElement(object_el, 'difficult')#difficult
        diff_el.text = '0'
        bndbox_el = SubElement(object_el, 'bndbox')#bndbox
        xmin_el = SubElement(bndbox_el, 'xmin')
        xmin_el.text = str(box[0])
        ymin_el = SubElement(bndbox_el, 'ymin')
        ymin_el.text = str(box[1])
        xmax_el = SubElement(bndbox_el, 'xmax')
        xmax_el.text = str(box[2])
        ymax_el = SubElement(bndbox_el, 'ymax')
        ymax_el.text = str(box[3])

    save_anno_path = os.path.join(args.save_dir, 'Annotations', photo_id + '.xml')
    tree = ET.ElementTree(element=annotation_el)
    tree.write(save_anno_path, xml_declaration = False)

    if (i + 1) % 10000:
        print('Progress:', i, '/', all)

print('Saved :', i + 1)
print('Error :', i + 1 - err)

anno_files = os.listdir(os.path.join(args.save_dir, 'Annotations'))
for anno_file in anno_files:
    name, ext = os.path.splitext(anno_file)
    text_p = name + "  1"
    text_t = name

    t = open(os.path.join(args.save_dir, 'ImageSets/Main/person_trainval.txt'), "a")
    t.write(text_p + "\n")
    t.close()

    t = open(os.path.join(args.save_dir, 'ImageSets/Main/trainval.txt'), "a")
    t.write(text_t + "\n")
    t.close()

print('Finish!!')
