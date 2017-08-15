#### How I do this 

#### Experiment Environment

Impletmented by [UC Berkeley Caffe](http://caffe.berkeleyvision.org/), [Github Page](https://github.com/BVLC/caffe/).

Pre-trained models including CaffeNet, GoogLeNet, AlexNet, ResNet-50(trained on [ImageNet](http://www.image-net.org/)). Runing on a machine with two Xeon E5-2665 CPU and 32 GB RAM,equipped with an Nvidia GeForce GTX 970 GPU.

#### Data preparation

Current fairly effective CNN model can not accept medical images directly, so I have converted the dataset to [HDF5](https://support.hdfgroup.org/HDF5/) file format with image data and its responding concrete age label. Detailly, it's neccessary to rescale the image to the size which the network can accept, and meanwhile it will reduce the computation pressure.

Data augmentation including rotating(旋转), image crop(裁剪), data shuffle(数据打乱) and so on.

Mean value normalization(均值归一化，这篇文章也用到一样的方法，使样本均值为0) hava the image data to own an 0 mean value to reduce computation pressure and converge easier.

To hava the pre-trained model effective, copy the 2-dimension data to another 2 2-dimension, so it becomes an color image(也就是数据是二维的，通过一个复制的过程，将这维的数据复制到另外两维，生成一个pre-trained的模型能接受的三通道彩色图片)

Randomly taking 1/10 from dataset to validate the performance of the network. For example, I have 1000 male samples in total, so I should take 100 of them to test.

#### Network Preparation

To sovle the regression problem, change the network input data layer to HDF5Data layer(normally data layer only accept lmdb or leveldb file which don't support float label).

(代码只是为了展示...)

```
layer {
  name: "data"
  type: "HDF5Data"
  top: "data"
  top: "label"
  include {
    phase: TRAIN
  }
  hdf5_data_param {
    source: "./train_h5.txt"
    batch_size: 120
  }
}
```

And set the one iteration batch size to the number which the GPU can afford(such as CaffeNet with a 120 batch size).

Detailly, set the last fully connected layer also called classifer to has only one neuron since we only want the network output a predicted bone age.(最后一个全连接层,也叫分类器，这一层输出结果，调整成一个，输出的这个值就是结果)

Lastly , set the SoftMax loss layer to euclidean loss layer. Below is the loss function equation:

<img src="http://omoitwcai.bkt.clouddn.com/2017-08-15-gif.gif" style="clear: both; 
display: block; 
margin:auto;" />

#### Comparation Between Different Pre-trained Model

I have fine-tuned on 4 different network which has already been proved to be effective, including CaffeNet, AlexNet, GoogLeNet and ResNet-50. For female or male's performance details, see the [result folder](https://github.com/Hzzone/Bone-Age-Assessment/tree/master/result). I have measured the performance by test the accuracy on validation dataset(for example, 五十个验证集，正确的有48个，那准确度就有96%).

For every pre-trained model, I have 10000 iterations each and snapshoot the weight every 500 iteration. And then sorted the different weights by accuracy.

Taking CaffeNet for Example:

```
/home/bw/DeepLearning/male_regression/Caffenet/nodiv256/caffenet_train_iter_2000.caffemodel 0.970588
/home/bw/DeepLearning/male_regression/Caffenet/nodiv256/caffenet_train_iter_1500.caffemodel 0.970588
/home/bw/DeepLearning/male_regression/Caffenet/nodiv256/caffenet_train_iter_500.caffemodel 0.970588
/home/bw/DeepLearning/male_regression/Caffenet/nodiv256/caffenet_train_iter_5000.caffemodel 0.955882
/home/bw/DeepLearning/male_regression/Caffenet/nodiv256/caffenet_train_iter_2500.caffemodel 0.955882
/home/bw/DeepLearning/male_regression/Caffenet/nodiv256/caffenet_train_iter_5500.caffemodel 0.955882
/home/bw/DeepLearning/male_regression/Caffenet/nodiv256/caffenet_train_iter_8500.caffemodel 0.941176
/home/bw/DeepLearning/male_regression/Caffenet/nodiv256/caffenet_train_iter_3500.caffemodel 0.941176
/home/bw/DeepLearning/male_regression/Caffenet/nodiv256/caffenet_train_iter_3000.caffemodel 0.941176
/home/bw/DeepLearning/male_regression/Caffenet/nodiv256/caffenet_train_iter_6500.caffemodel 0.941176
/home/bw/DeepLearning/male_regression/Caffenet/nodiv256/caffenet_train_iter_9500.caffemodel 0.941176
/home/bw/DeepLearning/male_regression/Caffenet/nodiv256/caffenet_train_iter_7500.caffemodel 0.941176
/home/bw/DeepLearning/male_regression/Caffenet/nodiv256/caffenet_train_iter_4000.caffemodel 0.941176
/home/bw/DeepLearning/male_regression/Caffenet/nodiv256/caffenet_train_iter_4500.caffemodel 0.941176
/home/bw/DeepLearning/male_regression/Caffenet/nodiv256/caffenet_train_iter_10000.caffemodel 0.941176
/home/bw/DeepLearning/male_regression/Caffenet/nodiv256/caffenet_train_iter_8000.caffemodel 0.941176
/home/bw/DeepLearning/male_regression/Caffenet/nodiv256/caffenet_train_iter_7000.caffemodel 0.941176
/home/bw/DeepLearning/male_regression/Caffenet/nodiv256/caffenet_train_iter_6000.caffemodel 0.941176
/home/bw/DeepLearning/male_regression/Caffenet/nodiv256/caffenet_train_iter_9000.caffemodel 0.941176
/home/bw/DeepLearning/male_regression/Caffenet/nodiv256/caffenet_train_iter_1000.caffemodel 0.882353
```

It is proved that CaffeNet has the most effective result on this problem.

#### Network visualization

<img src="http://omoitwcai.bkt.clouddn.com/2017-08-15-%E4%B8%8B%E8%BD%BD.png" style="clear: both; 
display: block; 
margin:auto;" />
(更容易理解的:)
<img src="http://omoitwcai.bkt.clouddn.com/2017-08-15-FireShot%20Capture%202%20-%20Netscope%20-%20http___ethereon.github.io_netscope_-_editor.png" style="clear: both; 
display: block; 
margin:auto;" />

##### middle layers output dimensions(中间层输出的维数)

The param shapes typically have the form `(output_channels, input_channels, filter_height, filter_width)` (for the weights) and the 1-dimensional shape `(output_channels,)` (for the biases).

```angular2html
conv1	(96, 3, 11, 11)		(96,)
conv2	(256, 48, 5, 5)		(256,)
conv3	(384, 256, 3, 3)	(384,)
conv4	(384, 192, 3, 3)	(384,)
conv5	(256, 192, 3, 3)	(256,)
fc6	    (4096, 9216)		(4096,)
fc7	    (4096, 4096)		(4096,)
my-fc8	(1, 4096)		    (1,)
```
##### feature map

For exmaple:

one of conv1 output:

<img src="http://omoitwcai.bkt.clouddn.com/2017-08-15-19.jpg" style="clear: both; 
display: block; 
margin:auto;" />

Pictures below show the output values of fully connected layer and the histogram of the positive values

fc6:

<img src="http://omoitwcai.bkt.clouddn.com/2017-08-15-output.png" style="clear: both; 
display: block; 
margin:auto;" />

fc7:

<img src="http://omoitwcai.bkt.clouddn.com/2017-08-15-output-1.png" style="clear: both; 
display: block; 
margin:auto;" />

fc8 output the result.

#### Results

- male: 0.970588

- female: 0.956522

  Caffemodel and deploy file is on [Github Page](https://github.com/Hzzone/Bone-Age-Assessment), just test it on your own data.