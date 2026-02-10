#Goals:
# load image using PIL
# resize image and keep ratio
# convert image to greyscale
# convert greyscale values to ascii chars 
# save as text
# print to terminal
from PIL import Image
ASCII_ARR = " .:-=+*#%@"
NEW_SIZE = 128
file_name = "asuka.png" #put path to file here -required
target_txt = "asciisuka.txt" #put txt file name here -required


def resize_preserve(new_size, im):
    width, height = im.size
    img_ratio = width / height
    if img_ratio <= 1:
        width = new_size
        height = new_size * img_ratio
    elif img_ratio > 1:
        height = new_size
        width = new_size * img_ratio
        
    width = int(width)
    height = int(height)
    return width, height

def convert_ascii(image):
    range = 25.5 #255/10
    pixels = image.getdata()
    string_ascii = ""
    count = 0
    for i in pixels:
        current_pixel = i[0]
        current_pixel = int(current_pixel // range)

        if current_pixel >= len(ASCII_ARR):
            current_pixel = len(ASCII_ARR) -1
    
        string_ascii += ASCII_ARR[current_pixel] 

        count +=1
        if count % image.width == 0:
            string_ascii += "\n"
        
    return string_ascii

# intensity equation that turns RGB into greyscale = (0.299 * R) + (0.587 * G) + (0.114 * B)
# pixel format: (R, G, B)
def to_greyscale(image):
    new_pixels = []
    new_image = image.copy()
    pixels = new_image.getdata()
    for i in pixels:
        greyscale_value = (0.299 * i[0] + 0.587 * i[1] + 0.114 * i[2])
        greyscale_value = int(greyscale_value)
        new_pixels.append((greyscale_value, greyscale_value, greyscale_value))
    new_image.putdata(new_pixels)
    return new_image

def resize_image(NEW_SIZE):
    with Image.open(file_name) as im:   
        im_scaled = im.resize(resize_preserve(NEW_SIZE, im))
        im_scaled.save("resized_imag.png")

def greyscale_image():
    with Image.open(file_name) as im: 
        im_greyscale = to_greyscale(im)
        im_greyscale.save("greyscaled_image.png")   

def to_ascii(file_name, target_txt):
    with Image.open(file_name) as im:
        width = 100
        resized_im = im.resize(resize_preserve(width, im))
        greyscale_im = to_greyscale(resized_im)
        ascii_string = convert_ascii(greyscale_im)


    with open(target_txt, "w") as txt:
        txt.write(ascii_string)
        print(ascii_string)


def main():
    to_ascii(file_name, target_txt)
    
  
     
main()

