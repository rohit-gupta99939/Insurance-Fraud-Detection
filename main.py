from wsgiref import simple_server
from flask import Flask, request, render_template, jsonify
import pandas as pd
from pathlib import Path

from flask import Response
import os
from flask_cors import CORS, cross_origin
from flow.prediction_Validation_Insertion import pred_validation
from flow.trainingModel import trainModel
from flow.training_Validation_Insertion import train_validation
import flask_monitoringdashboard as dashboard
from flow.predictFromModel import prediction

os.putenv('LANG', 'en_US.UTF-8')
os.putenv('LC_ALL', 'en_US.UTF-8')

app = Flask(__name__)
dashboard.bind(app)
CORS(app)


# Create a folder to store uploaded files
UPLOAD_FOLDER = 'Batch_files\Prediction_Batch_files'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route("/", methods=['GET'])
@cross_origin()
def home():
    return render_template('index.html')

@app.route("/predict", methods=['POST'])
@cross_origin()
def predictRouteClient():
    try:
        
        # path = request.json['filepath']
        if 'files' not in request.files:
            return jsonify({"error": "No file part"})
        file = request.files['files']
        if file.filename == '':
            return jsonify({"error": "No selected file"})
        
        # Save the uploaded file
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)


        pred_val = pred_validation(UPLOAD_FOLDER) #object initialization

        pred_val.prediction_validation() #calling the prediction_validation function

        pred = prediction(UPLOAD_FOLDER) #object initialization

        # predicting for dataset present in database
        path = pred.predictionFromModel()
        print(path)
        # Read the uploaded CSV file
        try:

            df = pd.read_csv(path)
            # Convert the dataframe to HTML
            csv_html = df.to_html(classes="table table-striped", index=False)
            return render_template('index.html', table=csv_html)  # Send the HTML table to the frontend
        except Exception as e:
            return jsonify({"error": f"Error processing the CSV file: {str(e)}"})


        # return Response("Prediction File created at %s!!!" % path)

    except ValueError:
        return Response("Error Occurred! %s" %ValueError)
    except KeyError:
        return Response("Error Occurred! %s" %KeyError)
    except Exception as e:
        return Response("Error Occurred! %s" %e)



@app.route("/train", methods=['GET'])
@cross_origin()
def trainRouteClient():

    try:
            path = Path('D:/neuron/case_study/Insurance-Fraud-Detection/Batch_files/Training_Batch_Files/')
            train_valObj = train_validation(path) #object initialization

            train_valObj.train_validation()#calling the training_validation function


            trainModelObj = trainModel() #object initialization
            trainModelObj.trainingModel() #training the model for the files in the table


    except ValueError:

        return Response("Error Occurred! 1 %s" % ValueError)

    except KeyError:

        return Response("Error Occurred! 2 %s" % KeyError)

    except Exception as e:

        return Response("Error Occurred!  3%s" % e)
    return Response("Training successfull!!")

port = int(os.getenv("PORT",5001))
if __name__ == "__main__":
    app.run(port=port,debug=True)
