#Goals:
# load image using PIL
# resize image and keep ratio
# convert image to greyscale
# convert greyscale values to ascii chars 
# save as text
# print to terminal
from PIL import Image
ASCII_ARR = " .:-=+*#%@"
size = 100
file_name = "asuka.png"                         #put path to image here -required
target_txt = "asciisuka.txt"                    #put path to created txt file name here -required
target_colour__txt = "asciisuka_colour.txt"

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
def convert_greyscale(image):
    new_pixels = []
    new_image = image.copy()
    pixels = new_image.getdata()
    for i in pixels:
        greyscale_value = (0.299 * i[0] + 0.587 * i[1] + 0.114 * i[2])
        greyscale_value = int(greyscale_value)
        new_pixels.append((greyscale_value, greyscale_value, greyscale_value))
    new_image.putdata(new_pixels)
    return new_image

 #we project the ansi colours and the pixel colour rgb onto a 3D plane - then we can use euclidian geometry to calculate the closest colour
def get_closest_colour(pixel_colour):
    ansi_colours = {
    'red': (255, 0, 0),
    'green': (0, 255, 0),
    'blue': (0, 0, 255),
    } 
    pixel_rgb = pixel_colour
    min_distance = float('inf')
    
    for ansi_colour, ansi_rgb in ansi_colours.items():
        for c1, c2 in zip(pixel_rgb, ansi_rgb):
            distance = 0
            distance += (c1 - c2) ** 2

        if distance < min_distance:
            min_distance = distance
            closest_color = ansi_colour      
    return closest_color

def convert_ascii_colour(image):
    range = 25.5 #255/10
    pixels = image.getdata()
    string_ascii = ""
    count = 0

    for pixel_colour in pixels:
        current_pixel = pixel_colour[0]
        current_pixel = int(current_pixel // range)

        if current_pixel >= len(ASCII_ARR):
            current_pixel = len(ASCII_ARR) -1

        #I really, really hated having to write this out (ansi escape sequence + ascii character + ansi exit sequence):
        colour_code = f"\033[38;2;{pixel_colour[0]};{pixel_colour[1]};{pixel_colour[2]}m" 
        string_ascii += f"{colour_code}{ASCII_ARR[current_pixel]}\033[0m"   


        count +=1
        if count % image.width == 0:
            string_ascii += "\n"
        
    return string_ascii





#stacked functions
def resize_image(size=128):
    with Image.open(file_name) as im:   
        im_scaled = im.resize(resize_preserve(size, im))
        im_scaled.save("resized_imag.png")

def to_greyscale(file_name):
    with Image.open(file_name) as im: 
        im_greyscale = convert_greyscale(im)
        im_greyscale.save("greyscaled_image.png")   

def to_ascii(file_name, target_txt, width):
    with Image.open(file_name) as im:

        resized_im = im.resize(resize_preserve(width, im))
        greyscale_im = convert_greyscale(resized_im)
        ascii_string = convert_ascii(greyscale_im)
    with open(target_txt, "w") as txt:
        txt.write(ascii_string)
        print(ascii_string)

def to_ascii_colour(file_name, target_txt, width):
    with Image.open(file_name) as im:

        resized_im = im.resize(resize_preserve(width, im))
        ascii_string = convert_ascii_colour(resized_im)
        print(ascii_string)


def main():

    #resize_image(size)
    #to_greyscale(file_name)
    #to_ascii(file_name, target_txt, width=100)
    to_ascii_colour(file_name, target_colour__txt, width=100)
    
    

  
     
main()

