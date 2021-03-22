import pandas as pd # version 0.25.1
import numpy as np # version 1.18.4
from quadrants384_to_96 import quadrants384_to_96
pd.set_option("display.max_rows", None, "display.max_columns", None)

def uniformitySetUp(sarsdf, REDdf, input384):
    FAMdf = sarsdf.copy()
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

    uniformity_dict = {
        'Well': wellLocation,
        'CT Value SARS-CoV-2': FAM_CT,
        'CT Value RNASE P': CalRed_CT,
        'Well row': wellLocationRow,
        'Well col': wellLocationCol,
        'Result': specimen_result
    }

    pd.options.display.float_format = '{:,.2f}'.format
    uniformity_report = pd.DataFrame(uniformity_dict).round(decimals = 2)
    uniformity_report = uniformity_report.sort_values(by = ['Well row','Well col']).\
            fillna('N/A')[['Well', 'CT Value SARS-CoV-2', 'CT Value RNASE P',
                          'Result']]
    return uniformity_report

def uniformityValidationMethod(file: str, input384 = False,
                               quadrants384_to_96Method = False):

    sarsdf = pd.read_excel(file,
                              sheet_name = 0)
    sarsdf.rename(columns={'Unnamed: 0':'Rows'}, inplace=True)
    sarsdf.set_index('Rows', inplace = True)
    sarsdf = sarsdf[sarsdf['Unnamed: 1'] == 'Cq']
    sarsdf = sarsdf.loc[:, sarsdf.columns != 'Unnamed: 1']  # changed
    sarsdf.columns = sarsdf.columns.astype('int64')

    REDdf = pd.read_excel(file,
                              sheet_name = 1)
    REDdf.rename(columns={'Unnamed: 0':'Rows'}, inplace=True)
    REDdf.set_index('Rows', inplace = True)
    REDdf = REDdf[REDdf['Unnamed: 1'] == 'Cq']
    REDdf = REDdf.loc[:, REDdf.columns != 'Unnamed: 1']  # changed
    REDdf.columns = REDdf.columns.astype('int64')


    if quadrants384_to_96Method == False: # works for both 384 and 96 methods.
        return sarsdf, REDdf, uniformitySetUp(sarsdf, REDdf, input384).round(decimals = 2)

    # focus on this part after for 384 split quadrants!!
    elif quadrants384_to_96Method == True:
        sarsQUAD1_96, sarsQUAD2_96, sarsQUAD3_96, sarsQUAD4_96 = quadrants384_to_96(sarsdf)
        redQUAD1_96, redQUAD2_96, redQUAD3_96, redQUAD4_96 = quadrants384_to_96(REDdf)
        sarsdf = [sarsQUAD1_96, sarsQUAD2_96, sarsQUAD3_96, sarsQUAD4_96]
        REDdf = [redQUAD1_96, redQUAD2_96, redQUAD3_96, redQUAD4_96]
        dfs_96 = []
        for sars, red in zip([sarsQUAD1_96, sarsQUAD2_96, sarsQUAD3_96, sarsQUAD4_96],
                            [redQUAD1_96, redQUAD2_96, redQUAD3_96, redQUAD4_96]):

            dfs_96.append(uniformitySetUp(sars, red, input384 = False).round(decimals = 2))


        return sarsdf, REDdf, dfs_96

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
