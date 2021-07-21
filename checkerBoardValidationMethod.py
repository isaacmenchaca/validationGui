import pandas as pd
import numpy as np
from quadrants384_to_96 import quadrants384_to_96

def checkerSetUp(FAMdf, REDdf, input384, sortBy):
    FAMdf = FAMdf.copy()
    REDdf = REDdf.copy()

    if input384 == True:
        setRange = 25
    else:
        setRange = 13

    wellLocation = []
    wellLocationRow = []
    wellLocationCol = []
    FAM_CT = []
    CalRed_CT = []

    specimen_result = []
    repeat_list = []
    for index, row in FAMdf.iterrows():
            for i in range(1, setRange):
                FAMValue = FAMdf.loc[index,i]

                RedValue = REDdf.loc[index,i]
                FAM_CT.append(FAMValue)
                CalRed_CT.append(RedValue)


                wellLocationRow.append(index)
                wellLocationCol.append(i)
                wellLocation.append(index + str(i))

                if np.isnan(FAMValue):
                    specimen_result.append('Negative')
                    repeat_list.append('N/A')
                elif FAMValue >= 36 and FAMValue < 40:
                    specimen_result.append('REPEAT')
                    repeat_list.append('REPEAT')
                elif FAMValue >= 40:
                    specimen_result.append('Negative')
                    repeat_list.append('N/A')
                else:
                    specimen_result.append('Positive')
                    repeat_list.append('N/A')

    checker_dict = {
        'Well': wellLocation,
        'CT Value SARS-CoV-2': FAM_CT,
        'CT Value RNASE P': CalRed_CT,
        'Well row': wellLocationRow,
        'Well col': wellLocationCol,
        'Result': specimen_result,
        'REPEAT Ct VALUE SARS-CoV-2': repeat_list,
        'REPEAT Ct VALUE RNASE P': repeat_list,
        'REPEAT RESULT': repeat_list
    }



    pd.options.display.float_format = '{:,.2f}'.format
    checker_report = pd.DataFrame(checker_dict).round(decimals = 2)
    checker_report = checker_report.sort_values(by = sortBy).\
            fillna('N/A')[['Well', 'CT Value SARS-CoV-2', 'CT Value RNASE P',
                          'Result', 'REPEAT Ct VALUE SARS-CoV-2',
                          'REPEAT Ct VALUE RNASE P', 'REPEAT RESULT']]

    return checker_report


def checkerBoardValidationMethod(file: str, input384 = False, sortBy = ['Well row','Well col'],
                                quadrants384_to_96Method = False): # do RED and FAM together eventually


    FAMdf = pd.read_excel(file)
    FAMdf.rename(columns={'Unnamed: 0':'Rows'}, inplace=True)
    FAMdf.set_index('Rows', inplace = True)
    FAMdf = FAMdf[FAMdf['Unnamed: 1'] == 'Cq'].loc[:, FAMdf.columns != 'Unnamed: 1']
    FAMdf.columns = FAMdf.columns.astype('int64')


    REDdf = pd.read_excel(file,sheet_name = 1)
    REDdf.rename(columns={'Unnamed: 0':'Rows'}, inplace=True)
    REDdf.set_index('Rows', inplace = True)
    REDdf = REDdf[REDdf['Unnamed: 1'] == 'Cq'].loc[:, REDdf.columns != 'Unnamed: 1']
    REDdf.columns = REDdf.columns.astype('int64')


    if quadrants384_to_96Method == False:
        return FAMdf, REDdf, checkerSetUp(FAMdf, REDdf, input384, sortBy)

    elif quadrants384_to_96Method == True:
        sarsQUAD1_96, sarsQUAD2_96, sarsQUAD3_96, sarsQUAD4_96 = quadrants384_to_96(FAMdf)
        redQUAD1_96, redQUAD2_96, redQUAD3_96, redQUAD4_96 = quadrants384_to_96(REDdf)
        sarsdf = [sarsQUAD1_96, sarsQUAD2_96, sarsQUAD3_96, sarsQUAD4_96]
        REDdf = [redQUAD1_96, redQUAD2_96, redQUAD3_96, redQUAD4_96]
        dfs_96 = []
        for sars, red in zip([sarsQUAD1_96, sarsQUAD2_96, sarsQUAD3_96, sarsQUAD4_96],
                            [redQUAD1_96, redQUAD2_96, redQUAD3_96, redQUAD4_96]):
            dfs_96.append(checkerSetUp(sars, red, input384 = False, sortBy = sortBy))
        return sarsdf, REDdf, dfs_96

def checkerBoardEvaluation96Helper(SARSdf, calReddf):
    outputString = ""
    numRepeats = 0
    numFailsNeg = 0
    numFailsPos = 0
    negativeWellsSARS = []
    negativeWellsCalRed = []
    controlsPassed = True

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
                    #print('Controls Failed.')
                    controlsPassed = False

                if (np.isnan(SARSdf.values[rowCase2, colCase2])) or (SARSdf.values[rowCase2, colCase2] >= 40):
                    #print('Controls Failed.')
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

    return controlsPassed, numFailsNeg, numFailsPos, numRepeats


#####3
def checkerBoardEvaluation384Helper(SARSdf, calReddf):
    #print("This will call 96 helper four times.")
    sarsQUAD1_96, sarsQUAD2_96, sarsQUAD3_96, sarsQUAD4_96 = quadrants384_to_96(SARSdf)
    calQUAD1_96, calQUAD2_96, calQUAD3_96, calQUAD4_96 = quadrants384_to_96(calReddf)

    sarsQuads = [sarsQUAD1_96, sarsQUAD2_96, sarsQUAD3_96, sarsQUAD4_96]
    calQuads = [calQUAD1_96, calQUAD2_96, calQUAD3_96, calQUAD4_96]

    allControlsPassed = True
    totalNumFailsNeg = 0
    totalNumFailsPos = 0
    totalNumRepeats = 0

    for sars, calRed in zip(sarsQuads, calQuads):
        controlsPassed, numFailsNeg, numFailsPos, numRepeats = checkerBoardEvaluation96Helper(sars, calRed)
        allControlsPassed = allControlsPassed and controlsPassed
        totalNumFailsNeg += numFailsNeg
        totalNumFailsPos += numFailsPos
        totalNumRepeats += numRepeats

    return allControlsPassed, totalNumFailsNeg, totalNumFailsPos, totalNumRepeats


def checkerBoardEvaluation(controlsPassed, numFailsNeg, numFailsPos, numRepeats, input384 = False):
    totalSampleEach = 0
    platePassed = True

    if input384 == False: # 96 test
        totalSampleEach = 46
        percentageNeg = (totalSampleEach - numFailsNeg) * 100 / totalSampleEach
        percentagePos = (totalSampleEach - numFailsPos) * 100 / totalSampleEach
    elif input384 == True: # 96 test
        totalSampleEach = 184
        percentageNeg = (totalSampleEach - numFailsNeg) * 100 / totalSampleEach
        percentagePos = (totalSampleEach - numFailsPos) * 100 / totalSampleEach

    if controlsPassed and percentageNeg >= 95 and percentagePos >= 95: # PASS CRITERIA
        if numRepeats == 0:
            outputString = "Plate Passed. Checkerboard Summary: Negative = %.2f%% (%d/ %d), Positive = %.2f%% (%d/ %d)." % (percentageNeg, totalSampleEach - numFailsNeg, totalSampleEach, percentagePos, totalSampleEach - numFailsPos, totalSampleEach)
        else:
            outputString = "Plate Passed. Checkerboard Summary: Negative = %.2f%% (%d/ %d), Positive = %.2f%% (%d/ %d), Total Repeats = %d." % (percentageNeg, totalSampleEach - numFailsNeg, totalSampleEach, percentagePos, totalSampleEach - numFailsPos, totalSampleEach,numRepeats)

    else:
        if not(controlsPassed):
            outputString = "Plate Failed. Checkerboard Summary: Controls failed. Negative = %.2f%% (%d/ %d), Positive = %.2f%% (%d/ %d)." % (percentageNeg, totalSampleEach - numFailsNeg, totalSampleEach, percentagePos, totalSampleEach - numFailsPos, totalSampleEach)
        else:
            outputString = "Plate Failed. Checkerboard Summary: Negative = %.2f%% (%d/ %d), Positive = %.2f%% (%d/ %d)." % (percentageNeg, totalSampleEach - numFailsNeg, totalSampleEach, percentagePos, totalSampleEach - numFailsPos, totalSampleEach)
        platePassed = False

    return outputString, platePassed
