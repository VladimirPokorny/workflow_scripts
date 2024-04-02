from PIL import Image
import os


class ImageResizer:
    def __init__(self, img_sufix='.png') -> None:
        self.working_directory = os.getcwd()
        self.image_folder_path = os.path.join(self.working_directory, '')
        self.resized_image_folder_path = os.path.join(self.image_folder_path, 'resized_images')
        self.list_all_images = []
        self.img_sufix = img_sufix

    def move_all_images_into_images_folder(self):
        for root, dirs, files in os.walk(self.working_directory):
            for file in files:
                if file.endswith(self.img_sufix):
                    try:
                        os.rename(os.path.join(root, file), os.path.join(self.image_folder_path, file))
                    except FileExistsError:
                        pass

    def find_all_images(self):
        for root, dirs, files in os.walk(self.image_folder_path):
            for file in files:
                if file.endswith(self.img_sufix):
                    self.list_all_images.append(os.path.join(root, file))

    def create_resized_image_folder(self):
        try:
            os.mkdir(self.resized_image_folder_path)
        except FileExistsError:
            pass
    
    def create_image_folder(self):
        try:
            os.mkdir(self.image_folder_path)
        except FileExistsError:
            pass

    def resize_image(self, input_image_path, new_width=None, new_height=None):
        img_base_name = os.path.basename(input_image_path)
                
        original_image = Image.open(input_image_path)
        original_width, original_height = original_image.size

        if new_width:
            ratio = new_width / original_width
            new_height = int(original_height * ratio)
            resized_image = original_image.resize((new_width, new_height))
            resized_image.save(os.path.join(self.resized_image_folder_path, img_base_name))
        
        elif new_height:
            ratio = new_height / original_height
            new_width = int(original_width * ratio)
            resized_image = original_image.resize((new_width, new_height))
            resized_image.save(os.path.join(self.resized_image_folder_path, img_base_name))

        elif new_width and new_height:
            resized_image = original_image.resize((new_width, new_height))
            resized_image.save(os.path.join(self.resized_image_folder_path, img_base_name))

        else:
            print('No new width or height specified')


if __name__ == '__main__':
    image_resizer = ImageResizer()
    image_resizer.find_all_images()
    image_resizer.create_image_folder()
    image_resizer.move_all_images_into_images_folder()
    image_resizer.create_resized_image_folder()
    for image in image_resizer.list_all_images:
        image_resizer.resize_image(image, new_width=800)