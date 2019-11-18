import os
import argparse
import json
import urllib.error
import urllib.request
from PIL import Image

parser = argparse.ArgumentParser(description = 'collect FCDBv2 from YFCC100M')
parser.add_argument('--yfcc', default='../YFCC100Mpart0', type=str, help='path for yfcc100m metadata')
parser.add_argument('--id_dict', default='../image_id_list.json', type=str, help='path for image id list')
parser.add_argument('--save_dir', default='../VOC_format', type=str, help='path for save dir')
args = parser.parse_args()

CITYS = ['London', 'NewYork', 'Boston', 'Paris', 'Toronto',
            'Barcelona', 'Tokyo', 'SanFrancisco', 'HongKong',
            'Zurich', 'Seoul', 'Beijing', 'Bangkok',
            'Singapore', 'KualaLumpur', 'NewDelhi']

os.mkdir(args.save_dir)
for name in CITYS: os.mkdir(os.path.join(args.save_dir, name))

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
        continue
    
    try:
        img = Image.open(save_img_path)
    except:
        os.remove(save_img_path)
        continue

    for j, box in enumerate(v):
        coor = (box[0], box[1], box[2], box[3])
        img_save = os.path.join(args.save_dir, city_txt,
                    photo_id + '_' + str(j) + '.jpg')
        try:
            img.crop(coor).save(img_save, quality=95)
        except:
            continue




xml_list = os.listdir(os.path.join(args.voc_dir, 'Annotations'))
random.shuffle(xml_list)
print("xmls :", len(xml_list))

for xml in xml_list:
    xml_data = os.path.join(args.voc_dir, 'Annotations', xml)
    # find source
    try: tree_o = ET.parse(xml_data)
    except: continue
    source_o = tree_o.find('source')
    city_txt = source_o.find('city').text
    if CITYS[city_txt] == args.num_per_cls: continue
    filename_txt = tree_o.find('filename').text
    img_path = os.path.join(args.voc_dir, 'JPEGImages', filename_txt)
    img = Image.open(img_path)
    size = img.size
    # find boxes
    objects_o = tree_o.findall('object')
    for i, object_o in enumerate(objects_o):
        bndbox_o = object_o.find('bndbox')
        xmin = int(bndbox_o.find('xmin').text)
        ymin = int(bndbox_o.find('ymin').text)
        xmax = int(bndbox_o.find('xmax').text)
        ymax = int(bndbox_o.find('ymax').text)
        if xmin < 0: xmin = 0
        if ymin < 0: ymin = 0
        if xmax > size[0]: xmax = size[0]
        if ymax > size[1]: ymax = size[1]

        box = (xmin, ymin, xmax, ymax)
        img_save = os.path.join(args.save_dir, city_txt,
                    filename_txt.replace('.jpg', '') + '_' + str(i) + '.jpg')
        try:
            img.crop(box).save(img_save, quality=95)
        except:
            continue

        CITYS[city_txt] += 1
        if CITYS[city_txt] == args.num_per_cls: break

print("# ----- finish !! ----- #")
