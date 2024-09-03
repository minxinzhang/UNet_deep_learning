# 个人课程项目介绍
复刻了UNet的论文代码（见`Unet.pdf`)。对细胞影像原始图片进行细胞核的识别工作，训练数据来自https://bbbc.broadinstitute.org/BBBC039 。
整个程序对算力要求及其高，建议和我一样申请一个谷歌服务器上的GPU跑训练。每个新谷歌账户有500美元的免费使用额度，可以在GCP上租借最便宜的英伟达T4节约时间（整个过程1小时左右）。
原始源代码TensorFlow, Keras, SkiImage API已过期，我的工作是调用了新的API（所有的Python文件），修改训练参数如原始图片的分割大小，训练数据和验证数据的比例。特别地，针对原始数据量过小的问题，进行了数据增强，并对比新数据集和老数据集的模型训练效果。具体报告请阅读`report.pdf`。

# SOURCE CODE
Most parts of the source code is from https://bbbc.broadinstitute.org/BBBC039
Modifications were made to call the lastest APIs from TensorFlow, Keras and Ski image.

# Dependency
seaborn                       0.12.2
scikit-image                  0.20.0
pandas                        2.1.2
numpy                         1.24.3
keras                         2.14.0
tensorflow                    2.14.0
tqdm                          4.65.0
glob2                         0.7

# How to use
## reset to the default[optional]
1. `rm -r data` to reset 
## prepare for experiments
2. `vim config.py` and customize your own parameters
3. `python config.py` to configure. Note that enable data augmentation is time consuming
4. `python download_data.py` to get the BBBC039 dataset. Check if you have got `raw_images` etc after this
5. `python preprocess.py` to process raw data and raw annotation.

## conduct an experiment manually
1. `python train.py` to train a model
2. `python prediction.py` to use the model to predict based on the validation set
3. `python evaluate.py` to measure the performance of the model
## conduct another experiment
1. modify the configuration and run `python config.py` again
2. repeat the previous train predict and evaluate procedure.
## replicate my preset experiment
after the experiment preparation, simply run `python compare.py`
It is computational heavy. You can check my experiment process in `output.log`
The summary of the experiment result is in the `data/experiments/impact*` folder.

