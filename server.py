import eel
import tkinter as tk
from tkinter import filedialog
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

@eel.expose
def getValidationInputs(textValidationType, textPlateType, textQuadrantSplitType, filePath):
    print(textValidationType, textPlateType, textQuadrantSplitType, filePath)

    if textValidationType == 'Accuracy':
        if textPlateType == 96:
            print('FIXME: Run python Accuracy 96 method')
        elif textPlateType == 384:
            if textQuadrantSplitType == "No":
                print('FIXME: Run python Accuracy 384 method')
            elif textQuadrantSplitType == "Yes":
                print('FIXME: Run python Accuracy 384 method with Quadrants split')

    elif textValidationType == 'Uniformity':
        if textPlateType == 96:
            print('FIXME: Run python Uniformity 96 method')
        elif textPlateType == 384:
            if textQuadrantSplitType == "No":
                print('FIXME: Run python Uniformity 384 method')
            elif textQuadrantSplitType == "Yes":
                print('FIXME: Run python Uniformity 384 method with Quadrants split')

    elif textValidationType == 'Checkerboard':
        if textPlateType == 96:
            print('FIXME: Run python Checkerboard 96 method')
        elif textPlateType == 384:
            if textQuadrantSplitType == "No":
                print('FIXME: Run python Checkerboard 384 method')
            elif textQuadrantSplitType == "Yes":
                print('FIXME: Run python Checkerboard 384 method with Quadrants split')

    print('/n')
    return






eel.start('index.html', size=(1000,800))            # Start (this blocks and enters loop)
