import eel

# Set web files folder and optionally specify which file types to check for eel.expose()
#   *Default allowed_extensions are: ['.js', '.html', '.txt', '.htm', '.xhtml']
eel.init('web')

@eel.expose
def pythonPrintsValue(a, b):
    print(a, b, a + b)
    return

eel.start('index.html', size=(1000,800))            # Start (this blocks and enters loop)
