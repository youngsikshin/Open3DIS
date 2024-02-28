# Open3DIS: Open-vocabulary 3D Instance Segmentation with 2D Mask Guidance

> **Abstract**: 
We introduce Open3DIS, a novel solution designed to tackle the problem of Open-Vocabulary Instance Segmentation within 3D scenes. Objects within 3D environments exhibit diverse shapes, scales, and colors, making precise instance-level identification a challenging task. Recent advancements in Open-Vocabulary scene understanding have made significant strides in this area by employing class-agnostic 3D instance proposal networks for object localization and learning queryable features for each 3D mask. While these methods produce high-quality instance proposals, they struggle with identifying small-scale and geometrically ambiguous objects. The key idea of our method is a new module that aggregates 2D instance masks across frames and maps them to geometrically coherent point cloud regions as high-quality object proposals addressing the above limitations. These are then combined with 3D class-agnostic instance proposals to include a wide range of objects in the real world. 
To validate our approach, we conducted experiments on three prominent datasets, including Scannet200, S3DIS, and Replica, demonstrating significant performance gains in segmenting objects with diverse categories over the state-of-the-art approaches. 

## Features :mega:
* State-of-the-art performance of Open-Vocabulary Instance Segmentation on ScanNet200, S3DIS, and Replica.
* Support Open-Vocabulary queries: affordances, materials, color, shape, etc.
* Reproducibility code for both ScanNet200, S3DIS, and Replica datasets.
* Demo application for scene visualization

# Installation guide

1\) Environment requirements

The following installation guide supposes ``python=3.8``, ``pytorch=1.12.1``, ``cuda=11.3``, ``torch-scatter-2.1.0+pt112cu113``, and ``spconv-cu113==2.1.25``. You may change them according to your system.

Create conda and install core packages:
```
conda create -n Open3DIS python=3.8
conda activate Open3DIS
conda install pytorch==1.12.1 torchvision==0.13.1 cudatoolkit=11.3 -c pytorch
pip3 install spconv-cu113==2.1.25
```

Install torch_scatter: the version must match your ``python`` version. It is recommended to visit [torch_scatter](https://data.pyg.org/whl/torch-1.12.1+cu113.html) and download the corresponding version.
In our case, we use:
```
pip install torch_scatter-2.1.0+pt112cu113-cp38-cp38-linux_x86_64.whl
```

General case, might lead to Segmentaion Core Dump:
```
pip install torch-scatter==2.0.9 -f https://data.pyg.org/whl/torch-1.12.1+cu113.html
```

2\) Install Detectron2:  or you can refer to this link for cloning the [source](https://detectron2.readthedocs.io/en/latest/tutorials/install.html):

```
python -m pip install 'git+https://github.com/facebookresearch/detectron2.git'
```

3\) Install [GroundedSAM](https://github.com/IDEA-Research/Grounded-Segment-Anything), we modified the models to work with ours Open3DIS, so install the repo locally is needed: 
```
cd GroundingDINO/
pip install -e .
cd ../
cd segment_anything
pip install -e .
cd ../
```

4\) Install additional libs for Segment Anything 3D and pointops:
```
cd SegmentAnything3D
pip install scikit-image opencv-python open3d imageio plyfile
cd libs/pointops
python setup.py install
cd ../../../
```

5\) Install [ISBNet](https://github.com/VinAIResearch/): 
```
cd ISBNet
pip install -r requirements.txt
# Install build requirement
sudo apt-get install libsparsehash-dev
# Setup PointNet operator for DyCo3D
cd isbnet/pointnet2
python3 setup.py bdist_wheel
cd ./dist
pip3 install <.whl>
cd ../../../
# Setup build environment
python3 setup.py build_ext develop
cd ../
```

6\) Finally, install other dependencies:
```
pip install -r requirements.txt
```

# Download pretrained foundation models

 Download the pretrained Grounding DINO and Segment Anything model:
```
mkdir -p pretrains/foundation_models
cd pretrains/foundation_models

wget https://dl.fbaipublicfiles.com/segment_anything/sam_vit_h_4b8939.pth
wget https://github.com/IDEA-Research/GroundingDINO/releases/download/v0.1.0-alpha/groundingdino_swint_ogc.pth
```


# Data Preparation
1\) Create data folder:
```
mkdir -p data/ScannetV2
mkdir -p data/Scannet200
mkdir -p data/replica
mkdir -p data/S3DIS
```

2\) Prepare the 2D data of ScanNet. We follow [OpenScene](https://github.com/pengsongyou/openscene) to process the RGB-D video sequences of ScanNet dataset. Put the data at `data/ScannetV2/ScannetV2_2D_5interval`.

3\) Prepare the ground-truth instance masks of ScanNet200. We follow [ISBNet](https://github.com/VinAIResearch/ISBNet) to process the ground-truth instance masks and superpoints of ScanNet200. Put the data at `data/Scannet200/`.

updating...

```
Open3DIS <-- (you are here)
├── data
│   ├── ScannetV2
│   │   ├── ScannetV2_2D_5interval
│   │   │    ├── train
│   │   │    ├── val
│   │   │    |    scene0011_00
│   │   │    |    ├──color
│   │   │    |    ├──depth
│   │   │    |    ├──pose
│   │   │    |    |  instrinsic.txt (image intrinsic)
│   │   │    |    .... scenes
│   │   │    | intrinsic_depth.txt (depth intrinsic)
│   │   │    ├── original_ply_files # the _vh_clean_2.ply file from Scannet raw data.
│   ├── Scannet200
|   |   ├── train 
│   │   ├── val
│   │   ├── test
│   │   ├── superpoints
│   │   ├── isbnet_clsagnostic_scannet200 # class agnostic 3D proposals
│   │   ├── dc_feat_scannet200 # 3D deep feature map from backbone of 3D proposals network
├── pretrains
|   ├── foundation_models
|   |   ├── groundingdino_swint_ogc
|   |   ├── sam_vit_h_4b8939.pth
```

# Run the code

1\) Extract class-agnostic 3D proposals and 3D feature map from ISBNet:

```
cd ISBNet/
python3 tools/test.py configs/scannet200/isbnet_scannet200.yaml pretrains/scannet200/head_scannetv2_200_val.pth
```

2\) Extract 2D masks from RGB-D sequences:

```
sh scripts/grounding_2d.sh
```

3\) Generate open-vocab 3D instances:

```
sh scripts/generate_3d_inst.sh
```

4\) Run interactive visualization (required Open3D):

```
cd visualization
python3 vis_gui.py
```


# Some important modules

1\) The 2D segmenter: see `tools/grounding_2d.py`

2\) The 3D segmenter: see `ISBNet/isbnet/model/isbnet.py`

3\) The 2D-guide-3D Instance Proposal Module: see `open3dis/src/clustering/clustering.py` 

4\) The Pointwise Feature Extraction: see `tools/refine_grouding_feat.py`

5\) The overall process of generating 3D instances from both 2D proposals and 3D proposals: see `tools/generate_3d_inst.py`