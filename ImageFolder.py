import os
import argparse
import json
import urllib.error
import urllib.request
from PIL import Image

parser = argparse.ArgumentParser(description = 'collect FCDBv2 from YFCC100M')
parser.add_argument('--yfcc', default='./yfcc100m_dataset', type=str, help='path for yfcc100m metadata')
parser.add_argument('--id_json', default='./image_id_list.json', type=str, help='path for image id list')
parser.add_argument('--save_dir', default='./VOC_format', type=str, help='path for save dir')
args = parser.parse_args()

CITYS = {'London': (-0.12776, 51.50735), 'NewYork': (-74.0059, 40.71278),
            'Boston': (-71.0589, 42.36008), 'Paris': (2.352222, 48.85661),
            'Toronto': (-79.3832, 43.65323), 'Barcelona': (2.173403, 41.38506),
            'Tokyo': (139.6917, 35.68949), 'SanFrancisco': (122.419, 37.77493),
            'HongKong': (114.1095, 22.39643), 'Zurich': (8.541694, 47.37689),
            'Seoul': (126.978, 37.56654), 'Beijing': (116.4074, 39.90421),
            'Bangkok': (100.5018, 13.75633), 'Singapore': (103.8198, 1.352083),
            'KualaLumpur': (101.6869, 3.139003), 'NewDelhi': (77.20902, 28.61394)}

os.mkdir(args.save_dir)
for name in CITYS.keys(): os.mkdir(os.path.join(args.save_dir, name))

# Load metadata and ImageID list
print('Loading Data...')
f1 = open(args.yfcc)
lines = f1.readlines()
f2 = open(args.id_json, 'r')
ids = json.load(f2)

err = 0
all = len(ids.items())
# Start Main loop
print('Start!!')
for i, (k, v) in enumerate(ids.items()):
    line = lines[int(k)]
    line_split = line.strip().split('\t')
    photo_id = line_split[1]
    Longitude = float(line_split[13])
    Latitude = float(line_split[14])
    photo_url = line_split[16]

    euclids = []
    for LL in CITYS.values():
        euc = (Longitude - LL[0])**2 + (Latitude - LL[1])**2
        euclids.append(euc)
    city_txt = list(CITYS.keys())[euclids.index(min(euclids))]

    # Download Images
    ori_img_path = os.path.join(args.save_dir, photo_id + '.jpg')
    if os.path.exists(ori_img_path) == True: continue
    try:
        with urllib.request.urlopen(photo_url) as web_file:
            data = web_file.read()
            with open(ori_img_path, mode='wb') as local_file:
                local_file.write(data)
    except:
        continue
    
    try:
        img = Image.open(ori_img_path)
    except:
        os.remove(ori_img_path)
        continue

    for j, box in enumerate(v):
        coor = (box[0], box[1], box[2], box[3])
        save_img_path = os.path.join(args.save_dir, city_txt,
                    photo_id + '_' + str(j) + '.jpg')
        try:
            img.crop(coor).save(save_img_path, quality=95)
        except:
            continue

    os.remove(ori_img_path)

    if (i + 1) % 2500 == 0:
        print('Progress:', i + 1, '/', all)
