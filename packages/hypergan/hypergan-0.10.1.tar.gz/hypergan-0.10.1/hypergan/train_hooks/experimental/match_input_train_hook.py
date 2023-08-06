#From https://gist.github.com/EndingCredits/b5f35e84df10d46cfa716178d9c862a3
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from tensorflow.python.ops import control_flow_ops
from tensorflow.python.ops import math_ops
from tensorflow.python.ops import state_ops
from tensorflow.python.framework import ops
from tensorflow.python.training import optimizer
from hypergan.viewer import GlobalViewer
import tensorflow as tf
import hyperchamber as hc
import numpy as np
import inspect
from operator import itemgetter
from hypergan.train_hooks.base_train_hook import BaseTrainHook

class MatchInputTrainHook(BaseTrainHook):
  """ Makes d_fake and d_real match by training on a zero-based addition to the input images. """
  def __init__(self, gan=None, config=None, trainer=None, name="GradientPenaltyTrainHook", layer="match_support", variables=["x","g"]):
    super().__init__(config=config, gan=gan, trainer=trainer, name=name)
    xa = gan.inputs.xa
    gb = gan.generator.sample
    lam = self.config["lambda"] or 0.01
    
    loss = lam*gan.ops.squash(tf.abs(gb - xa))
    self.loss = loss
    self.gan.add_metric('l2-cross', loss)

  def losses(self):
    return [None, self.loss]
