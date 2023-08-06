# -*- coding: utf-8 -*-
"""
Created on Thu Jul 25 15:57:27 2019

@author: dyanni
"""

from VAEOversampler import VAEOversampler
from keras.datasets import mnist
import numpy as np
from matplotlib import pyplot as plt


if __name__=='__main__':
    (x_train, y_train), (x_test, y_test) = mnist.load_data()
    image_size = x_train.shape[1]
    original_dim = image_size * image_size
    x_train = np.reshape(x_train, [-1, original_dim])
    x_test = np.reshape(x_test, [-1, original_dim])
    x_train = x_train.astype('float32') / 255
    x_test = x_test.astype('float32') / 255

    vae_sampler = VAEOversampler(epochs=50,
                                 intermediate_dim=512,
                                 batch_size=64,
                                 rescale=False)
    Xres,yres = vae_sampler.fit_resample(x_train,
                                         y_train,
                                         validation_data=[x_test,y_test])
    results = Xres[:-11:-1].reshape((10,28,28))
    random_draw = x_train[np.random.choice(range(x_train.shape[0]),10)]\
    .reshape(10,28,28)
    with plt.style.context('dark_background'):
        fig,axes = plt.subplots(nrows=2,ncols=10,figsize=(20,5))
        for i in range(10):
            axes[0][i].imshow(results[i],cmap=plt.cm.bone)
            axes[1][i].imshow(random_draw[i],cmap=plt.cm.bone)
        axes[0][4].set_xlabel("minority generated")
        axes[1][4].set_xlabel("random draw from dataset")
    