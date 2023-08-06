#From https://gist.github.com/EndingCredits/b5f35e84df10d46cfa716178d9c862a3
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from tensorflow.python.ops import control_flow_ops
from tensorflow.python.ops import math_ops
from tensorflow.python.ops import state_ops
from tensorflow.python.framework import ops
from tensorflow.python.training import optimizer
import tensorflow as tf
import hyperchamber as hc
import numpy as np
import inspect
from operator import itemgetter
from hypergan.train_hooks.base_train_hook import BaseTrainHook

class AutoSegmentTrainHook(BaseTrainHook):
  def __init__(self, gan=None, config=None, trainer=None, name="GradientPenaltyTrainHook"):
    super().__init__(config=config, gan=gan, trainer=trainer, name=name)
    average_target = self.config.average_target or 0.1
    average_lambda = self.config.average_lambda or 1
    unsure_lambda  = self.config.unsure_lambda or 1

    layer     = gan.named_layers[self.config.layer]
    layer_avg = gan.ops.squash(layer, tf.reduce_mean)

    seg_loss =    tf.abs(average_target - layer_avg) * average_lambda
    unsure_loss = (-tf.abs(layer - 0.5) + 0.5)

    loss = 0.0

    if average_lambda > 0:
      self.gan.add_metric('segment_avg_loss', seg_loss)
      loss += seg_loss

    if unsure_lambda > 0:
      seg_loss = self.ops.squash(unsure_loss * unsure_lambda, tf.reduce_mean)
      self.gan.add_metric('segment_unsure_loss', seg_loss)
      loss += seg_loss

    self.loss = loss

  def losses(self):
    return [None, self.loss]

