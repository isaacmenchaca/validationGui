import numpy as np
import pandas as pd

def quadrants384_to_96(data):
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
