import pandas as pd # version 0.25.1
import numpy as np # version 1.18.4
pd.set_option("display.max_rows", None, "display.max_columns", None)
pd.options.display.float_format = '{:,.2f}'.format

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

def printStats(sarsdf, REDdf):
    print('Sars Mean:', sarsdf.values.mean(), '±', sarsdf.values.std())
    print('Sars Max - Min:', sarsdf.values.max() - sarsdf.values.min())
    print(sarsdf.values.max(), sarsdf.values.min())
    print()

    print('Cal Red Mean:', REDdf.values.mean(), '±', REDdf.values.std())
    print('Cal Red Max - Min:', REDdf.values.max() - REDdf.values.min())
    print(REDdf.values.max(), REDdf.values.min())
    return

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

    checker_dict = {
        'Well': wellLocation,
        'CT Value SARS-CoV-2': FAM_CT,
        'CT Value RNASE P': CalRed_CT,
        'Well row': wellLocationRow,
        'Well col': wellLocationCol,
        'Result': specimen_result
    }

    df = pd.DataFrame(checker_dict).sort_values(by = ['Well row','Well col']).\
            fillna('N/A')[['Well', 'CT Value SARS-CoV-2', 'CT Value RNASE P',
                          'Result']]
    return df

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
        # printStats(sarsdf, REDdf)
        return sarsdf, REDdf, uniformitySetUp(sarsdf, REDdf, input384).round(decimals = 2)

    # focus on this part after for 384 split quadrants!!
    elif quadrants384_to_96Method == True:
        dfs_96 = []

        sarsQUAD1_96, sarsQUAD2_96, sarsQUAD3_96, sarsQUAD4_96 = quadrants384_to_96(sarsdf)
        redQUAD1_96, redQUAD2_96, redQUAD3_96, redQUAD4_96 = quadrants384_to_96(REDdf)

        for sars, red in zip([sarsQUAD1_96, sarsQUAD2_96, sarsQUAD3_96, sarsQUAD4_96],
                            [redQUAD1_96, redQUAD2_96, redQUAD3_96, redQUAD4_96]):
            # printStats(sars, red)

            dfs_96.append(uniformitySetUp(sars, red, input384 = False).round(decimals = 2))


        return sarsdf, REDdf#dfs_96
