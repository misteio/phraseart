from PIL import Image, ImageDraw, ImageFont, ImageEnhance
from django.conf import settings
from django.utils.text import slugify
from pathlib import Path
from resizeimage import resizeimage
import os, uuid
from django.core.files.temp import NamedTemporaryFile
import urllib.request

def create_image_from_text(quote_model, width: int, height: int, text_size, uuid, fnt_author_size, watermark_width):
    static_path = '/home/jonathan/Documents/github/miste.io/website/static/'
    font_path = static_path + '/fonts/'
    print("font_path", font_path)

    image_path = static_path + '/images/'
    quote_path = os.path.abspath(os.path.dirname(__file__ + '/../../../quote/static/media/'))
    # choose a font
    fnt = ImageFont.truetype(font_path + 'Poppins-Bold.ttf', text_size)
    watermark = Image.open(image_path + 'logo-big-text-white.png')
    watermark = resizeimage.resize_width(watermark, watermark_width)

    fnt_author = ImageFont.truetype(font_path + 'Poppins-Bold.ttf', fnt_author_size)

    img_temp = NamedTemporaryFile(delete=True)
    img_temp.write(urllib.request.urlopen(quote_model.file_image.file.url).read())

    img = Image.open(img_temp).convert('RGB')
    img = resizeimage.resize_cover(img, [width, height])
    img = ImageEnhance.Brightness(img)
    img = img.enhance(0.5)
    d = ImageDraw.Draw(img)
    # find the average size of the letter
    sum = 0
    for letter in quote_model.body:
        sum += d.textsize(letter, font=fnt)[0]
    average_length_of_letter = sum / len(quote_model.body)
    # find the number of letters to be put on each line
    number_of_letters_for_each_line = (width / 1.7) / average_length_of_letter

    incrementer = 0
    quote = ''
    # add some line breaks
    for letter in quote_model.body:
        if letter == '-':
            quote += '\n' + letter
        elif letter == '+':
            quote += '\n'
            incrementer = 0
        elif incrementer < number_of_letters_for_each_line:
            quote += letter
        else:
            if letter == ' ':
                quote += '\n'
                incrementer = 0
            else:
                quote += letter
        incrementer += 1
    # render the text in the center of the box
    dim = d.textsize(quote, font=fnt)
    x2 = dim[0]
    y2 = dim[1]
    qx = (width / 2 - x2 / 2)
    qy = (height / 2 - y2 / 2) - 70
    d.text((qx, qy), '"' + quote + '"', align="center", font=fnt, fill=(255, 255, 255))

    w, h = img.size
    text_w, text_h = d.textsize("- " + quote_model.author.name, fnt_author)
    d.text(((w - text_w) // 2, dim[1] + qy + 5 + fnt_author_size), "- " + quote_model.author.name, (255, 255, 255),
           font=fnt_author)

    watermark_w, watermark_h = watermark.size

    img.paste(watermark, ((w - watermark_w) // 2, h - watermark_h - 10), watermark)
    path = quote_path + quote_model.author.name
    Path(path).mkdir(parents=True, exist_ok=True)
    filename = slugify(quote_model.title) + '_' + str(uuid) + '_' + str(width) + 'x' + str(height) + '.jpg'
    img.save(path + '/' + filename, quality=100)
    img_temp.flush()
    return img
