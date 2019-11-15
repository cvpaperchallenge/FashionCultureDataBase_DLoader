# FashionCultureDataBase v2 Downloader
## Updates
* 2019/11/08 レポジトリの作成

## Summary
FCDBおよびFCDBv2v2は以下の文献に従い，構成されております．  
[Kaori Abe, Teppei Suzuki, Shunya Ueta, Akio Nakamura, Yutaka Satoh, Hirokatsu Kataoka  
"Changing Fashion Cultures,"  
, 2017.][1]

[Hirokatsu Kataoka, Kaori Abe, Munetaka Minoguchi, Akio Nakamura and Yutaka Satoh  
"Ten-million-order Human Database for World-wide Fashion Culture Analysis,"  
Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition Workshop (CVPRW), 2019.][2]  

本レポジトリはFCDBv2を公開するためのコードやバウンディングボックスの情報を含みます。FCDBv2はYFCC100Mを基に構成しているため、画像やメタ情報などのデータを公開することはできません。しかし、著者らで生成したバウンディングボックスのデータや、FCDBv2の構築に必要なコードは公開することができるので、YFCC100Mと合わせて使用することで構築することが可能です。
本レポジトリで共有するものは以下の通りです。  
* FCDBv2構築に必要な画像およびバウンディングボックスの一覧
* 3種の形式でのFCDBv2の構築  
  * 画像みの収集 (16都市ごとにディレクトリを形成)
  * Pascal VOC形式 (人物検出用)
  * MS COCO形式 (人物検出用)

## Citation
文献での掲載は以下の内容でお願いします。  

```@inproceedings{hara3dcnns,
  author={Hirokatsu Kataoka, Kaori Abe, Munetaka Minoguchi, Akio Nakamura and Yutaka Satoh},
  title={Ten-million-order Human Database for World-wide Fashion Culture Analysis},
  booktitle={Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition Workshop (CVPRW)},
  pages={},
  year={2019},
}
```

## Requirements
* python 3
* その他のpythonライブラリ
* 400 GB程度の空き容量

## Preparation
FCDBv2はYFCC100Mを基に構築した画像データベースであるため、あらかじめYFCC100Mをダウンロードする必要があります。また、FCDBv2使用に関するライセンスやその他の権利はYFCC100Mに帰属します。  
YFCC100Mのダウンロード方法については[YFCC100M][3]にてご確認ください。  
必要なデータはAmazon s3から取得することができる`yfcc100m_dataset`です。

FCDBv2構築に必要な、画像IDとバウンディングボックスが対になったデータ`image_id_list.json`は以下からダウンロードすることができます。  
* [Download: Google Drive][4]

## Running the code
構築するデータ形式ごとに実行するコードが異なります。  
※データのパス、保存先の引数を適切に設定してください。

#### 16 citys Directory
Classificationなどのタスクに有効な16都市ごとのディレクトリ構成で、FCDBv2を構築します。  
```
python dir_16citys.py --yfcc='./yfcc100m_dataset' \
                        --id_dict='./image_id_list.json' \
                        --save_dir='./FCDBv2'
```

#### Pascal VOC (for Person Detection)
人物検出器の事前学習などに有効なPascal VOC形式で、FCDBv2を構築します。  
```
python voc_fomat.py --yfcc='./yfcc100m_dataset' \
                        --id_dict='./image_id_list.json' \
                        --save_dir='./FCDBv2'
```

#### MS COCO (for Person Detection)
人物検出器の事前学習などに有効なMS COCO形式で、FCDBv2を構築します。  
```
python coco_fomat.py --yfcc='./yfcc100m_dataset' \
                        --id_dict='./image_id_list.json' \
                        --save_dir='./FCDBv2'
```

## Copywrite
国立開発研究法人産業技術総合研究所




[1]:https://arxiv.org/abs/1703.07920
[2]:https://arxiv.org/abs/1703.07920
[3]:http://projects.dfki.uni-kl.de/yfcc100m/
[4]:http://projects.dfki.uni-kl.de/yfcc100m/