import eel, json
import tkinter as tk
from tkinter import filedialog
import numpy as np
import pandas as pd
from uniformityValidationMethod import uniformityValidationMethod
from accuracyValidationMethod import accuracyValidationMethod_96
from checkerBoardValidationMethod import checkerBoardValidationMethod
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
            # print(outputString)
            # print(mapAcc)
            print(outputDf)
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
            return SARSdf.to_json(), calReddf.to_json(), outputString, platePassed

#-->>>>>>>>>>>>>>

        elif textPlateType == 384:
            if textQuadrantSplitType == "No":
                print('FIXME: Run python Uniformity 384 method')
                SARSdf, calReddf, outputDf = uniformityValidationMethod(file = filePath, input384 = False)
                outputString, platePassed = uniformityEvaluationSummary(SARSdf, calReddf)
                print(SARSdf)
                print(calReddf)
                print(outputDf)
                popUpSaveNotSplit(outputDf)

                return SARSdf.to_json(), calReddf.to_json(), outputString, platePassed

#-->>>>>>>>>>>>>>
            elif textQuadrantSplitType == "Yes":
                print('FIXME: Run python Uniformity 384 method with Quadrants split')

#-->>>>>>>>>>>>>>
    elif textValidationType == 'Checkerboard':
        if textPlateType == 96:
            print('FIXME: Run python Checkerboard 96 method')
            SARSdf, calReddf, outputDf = checkerBoardValidationMethod(file = filePath, input384 = False)
            outputString, platePassed = checkerBoardEvaluationSummary(SARSdf, calReddf)

            print(SARSdf)
            print(calReddf)
            print(outputDf)

            return SARSdf.to_json(), calReddf.to_json(), outputString, platePassed
# -->>>>>>>>>>>>>>
        elif textPlateType == 384:
            if textQuadrantSplitType == "No":
                print('FIXME: Run python Checkerboard 384 method')
            elif textQuadrantSplitType == "Yes":
                print('FIXME: Run python Checkerboard 384 method with Quadrants split')
# -->>>>>>>>>>>>>>
    return

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
    if (SARSdfRange > 1.50) or (calReddRange > 1.50) or (np.isnan(SARSdfMean)) or (np.isnan(calReddfMean)):
        if np.isnan(SARSdfMean) or np.isnan(calReddfMean):
            outputString = 'Plate Failed. Uniformity CT Summary: Plate contained absent CT value(s) for either SARS or Human (Cal Red).'
        else:
            outputString = 'Plate Failed. Uniformity CT Summary: SARS (Mean = %.2f ± %.2f, MAX - MIN = %.2f), Human (Mean = %.2f ± %.2f, MAX - MIN = %.2f)' \
                                % (SARSdfMean, SARSdfSTD, SARSdfRange, calReddfMean, calReddfSTD, calReddRange)
        platePassed = False
    else:
        outputString = 'Plate Passed. Uniformity CT Summary: SARS (Mean = %.2f ± %.2f, MAX - MIN = %.2f), Human (Mean = %.2f ± %.2f, MAX - MIN = %.2f)' \
                            % (SARSdfMean, SARSdfSTD, SARSdfRange, calReddfMean, calReddfSTD, calReddRange)

    return outputString, platePassed

# ------------------------------------------------------------------------------

def checkerBoardEvaluationSummary(SARSdf, calReddf, input384 = False):
    outputString = ""
    numRepeats = 0
    numFailsNeg = 0
    numFailsPos = 0
    negativeWellsSARS = []
    negativeWellsCalRed = []
    controlsPassed = True
    platePassed = True

    if input384 == False:
        for rowCase1, rowCase2 in zip(np.arange(0, 8, 2), np.arange(1, 8, 2)):
            for colCase1 in np.arange(0, 12, 2):
                if (rowCase1 == 0 or rowCase1 == 2) and colCase1 == 0:
                    if not(np.isnan(calReddf.values[rowCase1, colCase1])):
                        controlsPassed = False

                    if not((np.isnan(SARSdf.values[rowCase1, colCase1])) or (SARSdf.values[rowCase1, colCase1] >= 40)):
                        controlsPassed = False
                else:
                    if not (np.isnan(SARSdf.values[rowCase1, colCase1]) or (SARSdf.values[rowCase1, colCase1] >= 40)):
                        if SARSdf.values[rowCase1, colCase1] >= 36: # repeat
                            numRepeats +=1
                        else:
                            numFailsNeg += 1

                negativeWellsSARS.append(SARSdf.values[rowCase1, colCase1])
                negativeWellsCalRed.append(calReddf.values[rowCase1, colCase1])

            for colCase2 in np.arange(1, 12, 2):
                if not (np.isnan(SARSdf.values[rowCase2, colCase2]) or (SARSdf.values[rowCase2, colCase2] >= 40)):
                        if SARSdf.values[rowCase2, colCase2] >= 36: # repeat
                            numRepeats +=1
                        else:
                            numFailsNeg += 1

                negativeWellsSARS.append(SARSdf.values[rowCase2, colCase2])
                negativeWellsCalRed.append(calReddf.values[rowCase2, colCase2])


        positiveWellsSARS = []
        positiveWellsCalRed = []
        for rowCase1, rowCase2 in zip(np.arange(0, 8, 2), np.arange(1, 8, 2)):
            for colCase2 in np.arange(0, 12, 2):
                if (rowCase2 == 0 or rowCase2 == 2) and colCase2 == 0:
                    if (np.isnan(calReddf.values[rowCase2, colCase2])):
                        print('Controls Failed.')
                        controlsPassed = False

                    if (np.isnan(SARSdf.values[rowCase2, colCase2])) or (SARSdf.values[rowCase2, colCase2] >= 40):
                        print('Controls Failed.')
                        controlsPassed = False

                if np.isnan(SARSdf.values[rowCase2, colCase2]) or SARSdf.values[rowCase2, colCase2] >= 40:
                    # print("Fail", SARSdf.values[rowCase2, colCase2])
                    numFailsPos += 1


                positiveWellsSARS.append(SARSdf.values[rowCase2, colCase2])
                positiveWellsCalRed.append(calReddf.values[rowCase2, colCase2])

            for colCase1 in np.arange(1, 12, 2):

                if np.isnan(SARSdf.values[rowCase1, colCase1]) or SARSdf.values[rowCase1, colCase1] >= 40:
                    numFailsPos += 1
                    # print("Fail", SARSdf.values[rowCase1, colCase1])

                positiveWellsSARS.append(SARSdf.values[rowCase1, colCase1])
                positiveWellsCalRed.append(calReddf.values[rowCase1, colCase1])


        percentageNeg = (46 - numFailsNeg) * 100 / 46
        percentagePos = (46 - numFailsPos) * 100 / 46

        if controlsPassed and percentageNeg >= 95 and percentagePos >= 95: # PASS CRITERIA
            if numRepeats == 0:
                outputString = "Plate Passed. Checkerboard Summary: Negative = %.2f%% (%d/ 46), Positive = %.2f%% (%d/ 46)." % (percentageNeg, 46 - numFailsNeg, percentagePos, 46 - numFailsPos)
            else:
                outputString = "Plate Passed. Checkerboard Summary: Negative = %.2f%% (%d/ 46), Positive = %.2f%% (%d/ 46), Total Repeats = %d." % (percentageNeg, 46 - numFailsNeg, percentagePos, 46 - numFailsPos, numRepeats)

        else:
            if not(controlsPassed):
                outputString = "Plate Failed. Checkerboard Summary: Controls failed. Negative = %.2f%% (%d/ 46), Positive = %.2f%% (%d/ 46)." % (percentageNeg, 46 - numFailsNeg, percentagePos, 46 - numFailsPos)
            else:
                outputString = "Plate Failed. Checkerboard Summary: Negative = %.2f%% (%d/ 46), Positive = %.2f%% (%d/ 46)." % (percentageNeg, 46 - numFailsNeg, percentagePos, 46 - numFailsPos)
            platePassed = False
    return outputString, platePassed

eel.start('index.html', size=(1000,800))            # Start (this blocks and enters loop)
