import eel, json
import tkinter as tk
from tkinter import filedialog
import numpy as np
import pandas as pd
from uniformityValidationMethod import uniformityValidationMethod, uniformityEvaluationSummary
from accuracyValidationMethod import accuracyValidationMethod_96
from checkerBoardValidationMethod import checkerBoardValidationMethod, checkerBoardEvaluationSummary
# Set web files folder and optionally specify which file types to check for eel.expose()
#   *Default allowed_extensions are: ['.js', '.html', '.txt', '.htm', '.xhtml']
eel.init('web')



@eel.expose
def pythonGoButtonClicked():
    root = tk.Tk()
    root.attributes('-topmost', 1)
    root.withdraw()
    filePath = filedialog.askopenfilename()
    root.destroy()
    return filePath

def popUpSaveNotSplit(outputDf):
    print('Pop up')
    root = tk.Tk()
    root.attributes('-topmost', 1)
    root.withdraw()
    filePath = filedialog.asksaveasfile(mode='a', defaultextension = '.xlsx')
    root.destroy()
    if filePath:
        outputDf.to_excel(filePath.name)
    return filePath

# ------------------------------------------------------------------------------
@eel.expose
def getValidationInputs(textValidationType, textPlateType, textQuadrantSplitType, filePath, inputInfo = None):
    print(textValidationType, textPlateType, textQuadrantSplitType, filePath)

    if textValidationType == 'Accuracy':
        if textPlateType == 96:

            mapAcc = javascriptAccuracyMap2Dataframe(np.resize(np.array(inputInfo), [12, 8]).T)
            SARSdf, calReddf, outputDf = accuracyValidationMethod_96(mapAcc, file = filePath)
            outputString, platePassed = accuracyEvaluationSummary(outputDf)
            print(outputDf)
            popUpSaveNotSplit(outputDf)
            return SARSdf.to_json(), calReddf.to_json(), outputString, platePassed

        elif textPlateType == 384:
            if textQuadrantSplitType == "No":
                print('FIXME: Run python Accuracy 384 method')
            elif textQuadrantSplitType == "Yes":
                print('FIXME: Run python Accuracy 384 method with Quadrants split')
# -->>>>>>>>>>>>>>
    elif textValidationType == 'Uniformity':
        if textPlateType == 96:
            SARSdf, calReddf, outputDf = uniformityValidationMethod(file = filePath, input384 = False)
            outputString, platePassed = uniformityEvaluationSummary(SARSdf, calReddf)
            popUpSaveNotSplit(outputDf)
            return SARSdf.to_json(), calReddf.to_json(), outputString, platePassed

#-->>>>>>>>>>>>>>

        elif textPlateType == 384:
            if textQuadrantSplitType == "No":
                SARSdf, calReddf, outputDf = uniformityValidationMethod(file = filePath, input384 = False)
                outputString, platePassed = uniformityEvaluationSummary(SARSdf, calReddf)
                popUpSaveNotSplit(outputDf)
                return SARSdf.to_json(), calReddf.to_json(), outputString, platePassed

            elif textQuadrantSplitType == "Yes":
                print('FIXME: Run python Uniformity 384 method with Quadrants split')

#-->>>>>>>>>>>>>>
    elif textValidationType == 'Checkerboard':
        if textPlateType == 96:
            SARSdf, calReddf, outputDf = checkerBoardValidationMethod(file = filePath, input384 = False)
            outputString, platePassed = checkerBoardEvaluationSummary(SARSdf, calReddf)
            popUpSaveNotSplit(outputDf)
            return SARSdf.to_json(), calReddf.to_json(), outputString, platePassed

        elif textPlateType == 384:
            if textQuadrantSplitType == "No":
                print('FIXME: Run python Checkerboard 384 method')
                SARSdf, calReddf, outputDf = checkerBoardValidationMethod(file = filePath, input384 = False)
                # outputString, platePassed = uniformityEvaluationSummary(SARSdf, calReddf)
                # popUpSaveNotSplit(outputDf)
                print(SARSdf)
                print(calReddf)
                print(outputDf)
                return SARSdf.to_json(), calReddf.to_json(), "filler", True
            elif textQuadrantSplitType == "Yes":
                print('FIXME: Run python Checkerboard 384 method with Quadrants split')
    return

def javascriptAccuracyMap2Dataframe(jsInputData):
    mapAcc = pd.DataFrame(jsInputData)
    mapAcc.columns = np.linspace(1, 12, 12, dtype = np.int)
    mapAcc['Row'] = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    mapAcc.set_index(['Row'], inplace = True)
    mapAcc.replace({'100': 100, '200': 200, '2000': 2000, '20000': 20000, 'N/A': np.nan}, inplace=True)
    return mapAcc


eel.start('index.html', size=(1000,800))            # Start (this blocks and enters loop)
