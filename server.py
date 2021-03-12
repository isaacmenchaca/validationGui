import eel, json
import tkinter as tk
from tkinter import filedialog
import numpy as np
import pandas as pd
from uniformityValidationMethod import uniformityValidationMethod
from accuracyValidationMethod import accuracyValidationMethod_96
# Set web files folder and optionally specify which file types to check for eel.expose()
#   *Default allowed_extensions are: ['.js', '.html', '.txt', '.htm', '.xhtml']
eel.init('web')



@eel.expose
def pythonGoButtonClicked():
    root = tk.Tk()
    root.withdraw()
    root.wm_attributes('-topmost', 1)
    filePath = filedialog.askopenfilename()
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
            # print(outputString)
            # print(mapAcc)
            # print(outputDf)

            return SARSdf.to_json(), calReddf.to_json(), outputString, platePassed
        elif textPlateType == 384:
            if textQuadrantSplitType == "No":
                print('FIXME: Run python Accuracy 384 method')
            elif textQuadrantSplitType == "Yes":
                print('FIXME: Run python Accuracy 384 method with Quadrants split')
# -->>>>>>>>>>>>>>
    elif textValidationType == 'Uniformity':
        if textPlateType == 96:
            print('FIXME: Run python Uniformity 96 method')
            SARSdf, calReddf, outputDf = uniformityValidationMethod(file = filePath, input384 = False)
            outputString, platePassed = uniformityEvaluationSummary(SARSdf, calReddf)

            print(SARSdf)
            print(calReddf)
            print(outputDf)

            return SARSdf.to_json(), calReddf.to_json(), outputString, platePassed

#-->>>>>>>>>>>>>>

        elif textPlateType == 384:
            if textQuadrantSplitType == "No":
                print('FIXME: Run python Uniformity 384 method')
                uniformJson = uniformityValidationMethod(file = filePath, input384=True).to_json()

                return uniformJson # delete right after
            elif textQuadrantSplitType == "Yes":
                print('FIXME: Run python Uniformity 384 method with Quadrants split')
#-->>>>>>>>>>>>>>
    elif textValidationType == 'Checkerboard':
        if textPlateType == 96:
            print('FIXME: Run python Checkerboard 96 method')
        elif textPlateType == 384:
            if textQuadrantSplitType == "No":
                print('FIXME: Run python Checkerboard 384 method')
            elif textQuadrantSplitType == "Yes":
                print('FIXME: Run python Checkerboard 384 method with Quadrants split')
    return
# ------------------------------------------------------------------------------
def javascriptAccuracyMap2Dataframe(jsInputData):
    mapAcc = pd.DataFrame(jsInputData)
    mapAcc.columns = np.linspace(1, 12, 12, dtype = np.int)
    mapAcc['Row'] = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    mapAcc.set_index(['Row'], inplace = True)
    mapAcc.replace({'100': 100, '200': 200, '2000': 2000, '20000': 20000, 'N/A': np.nan}, inplace=True)
    return mapAcc

# ------------------------------------------------------------------------------
def accuracyEvaluationSummary(df):
    control_filter = (df["Specimen Number"] == "Control")
    concentration_negative = (df["Specimen Concentration (cps/ mL)"] == "Negative")
    concentration_100 = (df["Specimen Concentration (cps/ mL)"] == "100")
    concentration_200 = (df["Specimen Concentration (cps/ mL)"] == "200")
    concentration_2000 = (df["Specimen Concentration (cps/ mL)"] == "2000")
    concentration_20000 = (df["Specimen Concentration (cps/ mL)"] == "20000")
    result_Fail = (df["REPEAT Ct VALUE SARS-CoV-2"] == "FAIL")
    result_Repeat = (df["Result"] == "REPEAT")
    ctSarsValue_Negative = (df["CT Value SARS-CoV-2"] == "N/A")
    ctCalRValue_Negative = (df["CT Value RNASE P"] == "N/A")
    negativeControlFail1 = (control_filter & concentration_negative & ~ctCalRValue_Negative)
    negativeControlFail2 = (control_filter & concentration_negative & ~ctSarsValue_Negative)
    positiveControlFail = (control_filter & ~concentration_negative & ctCalRValue_Negative & ctSarsValue_Negative)


    controlPassed = 'Pass'
    if (len(df[negativeControlFail1]) != 0) or (len(df[negativeControlFail2][df[negativeControlFail2]["CT Value SARS-CoV-2"] < 40]) != 0) or (len(df[positiveControlFail]) != 0):
        controlPassed = 'Fail'



    percentageNeg = 1 - len(df[~control_filter & concentration_negative & result_Fail]) / len(df[~control_filter & concentration_negative])
    percentage100 = 1 - len(df[~control_filter & concentration_100 & result_Fail]) / len(df[~control_filter & concentration_100])
    percentage200 = 1 - len(df[~control_filter & concentration_200 & result_Fail]) / len(df[~control_filter & concentration_200])
    percentage2000 = 1 - len(df[~control_filter & concentration_2000 & result_Fail]) / len(df[~control_filter & concentration_2000])
    percentage20000 = 1 - len(df[~control_filter & concentration_20000 & result_Fail]) / len(df[~control_filter & concentration_20000])
    totalRepeats = len(df[(df['Result'] == "REPEAT")])


    outputString = ''
    platePassed = True
    if (controlPassed == "Fail") or (percentageNeg < .95) or (percentage100 < 0.5) or (percentage200 < 0.95) or (percentage2000 < 0.95) or (percentage20000 < 0.95):
        if controlPassed == "Fail":
            outputString = 'Plate Failed. Accuracy Summary: Controls failed, Negative = %.2f%%, 100 = %.2f%%, 200 = %.2f%%, 2000 = %.2f%%, 20000 = %.2f%%' % (percentageNeg * 100, percentage100 * 100, percentage200 * 100, percentage2000 * 100, percentage20000 * 100)
        if controlPassed == "Pass":
            outputString = 'Plate Failed. Accuracy Summary: Negative = %.2f%%, 100 = %.2f%%, 200 = %.2f%%, 2000 = %.2f%%, 20000 = %.2f%%' % (percentageNeg * 100, percentage100 * 100, percentage200 * 100, percentage2000 * 100, percentage20000 * 100)
        platePassed = False
    else:
        if totalRepeats == 0:
            outputString = 'Plate Passed. Accuracy Summary: Negative = %.2f%%, 100 = %.2f%%, 200 = %.2f%%, 2000 = %.2f%%, 20000 = %.2f%%' % (percentageNeg * 100, percentage100 * 100, percentage200 * 100, percentage2000 * 100, percentage20000 * 100)
        else:
            outputString = 'Plate Passed. Accuracy Summary: Negative = %.2f%%, 100 = %.2f%%, 200 = %.2f%%, 2000 = %.2f%%, 20000 = %.2f%%, %d total repeats'% (percentageNeg * 100, percentage100 * 100, percentage200 * 100, percentage2000 * 100, percentage20000 * 100, totalRepeats)

    return outputString, platePassed

# ------------------------------------------------------------------------------
def uniformityEvaluationSummary(SARSdf, calReddf):
    SARSdfMean = SARSdf.values.mean()
    SARSdfSTD = SARSdf.values.std()
    SARSdfRange = SARSdf.values.max() - SARSdf.values.min()

    calReddfMean = calReddf.values.mean()
    calReddfSTD = calReddf.values.std()
    calReddRange = calReddf.values.max() - calReddf.values.min()

    outputString = ''
    platePassed = True
    if (SARSdfRange > 1.50) or (calReddRange > 1.50):
        if np.isnan(SARSdfRange) or np.isnan(calReddRange):
            outputString = 'Plate Failed. Uniformity CT Summary: Plate contained an absent CT value(s) for either SARS or Human (Cal Red).'
        else:
            outputString = 'Plate Failed. Uniformity CT Summary: SARS (Mean = %.2f ± %.2f, MAX - MIN = %.2f), Human (Mean = %.2f ± %.2f, MAX - MIN = %.2f)' \
                                % (SARSdfMean, SARSdfSTD, SARSdfRange, calReddfMean, calReddfSTD, calReddRange)
        platePassed = False
    else:
        outputString = 'Plate Passed. Uniformity CT Summary: SARS (Mean = %.2f ± %.2f, MAX - MIN = %.2f), Human (Mean = %.2f ± %.2f, MAX - MIN = %.2f)' \
                            % (SARSdfMean, SARSdfSTD, SARSdfRange, calReddfMean, calReddfSTD, calReddRange)

    return outputString, platePassed




eel.start('index.html', size=(1000,800))            # Start (this blocks and enters loop)
