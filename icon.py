from PIL import Image

# Replace 'path/to/your/icon.png' with the actual path to your icon file
input_icon_path = 'assets/ship.png'
output_icon_path = 'assets/icon.ico'

# Open and save the image in .ico format
Image.open(input_icon_path).save(output_icon_path, format='ICO')
