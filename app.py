from flask import Flask, jsonify, request
from prediction import getPrediction, getProbability, model, csvPredict
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/prediction', methods=["GET", "POST"])
def prediction():
    try:
        parameterInput = [float(x) for x in request.json.values()]
        predictionText="{}".format(getPrediction(model, parameterInput))
        probabilityText="{}".format(getProbability(model, parameterInput))

    except:
        predictionText="There was an error predicting the result."
        probabilityText="Recheck the data entered."

    request.json['p'] = predictionText
    request.json['m'] = probabilityText
    return jsonify(request.json)


if __name__ == "__main__":
    app.run(debug = True)