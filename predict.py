import sys
sys.path.insert(0, "/home/bw/code/caffe/python")
import caffe

# predict the age from a new dicom file by a trained caffemodel and deploy file
def predict(caffemodel, deploy, dicom):
    caffe.set_mode_gpu()
    net = caffe.Net(deploy, caffemodel, caffe.TEST)
    net.blobs['data'].reshape(1, 1, *DATA_SIZE)

    filename = sys.argv[1]

    with open(filename, 'r') as f:
        flag = -1
        for line in f.readlines():
            flag += 1

            line_data = numpy.zeros((1, 106), dtype=numpy.float32)
            for i in range(106):
                line_data[0][i] = float(line.split('\t')[i])
            print
            line_data.shape
            labels = float(line.split('\t')[-1].split('\n')[0])
            net.blobs['data'].data[...] = line_data

            output = net.forward()
            score = output['ip2'][0][0]

            print('The predicted score is {},the true is {}'.format(score, labels))
            if flag == 10:
                break
