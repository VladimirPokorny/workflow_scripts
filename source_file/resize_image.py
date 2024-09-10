from PIL import Image
import os
import sys
import logging

logging.basicConfig(level=logging.INFO)


class ImageResizer:
    def __init__(self, img_sufix='.png') -> None:
        self.working_directory = os.getcwd()
        self.image_folder_path = os.path.join(self.working_directory, '')
        self.resized_image_folder_path = os.path.join(self.image_folder_path, 'resized_images')
        self.list_all_images = []
        self.img_sufix = img_sufix

    def move_all_images_into_images_folder(self) -> None:
        for root, dirs, files in os.walk(self.working_directory):
            for file in files:
                if file.endswith(self.img_sufix):
                    try:
                        os.rename(os.path.join(root, file), os.path.join(self.image_folder_path, file))
                    except FileExistsError:
                        pass

    def find_all_images(self) -> None:
        for root, dirs, files in os.walk(self.image_folder_path):
            for file in files:
                if file.endswith(self.img_sufix):
                    self.list_all_images.append(os.path.join(root, file))

    def create_resized_image_folder(self, folder_name='resized_images') -> None:
        self.resized_image_folder_path = os.path.join(self.image_folder_path, folder_name)
        os.makedirs(self.resized_image_folder_path, exist_ok=True)

    def create_image_folder(self):
        try:
            os.mkdir(self.image_folder_path)
        except FileExistsError:
            pass

    def resize_image(self, input_image_path, new_width=None, new_height=None):
        img_base_name = os.path.basename(input_image_path)

        original_image = Image.open(input_image_path)
        original_width, original_height = original_image.size

        if new_width is not None and new_height is None:
            logging.info(f'New width: {new_width}')
            ratio = new_width / original_width
            new_height = int(original_height * ratio)
            resized_image = original_image.resize((new_width, new_height))
            resized_image.save(os.path.join(self.resized_image_folder_path, img_base_name))

        elif new_height is not None and new_width is None:
            logging.info(f'New height: {new_height}')
            ratio = new_height / original_height
            new_width = int(original_width * ratio)
            resized_image = original_image.resize((new_width, new_height))
            resized_image.save(os.path.join(self.resized_image_folder_path, img_base_name))

        elif new_width is not None and new_height is not None:
            logging.info(f'New width: {new_width} and New height: {new_height}')
            # Calculate the aspect ratio
            aspect_ratio = original_width / original_height
            if new_width / new_height > aspect_ratio:
                new_width = int(new_height * aspect_ratio)
            else:
                new_height = int(new_width / aspect_ratio)
            resized_image = original_image.resize((new_width, new_height))
            resized_image.save(os.path.join(self.resized_image_folder_path, img_base_name))

        else:
            print('No new width or height specified')

    def print_help(self):
        print("Usage: resize_image [-h] [-s] [--height] [--width] [--output_folder]")
        print()
        print("This script resizes images in the current directory and saves them in a new folder called resized_images")
        print()
        print("Options:")
        print("  -h, --help         Show this help message and exit")
        print("  -s                 Specify the image suffix (default is '.png')")
        print("  --height           Specify the new height of the image (default is None)")
        print("  --width            Specify the new width of the image (default is 800px)")
        print("  --output_folder    Specify the folder name where the resized images will be saved (default is 'resized_images')")
        print()


if __name__ == '__main__':
    print(sys.argv)

    if '-h' in sys.argv or '--help' in sys.argv:
        ImageResizer.print_help()
        sys.exit(0)

    if '-s' in sys.argv:
        img_sufix = sys.argv[sys.argv.index('-s') + 1]
    else:
        img_sufix = '.png'

    if '--width' in sys.argv and '--height' in sys.argv:
        new_width = int(sys.argv[sys.argv.index('--width') + 1])
        new_height = int(sys.argv[sys.argv.index('--height') + 1])
    elif '--width' in sys.argv:
        new_width = int(sys.argv[sys.argv.index('--width') + 1])
        new_height = None
    elif '--height' in sys.argv:
        new_height = int(sys.argv[sys.argv.index('--height') + 1])
        new_width = None

    if '--output_folder' in sys.argv:
        resized_image_folder_path = sys.argv[sys.argv.index('--output_folder') + 1]
    else:
        resized_image_folder_path = 'resized_images'

    image_resizer = ImageResizer(img_sufix=img_sufix)
    image_resizer.find_all_images()
    image_resizer.create_image_folder()
    image_resizer.move_all_images_into_images_folder()
    image_resizer.create_resized_image_folder(folder_name=resized_image_folder_path)

    for image in image_resizer.list_all_images:
        image_resizer.resize_image(image, new_width=new_width, new_height=new_height)
