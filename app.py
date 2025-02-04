from flask import Flask, request, jsonify, render_template
from flask_cors import CORS, cross_origin
from rice_leaf_disease.utils.common import decodeImage
from rice_leaf_disease.pipeline.predict import PredictionPipeline
import os


app = Flask(__name__)
CORS(app)

class ClientApp:
    def __init__(self):
        self.filename = "inputImage.jpg"
        self.classifier = PredictionPipeline(self.filename)
        

@app.route('/', methods=['GET'])
@cross_origin()
def home():
    return render_template('index.html')


@app.route('/train', methods=['GET', 'POST'])
@cross_origin()
def trainRoute():
    os.system('python main.py')
    return "Done Training !"

@app.route('/predict', methods=['POST'])
@cross_origin()
def predictRoute():
    image = request.json['image']
    decodeImage(image, clApp.filename)
    result = clApp.classifier.predict()
    return jsonify(result)

if __name__ == "__main__":
    clApp = ClientApp()
    app.run(host='0.0.0.0', port=8080)