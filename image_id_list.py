import os
import json
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
import xml.etree.ElementTree as ET

def rem_xml(li):
    return li - '.xml'

yfcc = '/media/minoguchi/FCDB2/YFCC100M/yfcc100m_dataset'
xml_dir = '/home/minoguchi/data/FCDB_voc/Annotations'

fin = open(yfcc)
dicts = {}

print('Start YFCC100M')
for i, line in enumerate(fin):

    line_split = line.strip().split('\t')
    line_num = int(line_split[0]) # Line num
    url = line_split[16] # URL
    name = url.split('/')[-1].replace('.jpg', '')

    xml_path = os.path.join(xml_dir, name + '.xml')
    if not os.path.exists(xml_path): continue

    tree = ET.parse(xml_path)
    objects = tree.findall('object')
    boxes = []
    for obj in objects:
        box = []

        bndbox = obj.find('bndbox')
        xmin = int(bndbox.find('xmin').text)
        ymin = int(bndbox.find('ymin').text)
        xmax = int(bndbox.find('xmax').text)
        ymax = int(bndbox.find('ymax').text)

        box.append(xmin)
        box.append(ymin)
        box.append(xmax)
        box.append(ymax)

        boxes.append(box)


    dicts[line_num] = boxes

    if i % 10000000 == 0: print("Progress", i, "/ 100M")


fw = open('image_id_list.json','w')
json.dump(dicts,fw)

print('Finish!!')
print(len(dicts), 'images')