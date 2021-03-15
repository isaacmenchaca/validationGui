import pandas as pd
import numpy as np

def quadrants384_to_96(data):
    data = data.copy()

    quad1 = []
    for row in np.arange(0, 16, 2):
        for col in np.arange(0, 23, 2):
            quad1.append(data.values[row, col])


    QUAD1_96 = pd.DataFrame(np.array(quad1).reshape([8, 12])) # 96
    QUAD1_96.columns = np.linspace(1, 12, 12, dtype = np.int)
    QUAD1_96['Row'] = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    QUAD1_96.set_index(['Row'], inplace = True)

    quad2 = []
    for row in np.arange(0, 16, 2):
        for col in np.arange(1, 24, 2):
            quad2.append(data.values[row, col])


    QUAD2_96 = pd.DataFrame(np.array(quad2).reshape([8, 12])) # 96
    QUAD2_96.columns = np.linspace(1, 12, 12, dtype = np.int)
    QUAD2_96['Row'] = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    QUAD2_96.set_index(['Row'], inplace = True)

    quad3 = []
    for row in np.arange(1, 17, 2):
        for col in np.arange(0, 23, 2):
            quad3.append(data.values[row, col])


    QUAD3_96 = pd.DataFrame(np.array(quad3).reshape([8, 12])) # 96
    QUAD3_96.columns = np.linspace(1, 12, 12, dtype = np.int)
    QUAD3_96['Row'] = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    QUAD3_96.set_index(['Row'], inplace = True)

    quad4 = []
    for row in np.arange(1, 17, 2):
        for col in np.arange(1, 24, 2):
            quad4.append(data.values[row, col])


    QUAD4_96 = pd.DataFrame(np.array(quad4).reshape([8, 12])) # 96
    QUAD4_96.columns = np.linspace(1, 12, 12, dtype = np.int)
    QUAD4_96['Row'] = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    QUAD4_96.set_index(['Row'], inplace = True)

    return QUAD1_96, QUAD2_96, QUAD3_96, QUAD4_96


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


        dfs_96 = []
        for sars, red in zip([sarsQUAD1_96, sarsQUAD2_96, sarsQUAD3_96, sarsQUAD4_96],
                            [redQUAD1_96, redQUAD2_96, redQUAD3_96, redQUAD4_96]):
            dfs_96.append(checkerSetUp(sars, red, input384 = False, sortBy = sortBy))


        return dfs_96
