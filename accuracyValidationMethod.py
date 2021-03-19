import pandas as pd # version 0.25.1
import numpy as np # version 1.18.4
from quadrants384_to_96 import quadrants384_to_96

def mapValidation(mapAcc):
# map validation, mapping A
    num_control, num_neg, num_100, num_200, num_2000, num_20000 = 0, 0, 0, 0, 0, 0
    for row in mapAcc.values:
        #print(row)
        for value in row:
            if value == 'control':
                num_control += 1

            elif value == 'neg':
                num_neg += 1

            elif value == 100:
                num_100 += 1

            elif value == 200:
                num_200 += 1

            elif value == 2000:
                num_2000 += 1

            elif value == 20000:
                num_20000 += 1

    # print(num_control, num_neg, num_100, num_200, num_2000, num_20000)

    assert num_control == 4, 'There is an invalid number of controls in Accuracy Mapping.'
    assert num_neg == 30, 'There is an invalid number of negatives in Accuracy Mapping.'
    assert num_100 == 20, 'There is an invalid number of 100 cps in Accuracy Mapping.'
    assert num_200 == 20, 'There is an invalid number of 200 cps in Accuracy Mapping.'
    assert num_2000 == 5, 'There is an invalid number of 2000 cps in Accuracy Mapping.'
    assert num_20000 == 5, 'There is an invalid number of 20000 cps in Accuracy Mapping.'

    return

def formatAccuracyReport(mapAcc, FAMdf, REDdf):

    idStart_neg, idStart_100cps, idStart_200cps, idStart_2000cps, idStart_20000cps = 1, 31, 51, 71, 76
    controlsWells_list = []
    controlSpecimenNumber_list = [] # keeping these two separate because we are unable to sort integers with strings.
                        # Will prepend this to our list instead.
    control_FAM_CT = []
    control_CalRed_CT = []
    control_specimen_in_concentration = []
    control_specimenResult = []

    wells_list = []
    specimenNumber_list = []
    FAM_CT = []
    CalRed_CT = []
    specimen_in_concentration = []
    specimen_in_concentration_cps = []
    specimen_result = []


    for index, row in mapAcc.iterrows():
        for i in range(1,13):
            mapValue = mapAcc.loc[index,i]
            correspondingValue = FAMdf.loc[index,i]
            correspondingRedValue = REDdf.loc[index,i]
            #print(mapValue, correspondingValue)

            if mapValue == 'control': # CONTROLS
                controlsWells_list.append(index + str(i))
                controlSpecimenNumber_list.append('Control')

                if (index == 'A' or index == 'C'):
                    control_specimen_in_concentration.append('Negative')
                elif (index == 'B' or index == 'D'):
                    control_specimen_in_concentration.append('Positive')


                control_FAM_CT.append(correspondingValue)
                control_CalRed_CT.append(correspondingRedValue)

                if np.isnan(correspondingValue):
                    control_specimenResult.append('Negative')
                else:
                    control_specimenResult.append('Positive')

            elif mapValue == 'neg': # NEGATIVES
                wells_list.append(index + str(i))
                specimenNumber_list.append(idStart_neg)
                idStart_neg += 1

                FAM_CT.append(correspondingValue)


                CalRed_CT.append(correspondingRedValue)

                specimen_in_concentration.append('Negative')
                specimen_in_concentration_cps.append('Negative')

                if np.isnan(correspondingValue):
                    specimen_result.append('Negative')
                elif correspondingValue > 40:
                    specimen_result.append('Negative')
                else:
                    specimen_result.append('Positive')

            elif not(np.isnan(mapValue)):   # checking if it not nan
                wells_list.append(index + str(i))
                FAM_CT.append(correspondingValue)
                CalRed_CT.append(correspondingRedValue) # leave out for now.
                specimen_in_concentration.append('Positive')
                specimen_in_concentration_cps.append(int(mapValue))

                if np.isnan(correspondingValue):
                    specimen_result.append('Negative')
                elif correspondingValue >= 40:
                    specimen_result.append('Negative')
                else:
                    specimen_result.append('Positive')


                if mapValue == 100:
                    specimenNumber_list.append(idStart_100cps)
                    idStart_100cps += 1

                elif mapValue == 200:
                    specimenNumber_list.append(idStart_200cps)
                    idStart_200cps += 1

                elif mapValue == 2000:
                    specimenNumber_list.append(idStart_2000cps)
                    idStart_2000cps += 1

                elif mapValue == 20000:
                    specimenNumber_list.append(idStart_20000cps)
                    idStart_20000cps += 1


    # sort everything by specimenNumber_list sorted indices.
    sort_accuracy = np.argsort(specimenNumber_list)
    specimenNumber_list = np.sort(specimenNumber_list)


    wells_list = np.array(wells_list)[sort_accuracy]
    FAM_CT = np.array(FAM_CT)[sort_accuracy]
    CalRed_CT = np.array(CalRed_CT)[sort_accuracy]
    specimen_in_concentration = np.array(specimen_in_concentration)[sort_accuracy]

    specimen_in_concentration_cps = np.array(specimen_in_concentration_cps)[sort_accuracy]
    specimen_result = np.array(specimen_result)[sort_accuracy]


    results_dict = {}
    #results_dict['Well Location'] = np.concatenate((np.array(controlsWells_list), wells_list))
    results_dict['Specimen Number'] = np.concatenate((np.array(controlSpecimenNumber_list), specimenNumber_list))
    results_dict['Specimen Concentration (cps/ mL)'] = np.concatenate((np.array(control_specimen_in_concentration),
                                                   specimen_in_concentration))


    results_dict['CT Value SARS-CoV-2'] = np.concatenate((np.array(control_FAM_CT), FAM_CT))
    results_dict['CT Value RNASE P'] = np.concatenate((np.array(control_CalRed_CT), CalRed_CT))
    results_dict['Result'] = np.concatenate((np.array(control_specimenResult), specimen_result))

    results_dict['REPEAT Ct VALUE SARS-CoV-2'] = []



    for i, (specimen_num, true_specimen, result_specimen, FAM, RED) in enumerate(zip(results_dict['Specimen Number'],
                                                        results_dict['Specimen Concentration (cps/ mL)'],
                                                        results_dict['Result'], results_dict['CT Value SARS-CoV-2'],
                                                        results_dict['CT Value RNASE P'])):

        if i < 4: # controls
            results_dict['REPEAT Ct VALUE SARS-CoV-2'].append('N/A') # controls.

        elif not(np.isnan(RED)): # if human sample is detected, proceed
            if true_specimen == result_specimen:
                if true_specimen == 'Negative':
                    if np.isnan(FAM) or FAM >= 40:
                        results_dict['REPEAT Ct VALUE SARS-CoV-2'].append('N/A') # PASS

                elif FAM < 36: # covid CT < 36 and cal red is present
                    results_dict['REPEAT Ct VALUE SARS-CoV-2'].append('N/A') # PASS

                elif FAM >= 36 and FAM < 40: # covid CT in repeat range and cal red is present
                    if int(specimen_num) <= 70: # checking if its not the 2000 or 20000 cps.

                        if int(specimen_num) < 31 or int(specimen_num) > 50:
                         # 1/28/2021
                            results_dict['REPEAT Ct VALUE SARS-CoV-2'].append('REPEAT') # 1/28/2021
                            results_dict['Result'][i] = 'REPEAT' # 1/28/2021
                        else:
                            results_dict['REPEAT Ct VALUE SARS-CoV-2'].append('N/A')

#                         results_dict['REPEAT Ct VALUE SARS-CoV-2'].append('REPEAT') # 1/28/2021
#                         results_dict['Result'][i] = 'REPEAT' # 1/28/2021

                    else: # if 2000 or 20000 cps, this is an automatic fail despite repeat.
                        #results_dict['REPEAT Ct VALUE SARS-CoV-2'].append('REPEAT/FAIL') # still a fail on accuracy but write repeat anyway
                        results_dict['REPEAT Ct VALUE SARS-CoV-2'].append('FAIL')
                elif FAM >= 40:
                    results_dict['REPEAT Ct VALUE SARS-CoV-2'].append('FAIL')

            else: # if it does not equal it.
                # check for repeats
                if FAM >= 36 and FAM < 40: # covid CT in repeat range and cal red is present
                    if int(specimen_num) < 31 or int(specimen_num) > 50:
                         # 1/28/2021
                        results_dict['REPEAT Ct VALUE SARS-CoV-2'].append('REPEAT') # 1/28/2021
                        results_dict['Result'][i] = 'REPEAT' # 1/28/2021
                    else:
                        results_dict['REPEAT Ct VALUE SARS-CoV-2'].append('N/A')


                else:
                    results_dict['REPEAT Ct VALUE SARS-CoV-2'].append('FAIL')
        else: # if no human sample is detected, test fails
            results_dict['REPEAT Ct VALUE SARS-CoV-2'].append('FAIL')

    results_dict['Specimen Concentration (cps/ mL)'] = np.concatenate((np.array(control_specimen_in_concentration),
                                                   specimen_in_concentration_cps))

    results_dict['REPEAT Ct VALUE RNASE P'] = results_dict['REPEAT Ct VALUE SARS-CoV-2'].copy()
    results_dict['REPEAT RESULT'] = results_dict['REPEAT Ct VALUE SARS-CoV-2'].copy()

    pd.set_option("display.max_rows", None, "display.max_columns", None)
    accuracy_report = pd.DataFrame(results_dict)

    pd.options.display.float_format = '{:,.2f}'.format
    accuracy_report = accuracy_report.round(decimals = 2)

    return accuracy_report

def accuracyValidationMethod_96(mapAcc, file: str):
    mapValidation(mapAcc) # helper method to make sure the assert is good. this is a double check ;)

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

    accuracy_report = formatAccuracyReport(mapAcc, FAMdf, REDdf) # helper method
    return FAMdf, REDdf, accuracy_report.fillna('N/A')

def accuracyValidationMethod_384(accuracyMap_Quad1: str,
                                accuracyMap_Quad2: str,
                                accuracyMap_Quad3: str,
                                accuracyMap_Quad4: str,
                                file: str, format_384: bool = False):


    accuracyMap_Quad1 = pd.read_excel(accuracyMap_Quad1, index_col = 'Rows')
    accuracyMap_Quad2 = pd.read_excel(accuracyMap_Quad2, index_col = 'Rows')
    accuracyMap_Quad3 = pd.read_excel(accuracyMap_Quad3, index_col = 'Rows')
    accuracyMap_Quad4 = pd.read_excel(accuracyMap_Quad4, index_col = 'Rows')



    FAMdf_384 = pd.read_excel(file)
    FAMdf_384.rename(columns={'Unnamed: 0':'Rows'}, inplace=True)
    FAMdf_384.set_index('Rows', inplace = True)
    FAMdf_384 = FAMdf_384[FAMdf_384['Unnamed: 1'] == 'Cq']
    FAMdf_384_filtered = FAMdf_384.loc[:, FAMdf_384.columns != 'Unnamed: 1']


    REDdf_384 = pd.read_excel(file, sheet_name = 1)
    REDdf_384.rename(columns={'Unnamed: 0':'Rows'}, inplace=True)
    REDdf_384.set_index('Rows', inplace = True)
    REDdf_384 = REDdf_384[REDdf_384['Unnamed: 1'] == 'Cq']
    REDdf_384_filtered = REDdf_384.loc[:, FAMdf_384.columns != 'Unnamed: 1']

    accuracy_reports = []
    for FAM, RED, MAP in zip(quadrants384_to_96(FAMdf_384_filtered),
                         quadrants384_to_96(REDdf_384_filtered),
                    [accuracyMap_Quad1, accuracyMap_Quad2, accuracyMap_Quad3, accuracyMap_Quad4]):

        accuracy_reports.append(formatAccuracyReport(mapAcc = MAP, FAMdf = FAM, REDdf = RED).fillna('N/A'))



    if format_384 == True:
        accuracy_reports = pd.concat(accuracy_reports)
        accuracy_reports_controls = accuracy_reports[accuracy_reports['Specimen Number'] == 'Control']
        accuracy_reports = accuracy_reports[accuracy_reports['Specimen Number'] != 'Control']
        accuracy_reports['Specimen Number'] = accuracy_reports['Specimen Number'].astype(int)
        accuracy_reports.sort_values(by = ['Specimen Number'], inplace =True)

        # accuracy_reports = pd.concat([accuracy_reports_controls, accuracy_reports])


        accuracy_reports['Specimen Number'] = np.linspace(1, len(accuracy_reports['Specimen Number']),
                                                         len(accuracy_reports['Specimen Number']), dtype=int)
        accuracy_reports = pd.concat([accuracy_reports_controls, accuracy_reports])

    return accuracy_reports

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
