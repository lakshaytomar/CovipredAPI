# Importing the required libraries
import pandas as pd, os, sys, pickle, csv
import math

# Initializing some parameters and loading the model "Dataset-III_Modal.pkl"
model = pd.read_pickle(r"Dataset-III_Modal.pkl")
cols_when_model_builds = model.get_booster().feature_names
parameterInput = []

plateletCountMean = 211.6
plateletCountStd = 87.4
monocyteMean = 570.4
monocyteStd = 314.7
leukocyteMean = 7048.1
leukocyteStd = 3350.8
eosinophilsMean = 115.5
eosinophilsStd = 179.7

errorCode = 200
data = []

def normalise(value, mean, standardDeviation):
    """
    This function normalizes the parameter inputs given by the user.
    """
    try:
        if standardDeviation == 0:
            sys.exit("Standard Deviation is zero, please check values")
            quit()

        normalisedValue = (value - mean) / standardDeviation

        return normalisedValue
    except:
        errorCode = 404
        print("Error: {}. Recheck the values you've entered".format(errorCode))


def getPrediction(model, parameterInput):
    """
    This function reads the parameterInput and returns a 'positive' or 'negative' text based on the model.
    """
    plateletCount = float(parameterInput[0])
    monocyte = float(parameterInput[1])
    leukocyte = float(parameterInput[2])
    eosinophils = float(parameterInput[3])

    try:
        
        X = pd.DataFrame({cols_when_model_builds[0] : [normalise(plateletCount, plateletCountMean, plateletCountStd)],
            cols_when_model_builds[1] : [normalise(leukocyte, leukocyteMean, leukocyteStd)],
            cols_when_model_builds[2] : [normalise(eosinophils, eosinophilsMean, eosinophilsStd)],
            cols_when_model_builds[3] : [normalise(monocyte, monocyteMean, monocyteStd ) ]})

        y = model.predict(X)

        if y == 1:
            res = "Positive"
            return res
        else:
            res = "Negative"
            return res

    except:
        return "Error in the input data"


def getProbability(model, parameterInput):
    """
    This function reads the parameterInput and returns probability of covid positive based on the model.
    """
    plateletCount = float(parameterInput[0])
    monocyte = float(parameterInput[1])
    leukocyte = float(parameterInput[2])
    eosinophils = float(parameterInput[3])

    try:
        
        X = pd.DataFrame({cols_when_model_builds[0] : [normalise(plateletCount, plateletCountMean, plateletCountStd)],
            cols_when_model_builds[1] : [normalise(leukocyte, leukocyteMean, leukocyteStd)],
            cols_when_model_builds[2] : [normalise(eosinophils, eosinophilsMean, eosinophilsStd)],
            cols_when_model_builds[3] : [normalise(monocyte, monocyteMean, monocyteStd ) ]})

        y = model.predict_proba(X)

        res = "Probability of COVID-19 Positive is " + str(math.ceil(100 * y[0][1])) + "%"
        return res

    except:
        return "Error in the input data"



def csvPredict(path):
    """
    Handles the CSV input and returns a 2D list that is displayed on the output page
    """
    with open(path) as file:
        csvFile = csv.reader(file)
        for row in csvFile:
            try:
                data.append([row[0], getPrediction(model, row[1:])])
            except:
                continue
    return data
