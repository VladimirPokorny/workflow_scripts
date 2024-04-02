from PIL import Image
import imageio
import os
import re

class GifMaker:
    def __init__(self, img_sufix='.png') -> None:
        self.working_directory = os.getcwd()
        self.image_folder_path = os.path.join(self.working_directory, 'images')
        self.gif_output_path = os.path.join(self.image_folder_path, 'gifs')
        self.list_all_images = []
        self.background_image = None
        self.img_sufix = img_sufix

    def find_all_images(self):
        for root, dirs, files in os.walk(self.image_folder_path):
            for file in files:
                if file.endswith(self.img_sufix) and not re.match(r'^_.*', file):
                    self.list_all_images.append(os.path.join(root, file))
    
    def find_background_image(self):
        for root, dirs, files in os.walk(self.image_folder_path):
            for file in files:
                if file.endswith(self.img_sufix) and re.match(r'^_.*', file):
                    self.background_image = os.path.join(root, file)
                    break
        
        if not self.background_image:
            raise FileNotFoundError('Background image not found')
    
    def create_gif_folder(self):
        try:
            os.mkdir(self.gif_output_path)
        except FileExistsError:
            pass

    def create_gif(self, duration=500):
        images = []
        background = Image.open(self.background_image)

        for path in self.list_all_images:
            img = Image.open(path)
            gif_name = os.path.basename(path)
            gif_path = os.path.join(self.gif_output_path, f'{gif_name}.gif')
            
            img.save(
                gif_path,
                save_all=True,
                append_images=[background.resize(img.size)],
                duration=duration,
                loop=0
            )
            
            images.clear()

if __name__ == "__main__":
    gif_maker = GifMaker()
    gif_maker.find_all_images()
    gif_maker.find_background_image()
    gif_maker.create_gif_folder()
    gif_maker.create_gif()
