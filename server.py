import eel, json
import tkinter as tk
from tkinter import filedialog
import numpy as np
import pandas as pd
from uniformityValidationMethod import uniformityValidationMethod, uniformityEvaluationSummary
from accuracyValidationMethod import accuracyValidationMethod_96, accuracyEvaluationSummary
from checkerBoardValidationMethod import checkerBoardValidationMethod, checkerBoardEvaluation, checkerBoardEvaluation96Helper, checkerBoardEvaluation384Helper
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

def popUpSaveNotSplit(outputDf, mapAcc = None, accuracy = False):
    print('Pop up')
    root = tk.Tk()
    root.attributes('-topmost', 1)
    root.withdraw()
    filePath = filedialog.asksaveasfile(mode='a', defaultextension = '.xlsx')
    root.destroy()
    if filePath:
        outputDf.to_excel(filePath.name)
        if accuracy != False:
            mapAcc.to_excel(filePath.name[:-5] +'_AccuracyMap.xlsx')
            return filePath, mapAcc
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
            popUpSaveNotSplit(outputDf, mapAcc, accuracy = True)
            return SARSdf.to_json(), calReddf.to_json(), outputString, platePassed

# -->>>>>>>>>>>>>>
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


        elif textPlateType == 384:
            if textQuadrantSplitType == "No":
                SARSdf, calReddf, outputDf = uniformityValidationMethod(file = filePath, input384 = True) # input384 param doesnt matter
                outputString, platePassed = uniformityEvaluationSummary(SARSdf, calReddf)
                popUpSaveNotSplit(outputDf)
                return SARSdf.to_json(), calReddf.to_json(), outputString, platePassed
#-->>>>>>>>>>>>>>

            elif textQuadrantSplitType == "Yes":
                print('FIXME: Run python Uniformity 384 method with Quadrants split')
                SARSdf, calReddf, outputDf = uniformityValidationMethod(file = filePath, input384 = True, quadrants384_to_96Method = True)

                outputString = []
                platePassed = []

                for sars, cal in zip(SARSdf, calReddf):
                    output, plate = uniformityEvaluationSummary(sars, cal)
                    outputString.append(output)
                    platePassed.append(plate)

                print(outputString)

                return SARSdf[0].to_json(), SARSdf[1].to_json(), SARSdf[2].to_json(), SARSdf[3].to_json(), \
                        calReddf[0].to_json(), calReddf[1].to_json(), calReddf[2].to_json(), calReddf[3].to_json(), \
                         outputString[0], outputString[1], outputString[2], outputString[3],\
                          platePassed[0], platePassed[1], platePassed[2], platePassed[3]


#-->>>>>>>>>>>>>>
    elif textValidationType == 'Checkerboard':
        if textPlateType == 96:
            SARSdf, calReddf, outputDf = checkerBoardValidationMethod(file = filePath, input384 = False)
            controlsPassed, numFailsNeg, numFailsPos, numRepeats = checkerBoardEvaluation96Helper(SARSdf, calReddf)
            outputString, platePassed = checkerBoardEvaluation(controlsPassed, numFailsNeg, numFailsPos, numRepeats)
            popUpSaveNotSplit(outputDf)
            return SARSdf.to_json(), calReddf.to_json(), outputString, platePassed

        elif textPlateType == 384:
            if textQuadrantSplitType == "No":
                SARSdf, calReddf, outputDf = checkerBoardValidationMethod(file = filePath, input384 = True) # input384 doesnt matter here
                controlsPassed, numFailsNeg, numFailsPos, numRepeats = checkerBoardEvaluation384Helper(SARSdf, calReddf)
                outputString, platePassed = checkerBoardEvaluation(controlsPassed, numFailsNeg, numFailsPos, numRepeats, input384 = True)
                popUpSaveNotSplit(outputDf)
                return SARSdf.to_json(), calReddf.to_json(), outputString, platePassed
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
