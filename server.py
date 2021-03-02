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
    folder = filedialog.askdirectory()
    return folder

eel.start('index.html', size=(1000,800))            # Start (this blocks and enters loop)
