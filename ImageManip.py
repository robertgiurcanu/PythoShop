import io
import math
from PythoShopExports import *
import random

def get_info(image):

    image.seek(22)
    height = int.from_bytes(image.read(4), 'little')
    image.seek(18)
    width = int.from_bytes(image.read(4), 'little')
    image.seek(10)
    fpp = int.from_bytes(image.read(4), 'little')
    row_size = width * 3
    padding = 0
    if (row_size) % 4 != 0: # not evenly divisible by 4
        padding = 4 - (row_size) % 4
        row_size = row_size + padding 
    # your code: to get the fpp, width, etc. from the image
    return fpp, width, height, padding, row_size


@export_filter
def draw_centered_hline(image, color, **kwargs):
    image.seek(22)
    height = int.from_bytes(image.read(4), 'little')

    draw_hline(image, (0, height // 2), color, **kwargs)
    
@export_filter
def draw_centered_vline(image, color, **kwargs):
    image.seek(18)
    width = int.from_bytes(image.read(4), 'little')

    draw_vline(image, (width // 2, 0), color, **kwargs)

@export_filter
def mark_middle(image, color, extra, **kwargs):

    image.seek(18)
    width = int.from_bytes(image.read(4), 'little')
    image.seek(22)
    height = int.from_bytes(image.read(4), 'little')

    x_middle = width // 2
    y_middle = height // 2

    change_pixel(image, (x_middle, y_middle), color, **kwargs)


@export_tool
def draw_vline(image, clicked_coordinate, color, extra, **kwargs):
    
    try:
        extra = int(extra)
    except ValueError:
        extra = 1


    x, y = clicked_coordinate
    fpp, width, height, padding, row_size = get_info(image)
  

    bgr = bytes([color[2], color[1], color[0]])  # [B, G, R]
    # Makes the correct row_size
    row_size = width*3 + padding

    # Go to the x value
    image.seek(fpp + x * 3)
    image.write(bgr)
    for row in range(height):
        image.seek(row_size - 3, 1)
        image.write(bgr)


@export_tool
def draw_hline(image, clicked_coordinate, color, **kwargs):
    fpp, width, height, padding, row_size = get_info(image)
    # Gets all the necessary information
    x, y = clicked_coordinate
    bgr = bytes([color[2], color[1], color[0]])  # [B, G, R]

    #row_of_pixels = "FF00FF" * width
    image.seek(fpp + (row_size) * y)
    for col in range(width):
        image.write(bgr)

@export_tool
def change_pixel(image, clicked_coordinate, color, **kwargs):
    x, y = clicked_coordinate

    fpp, width, height, padding, row_size = get_info(image)

    bgr = bytes([color[2], color[1], color[0]])  # [B, G, R]
    image.seek(fpp + (width * 3 + padding)* y + 3 * x)
    image.write(bgr)

@export_filter
def fill(image, color, **kwargs):
    fpp, width, height, padding, row_size = get_info(image)
    # your code: call get_info to get the information we need
    # your code: go to the first pixel (the start of the first row)
    image.seek(fpp)
    bgr = bytes([color[2], color[1], color[0]])  # [B, G, R]

    for row in range(height):  # goes through every row in the image
        # At this point we assume we're at the start of the CURRENT row
        for pixel in range(width):  # goes through every pixel WITHIN the current row
            # your code: write one red pixel
            image.write(bgr)
            # After writing these three bytes the cursor will have moved on to the next pixel
        # your code: skip past the padding bytes so that when the loop repeats we'll be at the beginning of the next row
        image.seek(padding, 1)



@export_filter
def make_static(image, extra, color, **kwargs):
    
    try:
        max_distance = int(extra)
        
    except ValueError:
        max_distance = 255

    blue = color[2]
    green = color[1]
    red = color[0]

    fpp, width, height, padding, row_size = get_info(image)
    image.seek(fpp)


    for row in range(height):
        for pixel in range(width):
            # Make the random blue

            max_blue = 0
            low_blue = 0

            if (blue + max_distance > 255):
                max_blue = 255
            else:
                max_blue = blue + max_distance
            
            if (blue - max_distance < 0):
                low_blue = 0
            else:
                low_blue = blue - max_distance

            max_red = 0
            low_red = 0

            if (red + max_distance > 255):
                max_red = 255
            else:
                max_red = red + max_distance
            
            if (red - max_distance < 0):
                low_red = 0
            else:
                low_red = red - max_distance

            max_green = 0
            low_green = 0

            if (green + max_distance > 255):
                max_green = 255
            else:
                max_green = green + max_distance
            
            if (green - max_distance < 0):
                low_green = 0
            else:
                low_green = green - max_distance

            actual_blue = random.randint(low_blue, max_blue)
            actual_green = random.randint(low_green, max_green)
            actual_red = random.randint(low_red, max_red)

            image.write(bytes([actual_blue, actual_green, actual_red]))
        image.seek(padding, 1)


@export_filter
def remove_red(image, color, extra, **kwargs):

    fpp, width, height, padding, row_size = get_info(image)
    image.seek(fpp)
    for row in range(height):
        for pixel in range(width):
            image.seek(2, 1)
            image.write(bytes([0]))
        image.seek(padding, 1)
@export_filter
def remove_green(image, color, extra, **kwargs):
    fpp, width, height, padding, row_size = get_info(image)
    image.seek(fpp)

    for row in range(height):
        for pixel in range(width):
            image.seek(1, 1)
            image.write(bytes([0]))
            image.seek(1, 1)
        image.seek(padding, 1)


@export_filter
def remove_blue(image, color, extra, **kwargs):
    fpp, width, height, padding, row_size = get_info(image)
    image.seek(fpp)

    for row in range(height):
        for pixel in range(width):
            image.write(bytes([0]))
            image.seek(2, 1)
        image.seek(padding, 1)

@export_filter
def max_red(image, color, extra, **kwargs):
    fpp, width, height, padding, row_size = get_info(image)
    image.seek(fpp)
    for row in range(height):
        for pixel in range(width):
            image.seek(2, 1)
            image.write(bytes([255]))
        image.seek(padding, 1)
@export_filter
def max_green(image, color, extra, **kwargs):
    fpp, width, height, padding, row_size = get_info(image)
    image.seek(fpp)

    for row in range(height):
        for pixel in range(width):
            image.seek(1, 1)
            image.write(bytes([255]))
            image.seek(1, 1)
        image.seek(padding, 1)


@export_filter
def max_blue(image, color, extra, **kwargs):
    fpp, width, height, padding, row_size = get_info(image)
    image.seek(fpp)

    for row in range(height):
        for pixel in range(width):
            image.write(bytes([255]))
            image.seek(2, 1)
        image.seek(padding, 1)


@export_filter
def negate_red(image, **kwargs):
    fpp, width, height, padding, row_size = get_info(image)

    image.seek(fpp)
    for row in range(height):
        for pixel in range(width):
            blue, green, red = image.read(3)
            r1 = 255 - red
            image.seek(-3, 1)
            image.write(bytes([blue, green, r1]))
        image.seek(padding, 1)
        
@export_filter
def draw_gray(image, clicked_coordinate,color, extra, **kwargs):
   fpp, width, height, padding, row_size = get_info(image)
   try:
       radius = int(extra)
   except:
       radius = 1
   x, y = clicked_coordinate
   image.seek(fpp)
   
   for row in range(height):
       for pixel in range(width):
           blue, green, red = image.read(3)
           image.seek(-3, 1)
           lumen = blue + green + red
           average = int(lumen/3)
           distance = math.sqrt((x - pixel) ** 2 + (y - row) ** 2)

           if distance <= radius:
               image.write(bytes([average, average, average]))
           else:
               image.seek(3, 1)
       image.seek(padding, 1)




@export_filter
def negate_green(image, **kwargs):
    fpp, width, height, padding, row_size = get_info(image)

    image.seek(fpp)
    for row in range(height):
        for pixel in range(width):
            blue, green, red = image.read(3)
            g1 = 255 - green
            image.seek(-3, 1)
            image.write(bytes([blue, g1, red]))
        image.seek(padding, 1)

@export_filter
def negate_blue(image, **kwargs):
    fpp, width, height, padding, row_size = get_info(image)

    image.seek(fpp)
    for row in range(height):
        for pixel in range(width):
            blue, green, red = image.read(3)
            b1 = 255 - blue
            
            image.seek(-3, 1)
            image.write(bytes([b1, green, red]))
        image.seek(padding, 1)

@export_filter
def lighten(image, **kwargs):


    fpp, width, height, padding, row_size = get_info(image)

    image.seek(fpp)

    for row in range(height):
        for pixel in range(width):
            blue, green, red = image.read(3)

            b1 = int(blue * 1.5)
            g1 = int(green * 1.5)
            r1 = int(red * 1.5)
            if (b1 > 255):
                b1 = 255
            if (g1 > 255):
                g1 = 255
            if (r1 > 255):
                r1 = 255

            image.seek(-3, 1)
            image.write(bytes([b1, g1, r1]))
        image.seek(padding, 1)






@export_filter
def make_gray(image, **kwargs):
    fpp, width, height, padding, row_size = get_info(image)

    image.seek(fpp)

    for row in range(height):
        for pixel in range(width):
                blue, green, red = image.read(3)
                average = round((blue + green + red) / 3)
                image.seek(-3, 1)
                image.write(bytes([average, average, average]))
        image.seek(padding, 1)


@export_filter
def darken(image, **kwargs):
    fpp, width, height, padding, row_size = get_info(image)

    image.seek(fpp)

    for row in range(height):
        for pixel in range(width):
            blue, green, red = image.read(3)

            b1 = int(blue * 0.5)
            g1 = int(green * 0.5)
            r1 = int(red * 0.5)
            
            image.seek(-3, 1)
            image.write(bytes([b1, g1, r1]))
        image.seek(padding, 1)




@export_filter
def negate(image, **kwargs):
    fpp, width, height, padding, row_size = get_info(image)

    image.seek(fpp)
    for row in range(height):
        for pixel in range(width):
            blue, green, red = image.read(3)
            b1 = 255 - blue
            g1 = 255 - green
            r1 = 255 - red
            image.seek(-3, 1)
            image.write(bytes([b1, g1, r1]))
        image.seek(padding, 1)







@export_filter
def intensify(image, color, extra, **kwargs):
    fpp, width, height, padding, row_size = get_info(image)
    image.seek(fpp)
    for row in range(height):
        for pixel in range(width):
            blue, green, red = image.read(3)
            if blue > 127.5:
                blue = 255
            else:
                blue = 0
            if green > 127.5:
                green = 255
            else:
                green = 0
            if red > 127.5:
                red = 255
            else:
                red = 0
            image.seek(-3, 1)  # go back 3 bytes
            image.write(bytes([blue, green, red]))  # write all three at once
        image.seek(padding, 1)

@export_filter
def make_two_tone(image, color, extra, **kwargs):
    fpp, width, height, padding, row_size = get_info(image)
    image.seek(fpp)
    for row in range(height):
        for pixel in range(width):
            blue, green, red = image.read(3)
            image.seek(-3, 1)  # go back 3 bytes
            if blue + green + red > 382.5:
                blue = 255
                green = 255
                red = 255
            else:
                blue = 0
                green = 0
                red = 0
            image.write(bytes([blue, green, red]))  # write all three at once
        image.seek(padding, 1)

@export_filter
def make_four_tone(image, **kwargs):
    fpp, w, h, padding, row_size = get_info(image)
    image.seek(fpp)
    for row in range(h):
        for pixel in range(w):
            blue, green, red = image.read(3)
            brightness = blue + green + red
            if brightness > 573.75:
                new_color = 255
            elif brightness > 382.5:
                new_color = 170
            elif brightness > 191.25:
                new_color = 85
            else:
                new_color = 0
            image.seek(-3, 1)
            image.write(bytes([new_color, new_color, new_color]))
        image.seek(padding, 1)

@export_filter
def make_better_two_tone(image, **kwargs):
    
    fpp, w, h, padding, row_size = get_info(image)
    image.seek(fpp)
    tb = 0
    for row in range(h):
        for pixel in range(w):
            b,g,r = image.read(3)
            cb = b+g+r
            tb += cb
        image.seek(padding, 1)
    avg = tb/(w*h)
    avg = int(avg)
    image.seek(fpp)
    for row in range(h):
        for pixel in range(w):
            blue, green, red = image.read(3)

            image.seek(-3, 1)
            if (blue + green + red > avg):
                blue = 255
                green = 255
                red = 255
            else:
                blue = 0
                green = 0
                red = 0

            image.write(bytes([blue, green, red]))
        image.seek(padding, 1)

def create_bmp(width, height):
    row_size = width * 3
    row_padding = 0
    if row_size % 4 != 0:
        row_padding = 4 - row_size % 4
        row_size += row_padding
    bmp = io.BytesIO(b'\x42\x4D'+(138 + row_size * height).to_bytes(4, byteorder="little"))
    bmp.seek(10)
    bmp.write((138).to_bytes(4, byteorder="little"))  # starting pixel
    bmp.write((124).to_bytes(4, byteorder="little"))  # header size (for version 5)
    bmp.write(width.to_bytes(4, byteorder="little"))
    bmp.write(height.to_bytes(4, byteorder="little"))
    bmp.write((1).to_bytes(2, byteorder="little"))  # color planes must be 1
    bmp.write((24).to_bytes(2, byteorder="little"))  # bits per pixel
    bmp.write((0).to_bytes(4, byteorder="little"))  # compression (none)
    bmp.seek(138)
    bmp.write(bytes(([0, 0, 0]) * width + [0] * row_padding) * height)
    bmp.seek(0)
    return bmp

@export_filter
def blend_other(image, other_image, **kwargs):
    image1 = image
    image2 = other_image
    fpp1, w1, h1, padding1, row_size1 = get_info(image1)
    fpp2, w2, h2, padding2, row_size2 = get_info(image2)
    image1.seek(fpp1)
    image2.seek(fpp2)
    image3 = create_bmp(w1, h1)
    fpp3, w3, h3, padding3, row_size3 = get_info(image3)


    image3.seek(fpp3)
    for row in range(h1):
        for pixel in range(w1):
            b1, g1, r1 = image1.read(3)
            b2, g2, r2 = image2.read(3)
            blue1 = int((b1+b2)/2)
            green1 = int((g1 + g2)/2)
            red1 = int((r1+r2)/2)

            image3.write(bytes([blue1, green1, red1]))
        image1.seek(padding1, 1)
        image2.seek(padding2, 1)
        image3.write(bytes(padding3))
    
    return image3
@export_filter
def borders(image, color, extra, **kwargs):
   fpp, width, height, row_size, padding = get_info(image)


   draw_vline(image, (0,0), color, extra)


   draw_hline(image, (0,0), color, extra)
   draw_hline(image, (0,height-1), color, extra)
   draw_vline(image, (width-1, 0), color, extra)

@export_filter
def chroma_overlay(image, other_image, **kwargs):
    green_screened = other_image
    background_image = image

   
    fpp1, w1, h1, padding1, row_size1 = get_info(green_screened)
    fpp2, w2, h2, padding2, row_size2 = get_info(background_image)
    
    image3 = create_bmp(w1, h1)
    fpp3, w3, h3, padding3, row_size3 = get_info(image3)
    
    
    green_screened.seek(fpp1)
    background_image.seek(fpp2)
    image3.seek(fpp3)

    for row in range(h1):
        for pixel in range(w1):
            b1, g1, r1 = green_screened.read(3)
            b2, g2, r2 = background_image.read(3)
            if (g1 - b1 >= 100) and (g1 - r1 >= 100):
                image3.write(bytes([b2, g2, r2]))
                
            else:
                image3.write(bytes([b1, g1, r1]))
        green_screened.seek(padding1, 1)
        background_image.seek(padding2, 1)
        image3.seek(padding3, 1)

    return image3

@export_filter
def fade_in_vertical(image, **kwargs):
    fpp1, w1, h1, padding1, row_size1 = get_info(image)
    image.seek(fpp1)

    for row in range(h1):
        percent = row / (h1 - 1)
        for pixel in range(w1):
            b1, g1, r1 = image.read(3)
            image.seek(-3, 1)
            blue = int(percent * b1)
            green = int(percent * g1)
            red = int(percent * r1)
            image.write(bytes([blue, green, red]))
        
        image.seek(padding1, 1)
@export_filter
def swap_rgb(image, extra, **kwargs):
   fpp, width, height, padding, row_size = get_info(image)
   image.seek(fpp)
   for row in range(height):
       for pixel in range(width):
           blue, green, red = image.read(3)
           new_blue = red
           new_red = blue
           image.seek(-3, 1)  # go back 3 bytes
           image.write(bytes([new_blue, green, new_red]))  # write all three at once


       image.seek(padding, 1)

@export_filter
def swap_brg(image, extra, **kwargs):
   fpp, width, height, padding, row_size = get_info(image)
   image.seek(fpp)
   for row in range(height):
       for pixel in range(width):
           blue, green, red = image.read(3)
           new_green = red
           new_red = green
           image.seek(-3, 1)  # go back 3 bytes
           image.write(bytes([blue, new_green, new_red]))  # write all three at once


       image.seek(padding, 1)

@export_filter
def swap_rbg(image, extra, **kwargs):
   fpp, width, height, padding, row_size = get_info(image)
   image.seek(fpp)
   for row in range(height):
       for pixel in range(width):
           blue, green, red = image.read(3)
           new_blue = red
           new_green = blue
           new_red = green
           image.seek(-3, 1)  # go back 3 bytes
           image.write(bytes([new_blue, new_green, new_red]))  # write all three at once


       image.seek(padding, 1)

@export_filter
def swap_grb(image, extra, **kwargs):
   fpp, width, height, padding, row_size = get_info(image)
   image.seek(fpp)
   for row in range(height):
       for pixel in range(width):
           blue, green, red = image.read(3)
           new_blue = green
           new_green = red
           new_red = blue
           image.seek(-3, 1)  
           image.write(bytes([new_blue, new_green, new_red])) 

       image.seek(padding, 1)

@export_filter
def grayify(image, **kwargs):
    fpp, width, height, padding, row_size = get_info(image)

    image.seek(fpp)

    for row in range(height):
        for pixel in range(width):
                blue, green, red = image.read(3)
                average = round((blue + green + red) / 3)
                image.seek(-3, 1)

                # Now make it halfway to the average
                if (blue > average):
                    diff = int((blue - average) / 2)
                    blue -= diff
                else:
                    diff = int((average - blue) / 2)
                    blue += diff

                if (green > average):
                    diff = int((green - average) / 2)
                    green -= diff
                else:
                    diff = int((average - green) / 2)
                    green += diff
                if (red > average):
                    diff = int((red - average) / 2)
                    red -= diff
                else:
                    diff = int((average - red) / 2)
                    red += diff
                image.write(bytes([blue, green, red]))
        image.seek(padding, 1)


@export_filter
def redify(image, **kwargs):

    fpp, width, height, padding, row_size = get_info(image)
    image.seek(fpp)

    for row in range(height):

        for pixel in range(width):

            blue, green, red = image.read(3)
            brightness = red + green + blue

            if brightness <= 382.5:
               
                percent = brightness/382.5
                red = int(percent * 255)
                green = 0
                blue = 0
            else:
                
                red = 255
                extra_brightness = brightness - 382.5
                percent = extra_brightness / 382.5

                green = int(percent * 255)  
                blue = int(percent * 255)
            
            image.seek(-3, 1)
            image.write(bytes([blue, green, red]))
        
        image.seek(padding, 1)


@export_filter
def blueify(image, **kwargs):
    fpp, width, height, padding, row_size = get_info(image)
    image.seek(fpp)

    for row in range(height):
        for pixel in range(width):
            blue, green, red = image.read(3)
            brightness = red + green + blue

            if brightness <= 382.5:
                percent = brightness / 382.5
                blue = int(percent * 255)
                green = 0
                red = 0
            else:
                blue = 255
                extra_brightness = brightness - 382.5
                percent = extra_brightness / 382.5
                green = int(percent * 255)
                red = int(percent * 255)

            image.seek(-3, 1)
            image.write(bytes([blue, green, red]))

        image.seek(padding, 1)

@export_filter
def greenify(image, **kwargs):
    fpp, width, height, padding, row_size = get_info(image)
    image.seek(fpp)

    for row in range(height):
        for pixel in range(width):
            blue, green, red = image.read(3)
            brightness = red + green + blue

            if brightness <= 382.5:
                percent = brightness / 382.5
                green = int(percent * 255)
                red = 0
                blue = 0
            else:
                green = 255
                extra_brightness = brightness - 382.5
                percent = extra_brightness / 382.5
                red = int(percent * 255)
                blue = int(percent * 255)

            image.seek(-3, 1)
            image.write(bytes([blue, green, red]))

        image.seek(padding, 1)


@export_filter
def magentify(image, **kwargs):
    fpp, width, height, padding, row_size = get_info(image)
    image.seek(fpp)

    for row in range(height):
        for pixel in range(width):
            blue, green, red = image.read(3)
            brightness = red + green + blue

            if brightness <= 382.5:
                
                percent = brightness / 382.5
                red = int(percent * 255)
                green = 0
                blue = int(percent * 255)
            else:
                red = 255
                blue = 255
                extra_brightness = brightness - 382.5
                percent = extra_brightness / 382.5
                green = int(percent * 255)

            image.seek(-3, 1)
            image.write(bytes([blue, green, red]))

        image.seek(padding, 1)

@export_filter
def mirror_right_horizontal(image, **kwargs):
    fpp, width, height, padding, row_size = get_info(image)
    image.seek(fpp)

    for row in range(height):
        for pixel in range(width//2):
            b, g, r = image.read(3)
            image.write(bytes[b, g, r])
