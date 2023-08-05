import numpy as np
from .ActivationFunctions import Sigmoid, Tanh, ReLU, LeakyReLU, StableSoftMax
Sigmoid, Tanh, ReLU, LeakyReLU, StableSoftMax = Sigmoid(), Tanh(), ReLU(), LeakyReLU(), StableSoftMax()

class NN:
  def __init__(self, InputSize, OutputSize, Activation, LearningRate, WeightsInit=(-1, 1), BiasesInit=(0, 0), DropoutRate=0):
    self.Weights = np.random.uniform(WeightsInit[0], WeightsInit[1], (InputSize, OutputSize))
    self.Biases = np.random.uniform(BiasesInit[0], BiasesInit[1], (OutputSize))
    self.Activation, self.LearningRate, self.DropoutRate = Activation, LearningRate, DropoutRate
  
  def ForwardProp(self, InputLayer):
    self.InputLayer = InputLayer
    self.Output = np.transpose(self.Weights) @ InputLayer + self.Biases
  
    # Apply Activation Function
    if self.Activation == 'Sigmoid': self.Output = Sigmoid.Sigmoid(self.Output)
    if self.Activation == 'Tanh': self.Output = Tanh.Tanh(self.Output)
    if self.Activation == 'ReLU': self.Output = ReLU.ReLU(self.Output)
    if self.Activation == 'LeakyReLU': self.Output = LeakyReLU.LeakyReLU(self.Output)
    if self.Activation == 'StableSoftMax': self.Output = StableSoftMax.StableSoftMax(self.Output)
    if self.Activation == 'None': self.Output = self.Output

    self.Dropout = np.random.binomial(1, self.DropoutRate, size=len(self.Output))
    self.Dropout = np.where(self.Dropout == 0, 1, 0)
    self.Output *= self.Dropout

    return self.Output

  def BackProp(self, FollowingLayerError):
    FollowingLayerError *= self.Dropout

    # Calculate Gradients
    FollowingLayerGradient = np.zeros(self.Output.shape)
    if self.Activation == 'Sigmoid': FollowingLayerGradient = np.multiply(Sigmoid.Derivative(self.Output), FollowingLayerError)
    if self.Activation == 'Tanh': FollowingLayerGradient = np.multiply(Tanh.Derivative(self.Output), FollowingLayerError)
    if self.Activation == 'ReLU': FollowingLayerGradient = np.multiply(ReLU.Derivative(self.Output), FollowingLayerError)
    if self.Activation == 'LeakyReLU': FollowingLayerGradient = np.multiply(LeakyReLU.Derivative(self.Output), FollowingLayerError)
    if self.Activation == 'StableSoftMax': FollowingLayerGradient = np.multiply(StableSoftMax.Derivative(self.Output), FollowingLayerError)
    if self.Activation == 'None': FollowingLayerGradient = np.multiply(self.Output, FollowingLayerError)
      
    # Calculate Current Layer Error
    CurrentLayerError = self.Weights @ FollowingLayerError
      
    # Apply Deltas To The Weights And Biases
    self.Biases += FollowingLayerGradient * self.LearningRate
    self.Weights += np.outer(np.transpose(self.InputLayer), FollowingLayerGradient) * self.LearningRate
    return CurrentLayerError