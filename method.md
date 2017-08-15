#### How I do this 

#### Experiment Environment

Impletmented by [UC Berkeley Caffe](http://caffe.berkeleyvision.org/), [Github Page](https://github.com/BVLC/caffe/).

Pre-trained models including CaffeNet, GoogLeNet, AlexNet, ResNet-50(trained on [ImageNet](http://www.image-net.org/)). Runing on a machine with two Xeon E5-2665 CPU and 32 GB RAM,equipped with an Nvidia GeForce GTX 970 GPU.

#### Data preparation

Current fairly effective CNN model can not accept medical images directly, so I have converted the dataset to [HDF5](https://support.hdfgroup.org/HDF5/) file format with image data and its responding concrete age label. Detailly, it's neccessary to rescale the image to the size which the network can accept, and meanwhile it will reduce the computation pressure.

Data augmentation including rotating(旋转), image crop(裁剪), data shuffle(数据打乱) and so on.

Mean value normalization(均值归一化，这篇文章也用到一样的方法，使样本均值为0) hava the image data to own an 0 mean value to reduce computation pressure and converge easier.

To hava the pre-trained model effective, copy the 2-dimension data to another 2 2-dimension, so it becomes an color image(也就是数据是二维的，通过一个复制的过程，将这维的数据复制到另外两维，生成一个pre-trained的模型能接受的三通道彩色图片)

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

Lastly , set the SoftMax loss layer to euclidean loss layer.

![](http://omoitwcai.bkt.clouddn.com/2017-08-15-gif.gif)



##### middle layers output dimensions
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