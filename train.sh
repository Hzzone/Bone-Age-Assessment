PATH="$PATH:/usr/local/cuda/bin" &&
export PATH &&
LD_LIBRARY_PATH="/usr/local/cuda/lib64" &&
export LD_LIBRARY_PATH &&
cd /home/bw/DeepLearning/female_regression/AlexNet &&
echo "AlexNet start!" &&
~/code/caffe/build/tools/caffe train --weights bvlc_alexnet.caffemodel --solver solver.prototxt --gpu 0 >> train.log &&
cd /home/bw/DeepLearning/female_regression/CaffeNet &&
echo "CaffeNet start!" &&
~/code/caffe/build/tools/caffe train --weights bvlc_reference_caffenet.caffemodel --solver solver.prototxt --gpu 0 >> train.log &&
cd /home/bw/DeepLearning/female_regression/GoogLeNet &&
echo "GoogLeNet start!" &&
~/code/caffe/build/tools/caffe train --weights bvlc_googlenet.caffemodel --solver solver.prototxt --gpu 0 >> train.log &&
cd /home/bw/DeepLearning/female_regression/ResNet50 &&
echo "ResNet50 start!" &&
~/code/caffe/build/tools/caffe train --weights resnet50_cvgj_iter_320000.caffemodel --solver train.solver --gpu 0 >> train.log 

