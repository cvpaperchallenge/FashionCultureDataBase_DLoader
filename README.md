# Fashion Culture DataBase (FCDB)
## Issues
* Mar. 4, 2020: YFCC100M, the source dataset of Fashion Culture DataBase currently may have an issue on downloading.
Please check updates of [this page][3].

## Updates
* Mar. 26, 2020: Pre-train weights are published
* Mar. 4, 2020: Repository is published
* Nov. 8, 2019: Repository creation

## Summary
FCDB has been constructed based on the following papers.

[Kaori Abe, Teppei Suzuki, Shunya Ueta, Akio Nakamura, Yutaka Satoh, Hirokatsu Kataoka  
"Changing Fashion Cultures," arXiv pre-print:1703.07920, 2017.][1]

[Hirokatsu Kataoka, Kaori Abe, Munetaka Minoguchi, Akio Nakamura and Yutaka Satoh  
"Ten-million-order Human Database for World-wide Fashion Culture Analysis,"  
Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition Workshop (CVPRW), 2019.][2]  

The repository provides codes and bounding boxes (bboxes) in order to construct FCDB which is based on YFCC100M dataset. Please note that we are NOT serving original images and meta information including YFCC100M dataset. Therefore, please download YFCC100M images yourself by following the Yahoo's instruction. We are sharing only person bboxes which are corresponding to YFCC100M images. The detailed sharing files are shown below.
* Image identification number (Image ID) and bboxes on FCDB
* 3 types of dataset representation
  * Images divided into 16 directories
  * Pascal VOC format (for person detection)
  * MS COCO format (for person detection)

## Citation
If you use the dataset or codes, please cite the following:

```
@inproceedings{KataokaCVPRW2019_FCDB,
  author={Hirokatsu Kataoka, Kaori Abe, Munetaka Minoguchi, Akio Nakamura and Yutaka Satoh},
  title={Ten-million-order Human Database for World-wide Fashion Culture Analysis},
  booktitle={Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition Workshop (CVPRW)},
  year={2019},
}

@inproceedings{Minoguchi_WSPD,
  author={Munetaka Minoguchi, Ken Okayama, Yutaka Satoh, Hirokatsu Kataoka},
  title={Weakly Supervised Dataset Collection for Robust Person Detection},
  booktitle={arXiv pre-print:2003.12263},
  year={2020},
}
```

## Requirements
* python 3
* numpy, xml, json, argparse
* 400 GB vacant space in your computer

## Preparation
A user must download in advance, due to FCDB has constructed based on YFCC100M. The rights including copyright and license are belonged to YFCC100M. Please refer to the description of YFCC100M [YFCC100M][3].
The required data can be available on `yfcc100m_dataset` on Amazon s3.

## Download
* Image ID and bboxes  
  Please fill out the [form][4] to obtain a file which contains image ID and bboxes. After our confirmation, we will send an email to get the file.

* Pre-train weights  
  It shares the trained weights of [M2Det][5] and [SSD][6] which are trained FCDB. The configuration of each detector follows the default settings of each original repository.  
  Download link is [here][7].


## Running the code
We provide three types of dataset representation. Please see the following instruction what you want. Please properly set a directory path in your environment.

#### 16 cities
FCDB is divided into 16 directories. The directory is corresponding at each city.
```
python ImageFolder.py --yfcc='./yfcc100m_dataset' \
                        --id_json='./image_id_list.json' \
                        --save_dir='./FCDBv2'
```

#### Pascal VOC (for Person Detection)
FCDB is transformed by Pascal VOC form which is used in object detection. The image ID and bbox are paired.
```
python VocFomat.py --yfcc='./yfcc100m_dataset' \
                        --id_json='./image_id_list.json' \
                        --save_dir='./FCDBv2'
```

#### MS COCO (for Person Detection)
FCDB is transformed by MS COCO form which is used in object detection. The image ID and bbox are paired.  
```
python CocoFomat.py --yfcc='./yfcc100m_dataset' \
                        --id_json='./image_id_list.json' \
                        --save_dir='./FCDBv2'
```


[1]:https://arxiv.org/abs/1703.07920
[2]:http://openaccess.thecvf.com/content_CVPRW_2019/html/FFSS-USAD/Kataoka_Ten-Million-Order_Human_Database_for_World-Wide_Fashion_Culture_Analysis_CVPRW_2019_paper.html
[3]:http://projects.dfki.uni-kl.de/yfcc100m/
[4]:https://forms.gle/ewTpFi6iYsnrairK6
[5]:https://github.com/qijiezhao/M2Det
[6]:https://github.com/amdegroot/ssd.pytorch
[7]:https://drive.google.com/drive/folders/1iSTxdASUS8Kz2I-v7Q9xIY7MDMovF6uR?usp=sharing
