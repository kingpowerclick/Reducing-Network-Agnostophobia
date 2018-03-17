import numpy as np
import cPickle
import csv
import gzip
import struct
import cv2
from sklearn.model_selection import train_test_split
from keras.utils.np_utils import to_categorical

# https://sashat.me/2017/01/11/list-of-20-simple-distinct-colors/
colors = np.array([
    [230, 25, 75],
    [60, 180, 75],
    [255, 225, 25],
    [0, 130, 200],
    [245, 130, 48],
    [145, 30, 180],
    [70, 240, 240],
    [240, 50, 230],
    [210, 245, 60],
    [250, 190, 190]
]).astype(np.float)
colors=colors/255.

def read_labels(fname):
    with gzip.open(fname, 'rb') as f:
        # reads 2 big-ending integers
        magic_nr, n_examples = struct.unpack(">II", f.read(8))
        # reads the rest, using an uint8 dataformat (endian-less)
        labels = np.fromstring(f.read(), dtype='uint8')
        return labels

def read_images(fname):
    with gzip.open(fname, 'rb') as f:
        # reads 4 big-ending integers
        magic_nr, n_examples, rows, cols = struct.unpack(">IIII", f.read(16))
        shape = (n_examples, rows*cols)
        # reads the rest, using an uint8 dataformat (endian-less)
        images = np.fromstring(f.read(), dtype='uint8').reshape(shape)
        return images

class mnist_data_prep:
    
    def __init__(self):

        images=read_images('/net/kato/datasets/MNIST/train-images-idx3-ubyte.gz')
        labels=read_labels('/net/kato/datasets/MNIST/train-labels-idx1-ubyte.gz')        
        images=images*(1./255.)
        images=images.reshape((images.shape[0],28,28,1))
        self.X_train, self.X_val, self.labels_train, self.labels_val = train_test_split(images, labels,train_size=0.8,test_size=0.2)
        
        images=read_images('/net/kato/datasets/MNIST/t10k-images-idx3-ubyte.gz')
        labels=read_labels('/net/kato/datasets/MNIST/t10k-labels-idx1-ubyte.gz')
        images=images*(1./255.)
        self.X_test=images.reshape((images.shape[0],28,28,1))
        self.labels_test=labels
        
        self.Y_train = to_categorical(self.labels_train,10)
        self.Y_val = to_categorical(self.labels_val,10)
        self.Y_test = to_categorical(self.labels_test,10)
    
class letters_prep:
        
    def __init__(self):
        images=read_images('/net/kato/datasets/MNIST_Letters/EMNIST_Binary_files/emnist-letters-train-images-idx3-ubyte.gz')
        labels=read_labels('/net/kato/datasets/MNIST_Letters/EMNIST_Binary_files/emnist-letters-train-labels-idx1-ubyte.gz')
        images=images*(1./255.)
        images=images.reshape((images.shape[0],28,28,1))
        self.X_train, self.X_val, self.Y_train, self.Y_val = train_test_split(images, labels,train_size=0.8,test_size=0.2)

        images=read_images('/net/kato/datasets/MNIST_Letters/EMNIST_Binary_files/emnist-letters-test-images-idx3-ubyte.gz')
        labels=read_labels('/net/kato/datasets/MNIST_Letters/EMNIST_Binary_files/emnist-letters-test-labels-idx1-ubyte.gz')
        images=images*(1./255.)
        self.X_test=images.reshape((images.shape[0],28,28,1))
        self.Y_test=labels
        
class cifar_prep:
    
    def __init__(self):
        cifar_data = cPickle.load(open('/net/kato/datasets/cifar-10-batches-py/data_batch_1', 'rb'))
        raw_images=cifar_data['data'].reshape(cifar_data['data'].shape[0],32,32,3, order='F')
        resized_images=[]
        for img in raw_images:
            gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            resized_images.append(cv2.resize(gray_img,(28,28),interpolation=cv2.INTER_CUBIC))
        resized_images=np.array(resized_images)[...,np.newaxis]
        self.images=resized_images*(1./255.)