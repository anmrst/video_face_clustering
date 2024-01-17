#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep  2 17:36:06 2023

@author: anmrst
"""

from keras.models import load_model

from keras_facenet import FaceNet

#model_path = "models/facenet_keras.h5"
#model = load_model("models/facenet_keras.h5")

model = FaceNet()

print(model.inputs)
print(model.outputs)