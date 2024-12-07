from wsgiref import simple_server
from flask import Flask, request, render_template
from flask import Response
import os
from flask_cors import CORS, cross_origin
from flow.training_Validation_Insertion import train_validation
from flow.trainingModel import trainModel
from flow.prediction_Validation_Insertion import pred_validation
from flow.predictFromModel import prediction
from pathlib import Path

# Define the base directory using pathlib
base_dir = Path('D:/neuron/case_study/Insurance-Fraud-Detection/Batch_files/Training_Batch_Files/')
base_test_dir = Path('D:/neuron/case_study/Insurance-Fraud-Detection/Batch_files/Prediction_Batch_files/')
# Initialize your object with the path

train_valObj = train_validation(base_dir)
train_valObj.train_validation()
trainModelObj = trainModel() #object initialization
trainModelObj.trainingModel() #training the model for the files in the table




pred_val = pred_validation(base_test_dir) #object initialization

pred_val.prediction_validation() #calling the prediction_validation function

pred = prediction(base_test_dir) #object initialization

# predicting for dataset present in database
# path = pred.predictionFromModel()