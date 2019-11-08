import os
import json
import urllib.error
import urllib.request
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
import xml.etree.ElementTree as ET

import sys
import cv2

yfcc = '/media/minoguchi/FCDB2/YFCC100M/yfcc100m_dataset'
id_dict = './image_id_list.json'
save_dir = './images'

#def img_download(url, filename):
#    img = urllib.request.urlopen(url)
#    fout = open(filename, 'wb')
#   fout.write(img.read())
#   img.close()
#   fout.close()

def img_download(url, dst_path):
    try:
        with urllib.request.urlopen(url) as web_file:
            data = web_file.read()
            with open(dst_path, mode='wb') as local_file:
                local_file.write(data)
    except urllib.error.URLError as e:
        print(e)

print('Load Data...')
fin = open(yfcc)
lines = fin.readlines()

f = open(id_dict, 'r')
ids = json.load(f)


print('Start!!')
for i, (k, v) in enumerate(ids.items()):
    line = lines[int(k)]
    line_split = line.strip().split('\t')
    photo_id = line_split[1]
    photo_url = line_split[16]

    save_path = os.path.join(save_dir, photo_id + '.jpg')
    img_download(photo_url, save_path)

    img = cv2.imread(save_path)
    for box in v:
        cv2.rectangle(img, (int(box[0]), int(box[1])),
                    (int(box[2]), int(box[3])), (0, 0, 255), 2)

    cv2.imwrite(save_path, img)

    if i > 10:
        print(i)
        sys.exit()

print('Finish!!')