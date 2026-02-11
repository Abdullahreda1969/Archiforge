import webbrowser

# Get the image files from the 'index.html' file
image_files = ['image1.jpg', 'image2.png', 'image3.gif']

# Open the images in a web browser
for image_file in image_files:
    webbrowser.open('file://' + image_file)

print('All images have been opened in a browser.')