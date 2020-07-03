# Fashion Culture DataBase (FCDB)
## Updates
* 2020/03/26: 事前学習モデルの重みを公開
* 2020/03/04: レポジトリの公開
* 2019/11/08: レポジトリの作成

## Summary
FCDBは以下の文献に従い，構成されております．  
[Kaori Abe, Teppei Suzuki, Shunya Ueta, Akio Nakamura, Yutaka Satoh, Hirokatsu Kataoka  
"Changing Fashion Cultures," arXiv pre-print:1703.07920, 2017.][1]

[Hirokatsu Kataoka, Kaori Abe, Munetaka Minoguchi, Akio Nakamura and Yutaka Satoh  
"Ten-million-order Human Database for World-wide Fashion Culture Analysis,"  
Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition Workshop (CVPRW), 2019.][2]  

本レポジトリはFCDBを構成するためのコードやbounding box（bbox; 検出枠）の情報を含みます。FCDBのオリジナル画像はYFCC100Mをベースとして構成しているため、画像やFlickrに含まれるメタ情報などのデータを公開することはできません。従って、著者らで生成したbboxのデータや、FCDBの構築に必要なコードのみを公開し、YFCC100Mと合わせて使用して頂くことでFCDBを再現することが可能です。
本レポジトリで共有するものは以下の通りです。
* FCDB構築に必要な画像IDおよびbboxの一覧
* 3種の形式でのFCDBの構築  
  * 画像のみ収集 (16都市ごとにディレクトリを形成)
  * Pascal VOC形式 (人物検出用)
  * MS COCO形式 (人物検出用)

また、FCDBを大規模事前学習用データセットとした人物検出タスクへの応用についても検証しております。論文はarXiv.orgで公開中です。  

[Munetaka Minoguchi, Ken Okayama, Yutaka Satoh, Hirokatsu Kataoka  
“Weakly Supervised Dataset Collection for Robust Person Detection”  
arXiv pre-print:2003.12263, 2020.][8]

## Citation
文献での掲載は以下の内容でお願いします。  

```
@inproceedings{KataokaCVPRW2019_FCDB,
  author={Hirokatsu Kataoka and Kaori Abe and Munetaka Minoguchi and Akio Nakamura and Yutaka Satoh},
  title={Ten-million-order Human Database for World-wide Fashion Culture Analysis},
  booktitle={Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition Workshop (CVPRW)},
  year={2019},
}

@inproceedings{Minoguchi_WSPD,
  author={Munetaka Minoguchi and Ken Okayama and Yutaka Satoh and Hirokatsu Kataoka},
  title={Weakly Supervised Dataset Collection for Robust Person Detection},
  booktitle={arXiv pre-print:2003.12263},
  year={2020},
}
```

## Requirements
* python 3
* numpy, xml, json, argparse
* 400 GB程度の空き容量

## Preparation
FCDBはYFCC100Mを基に構築した画像データベースであるため、あらかじめYFCC100Mをダウンロードする必要があります。また、FCDB使用に関するライセンスやその他の権利はYFCC100Mに帰属します。  
YFCC100Mのダウンロード方法については[YFCC100M][3]をご確認ください。  
必要なデータはAmazon s3から取得することができる`yfcc100m_dataset`です。

## Download
* ImageIDとbbox
  FCDB構築に必要な画像IDとbboxが対になったデータはこちらの[フォーム][4]にご記入・ご投稿頂いた後、確認の上で入手可能なリンクをご案内致します。

* 事前学習モデルの重み
  [M2Det][5]と[SSD][6]によってFCDBを学習した重みを提供します。ハイパーパラメータなどのconfigurationは、各実装のレポジトリのデフォルトに従います。  
  ダウンロードリンクは[こちら][7]です。

## Running the code
構築するデータ形式ごとに実行するコードが異なります。  
※データのパス、保存先の引数を適切に設定してください。

#### 16 citys Directory
ディレクトリを都市ごとに分割してFCDBを構築します。FCDBは16都市に分割されます。  
```
python ImageFolder.py --yfcc='./yfcc100m_dataset' \
                        --id_json='./image_id_list.json' \
                        --save_dir='./FCDBv2'
```

#### Pascal VOC (for Person Detection)
物体検出で使用されるPascal VOC形式でFCDBを構築します。画像IDとbboxを対応付ける処理です。
```
python VocFormat.py --yfcc='./yfcc100m_dataset' \
                        --id_json='./image_id_list.json' \
                        --save_dir='./FCDBv2'
```

#### MS COCO (for Person Detection)
物体検出で使用されるMS COCO形式でFCDBを構築します。画像IDとbboxを対応付ける処理です。  
```
python CocoFormat.py --yfcc='./yfcc100m_dataset' \
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
[8]:https://arxiv.org/abs/2003.12263
