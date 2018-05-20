import os
from shutil import copy2

from PIL import Image

SKIP_FILES = ['.DS_Store']


def get_list_of_files(location='raw'):
    file_paths = []
    for root, dirs, files in os.walk(location):
        for file in files:
            if file not in SKIP_FILES:
                file_paths.append(os.path.join(root, file))
    return file_paths


def copy_and_remove_raw(image_path):

    desired_directory = os.path.dirname(
        image_path.replace('raw', 'img', 1)
    )

    thumbnail_dir = os.path.join(desired_directory, 'tbnl')
    image_dir = os.path.join(desired_directory, 'fll')

    if not os.path.exists(thumbnail_dir):
        os.makedirs(thumbnail_dir, exist_ok=True)

    if not os.path.exists(image_dir):
        os.makedirs(image_dir, exist_ok=True)

    thumbnail_file = os.path.join(thumbnail_dir, os.path.basename(image_path))
    full_file = os.path.join(image_dir, os.path.basename(image_path))

    copy_full = True
    copy_thumb = True

    if os.path.isfile(full_file):
        confirm = input(f"File '{full_file}' exists...overwrite? (y/n) ")
        if confirm != 'y':
            copy_full = False

    if os.path.isfile(thumbnail_file):
        confirm = input(f"File '{thumbnail_file}' exists...overwrite? (y/n) ")
        if confirm != 'y':
            copy_thumb = False

    if copy_full:
        copy2(image_path, full_file)

    if not copy_thumb:
        return

    extension = image_path.split('.')[-1].upper()

    if extension == 'JPG':
        extension = 'JPEG'

    img = Image.open(image_path)
    if img.size[0] > 500 or img.size[1] > 500:
        img.thumbnail((500, 500), Image.ANTIALIAS)
        img.save(thumbnail_file, extension)
    else:
        copy2(image_path, thumbnail_file)

    os.remove(image_path)


if __name__ == '__main__':
    images = get_list_of_files()
    for image in images:
        copy_and_remove_raw(image)
