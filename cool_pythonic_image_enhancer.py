import os
import math
from PIL import Image, ImageFilter, ImageEnhance, ImageFont, ImageDraw
import textwrap


def main():
    assets_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), 'assets'))
    print_header()
    raw_im = get_image(assets_folder)
    try:
        if raw_im:
            im = update_image(raw_im, assets_folder)
            im.show()
            im.save(os.path.abspath(os.path.join(assets_folder,'result.jpg')), 'JPEG')
    except ValueError as ve:
        print('VALUE ERROR - {}'.format(ve))
    except Exception as x:
        print('BIG OOPS - {}'.format(x))



def print_header():
    print('----------------------------------------------')
    print("     Pierre's Pythonic Image Enhancer   ")
    print('----------------------------------------------')


def get_image(assets_folder):
    filename = input('Enter Image Name from Asset Folder (or full path to image):')
    full_file_name = os.path.abspath(os.path.join(assets_folder, filename))
    if os.path.exists(full_file_name):
        image = Image.open(full_file_name)
    elif os.path.exists(filename):
        image = Image.open(filename)
    else:
        image = None
    return image


def update_image(raw_im, assets_folder):
    margin = 10
    logo_size = 100
    # Image Filters
    im = raw_im.filter(ImageFilter.SHARPEN)
    enhancer = ImageEnhance.Color(im)
    im = enhancer.enhance(1.3)
    # Background
    background = Image.new('RGB', (im.width, im.height) , (0, 0, 0))
    background.paste(im, (0, 0))

    #create white image bigger than logo by margin
    border = Image.new('RGB', (logo_size + margin, logo_size + margin), (255,255,255))
    # DD Logo
    dd_logo_path = os.path.abspath(os.path.join(assets_folder, 'dimensionDataLogo.png'))
    if os.path.exists(dd_logo_path):
        dd_logo = Image.open(dd_logo_path)
    else:
        raise ValueError('could not find Logo {}'.format(dd_logo_path))
    dd_logo.thumbnail((logo_size, logo_size))
    # paste the DD logo Top Left
    # paste border
    background.paste(border, (int(margin/2), int(margin/2)))
    # then paste logo
    background.paste(dd_logo, (margin, margin))
    # paste the DD logo BOTTOM RIGHT
    #paste border
    background.paste(border, (int((background.width - dd_logo.width - margin - margin/2)),
                                  int(background.height - dd_logo.height - margin - margin/2)))
    #now paste logo
    background.paste(dd_logo, (background.width - dd_logo.width - margin, background.height - dd_logo.height - margin))

    # Python Logo
    python_logo_path = os.path.abspath(os.path.join(assets_folder, 'python-logo.png'))
    if os.path.exists(python_logo_path):
        python_logo = Image.open(python_logo_path)
    else:
        raise ValueError('Could not find Python Logo {}'.format(python_logo_path))

    python_logo.thumbnail((logo_size, logo_size))
    # background.paste(python_logo, (margin, background.height - python_logo.height - margin))
    # Paste Python Logo on Top Right and Bottom Left
    background.paste(border, (int(background.width - python_logo.width - margin - margin/2), int(margin/2)))
    background.paste(python_logo, (background.width - python_logo.width - margin, margin))
    background.paste(border, (int(margin/2), int(background.height - python_logo.height - margin - margin/2)))
    background.paste(python_logo,  (margin , background.height - python_logo.height - margin))

    return background


if __name__ == '__main__':
    main()
