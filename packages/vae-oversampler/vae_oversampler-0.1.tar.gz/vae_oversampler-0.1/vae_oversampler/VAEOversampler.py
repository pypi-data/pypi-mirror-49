from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from keras.layers import Lambda, Input, Dense
from keras.models import Model
from keras.losses import mse
from keras import backend as K
from sklearn.preprocessing import StandardScaler as SS
import numpy as np


#%%
class VAEOversampler: 

    def __init__(self,epochs=10,intermediate_dim=12,
                 weights=None, batch_size=64,
                 latent_dim=1, minority_class_id=1,
                 rescale=False, verbose = True):
        self.epochs=epochs
        self.batch_size=batch_size
        self.intermediate_dim=intermediate_dim
        self.weights=weights
        self.latent_dim=latent_dim
        self.minority_class_id=minority_class_id
        self.rescale = rescale
        self.verbose = verbose
        
    def sampling(self, args):
        """Reparameterization trick by sampling fr an isotropic unit Gaussian.
    
        # Arguments
            args (tensor): mean and log of variance of Q(z|X)
    
        # Returns
            z (tensor): sampled latent vector
        """
    
        z_mean, z_log_var = args
        batch = K.shape(z_mean)[0]
        dim = K.int_shape(z_mean)[1]
        # by default, random_normal has mean=0 and std=1.0
        epsilon = K.random_normal(shape=(batch, dim))
        return z_mean + K.exp(0.5 * z_log_var) * epsilon
    
    def build_train(self, x_train, x_test = None,
                                *args,**kwargs):
        """ builds a variational autoencoder using Keras
            and then compiles and trains it
        
        #Arguments
            x_train: array like, shape == (num_samples, num_features)
            x_test: optional validation data
            
        #Returns
            none.
            sets self.vae, self.encoder, and self.decoder
        """
        
        original_dim = x_train.shape[1]
        input_shape = (original_dim, )
        inputs = Input(shape=input_shape, name='encoder_input')
        x = Dense(self.intermediate_dim, activation='relu')(inputs)
        z_mean = Dense(self.latent_dim, name='z_mean')(x)
        z_log_var = Dense(self.latent_dim, name='z_log_var')(x)
        z = Lambda(self.sampling, output_shape=(self.latent_dim,), name='z')([z_mean, z_log_var])
        encoder = Model(inputs, [z_mean, z_log_var, z], name='encoder')
        if self.verbose:
            encoder.summary()
        latent_inputs = Input(shape=(self.latent_dim,), name='z_sampling')
        x = Dense(self.intermediate_dim, activation='relu')(latent_inputs)
        outputs = Dense(original_dim, activation='sigmoid')(x)
        decoder = Model(latent_inputs, outputs, name='decoder')
        if self.verbose:
            decoder.summary()

        # instantiate VAE model
        outputs = decoder(encoder(inputs)[2])
        self.vae = Model(inputs, outputs, name='vae_mlp')
        reconstruction_loss = mse(inputs, outputs)
        reconstruction_loss *= original_dim
        kl_loss = 1 + z_log_var - K.square(z_mean) - K.exp(z_log_var)
        kl_loss = K.sum(kl_loss, axis=-1)
        kl_loss *= -0.5
        vae_loss = K.mean(reconstruction_loss + kl_loss)
        self.vae.add_loss(vae_loss)
        self.vae.compile(optimizer='adam')
        self.vae.summary()
        if self.weights:
            self.vae.load_weights(self.weights)
        else:
            # train the autoencoder
            try:
                self.vae.fit(x_train,
                        epochs=self.epochs,
                        batch_size=self.batch_size,
                        validation_data=(x_test, None),
                        verbose = self.verbose)
            except:
                self.vae.fit(x_train,
                    epochs=self.epochs,
                    batch_size=self.batch_size,
                    verbose = self.verbose)
            self.vae.save_weights('vae.h5')
        self.encoder = encoder
        self.decoder = decoder
        return
        
    def fit(self, Xtrain, ytrain, validation_data=None, **vae_kwargs):
        """ fits a standard scaler to the training data
        then trains a variational autoencoder on the training data
        """
        self.ss = SS()
        self.ss.fit(Xtrain[ytrain==self.minority_class_id])
        if validation_data is not None:
            Xtest,ytest = validation_data
            self.variational_autoencoder(self.ss.transform(Xtrain[ytrain==self.minority_class_id]),
             x_test = self.ss.transform(Xtest[ytest==self.minority_class_id]),**vae_kwargs)
        else:
            self.variational_autoencoder(self.ss.transform(Xtrain[ytrain==self.minority_class_id]),**vae_kwargs)
        return
    
    def fit_resample(self,Xtrain,ytrain,validation_data=None,**vae_kwargs):
        """ fits a standard scaler to the training data
        then trains a variational autoencoder on the training data
        finally returns balanced resampled data
        """
        if validation_data is not None:
            Xtest,ytest = validation_data
        num_samples_to_generate = max(Xtrain[ytrain != self.minority_class_id].shape[0]\
                                      - Xtrain[ytrain ==self.minority_class_id].shape[0],100)
        if self.rescale:
            self.ss = SS()
            self.ss.fit(Xtrain[ytrain==self.minority_class_id])
            X = self.ss.transform(Xtrain[ytrain==self.minority_class_id])
            if validation_data is not None:
                x_test = self.ss.transform(Xtest[ytest==self.minority_class_id])
        else:
            X = Xtrain[ytrain==self.minority_class_id]
            if validation_data is not None:
                x_test = Xtest[ytest==self.minority_class_id]
        if validation_data is not None:
            self.build_train(X,x_test = x_test,**vae_kwargs)
        else:
            self.build_train(X,**vae_kwargs)
        z_sample = np.random.normal(0,1,num_samples_to_generate)
        outputs = self.decoder.predict(z_sample)
        if self.rescale:
            oversampled_X = self.ss.inverse_transform(outputs)
        else:
            oversampled_X = outputs
        oversampled_y = np.ones(num_samples_to_generate)*self.minority_class_id
        X_all = np.concatenate((Xtrain,oversampled_X))
        y_all = np.concatenate((ytrain,oversampled_y))
        return(X_all,y_all)