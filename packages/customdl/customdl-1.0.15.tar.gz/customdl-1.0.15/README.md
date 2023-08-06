# Custom Deep Learning
* Create a customized Feedforward Neural Network
    * Available options:
        * Weight initialization: Random, Xavier, He 
        * Activation functions: Identity, Sigmoid, Softmax, Tanh, ReLU
        * Loss functions: MSE, Cross Entropy
        * Optimizers: GD, Momentum based GD, Nesterov accerelated GD  
        * Learning mode: online, mini-batch, batch
* Refer to the documentation of any class/method by using help(class/method) Eg: help(FNN), help(FNN.compile)
* For a high-level overview of the underlying theory refer:
   * [Feedforward Neural Network](https://github.com/Taarak9/DL-from-Scratch/blob/master/Feedforward%20Neural%20Network/README.md)
   * [Optimizers](https://github.com/Taarak9/DL-from-Scratch/blob/master/Optimizers/README.md)

## Installation
```bash
$ [sudo] pip3 install customdl
``` 
## Development Installation
```bash
$ git clone https://github.com/Taarak9/Custom-DL.git
```
## Usage
```python3
>>> from customdl import FNN
```
### Handwritten Digit Recognition example
```python3
import numpy as np
from matplotlib import pyplot as plt
from mnist_loader import load_data_wrapper 
from customdl import FNN

# MNIST data split
training_data, validation_data, test_data = load_data_wrapper()

# Loss function: Cross Entropy
hdr = FNN(784, "ce")
hdr.add_layer(80, "sigmoid")
hdr.add_layer(10, "sigmoid")
hdr.compile()
hdr.fit(training_data, validation_data)
hdr.accuracy(test_data)
```
The mnist_loader used could be found [here](https://github.com/mnielsen/neural-networks-and-deep-learning/blob/master/src/mnist_loader.py).

### Features to be added
* Plots for monitoring loss and accuracy over epochs
* Regularization techniques: L1, L2, dropout
* Optimizers: Adam, RMSProp
* RBF NN
