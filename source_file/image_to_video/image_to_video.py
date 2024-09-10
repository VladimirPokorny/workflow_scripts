import cv2
import os
import logging
import sys
import natsort
import datetime


class Image2Video:
    def __init__(self, img_sufix='.png') -> None:
        self.working_directory = os.getcwd()
        self.image_folder_path = os.path.join(self.working_directory, '')
        self.source_image_folder_path = os.path.join(self.image_folder_path, 'source_images')
        self.list_all_images = []
        self.img_sufix = img_sufix

    def find_all_images(self) -> None:
        for root, dirs, files in os.walk(self.image_folder_path):
            for file in files:
                if file.endswith(self.img_sufix):
                    self.list_all_images.append(os.path.join(root, file))

    def move_all_images_into_source_images_folder(self) -> None:
        for file in self.list_all_images:
            try:
                os.rename(os.path.join(file), os.path.join(self.source_image_folder_path, os.path.basename(file)))
            except FileExistsError:
                pass

    def sort_images(self) -> None:
        self.list_all_images = natsort.natsorted(self.list_all_images)

    def format_timedelta(self, seconds: float) -> str:
        td = datetime.timedelta(seconds=seconds)

        total_seconds = int(td.total_seconds())
        milliseconds = int((td.total_seconds() - total_seconds) * 1000)
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"

    def create_subtitles(self, fps, subtitles_name='video.srt') -> None:
        video_duration = len(self.list_all_images) / fps
        frame_duration = video_duration / len(self.list_all_images)
        previous_frame_time = 0

        with open(subtitles_name, 'w') as f:
            for i, img in enumerate(self.list_all_images):
                f.write(f"{i + 1}\n")
                f.write(f"{self.format_timedelta(previous_frame_time)} --> {self.format_timedelta(previous_frame_time + frame_duration)}\n")
                f.write(f"{os.path.basename(img)}\n")
                f.write("\n")
                previous_frame_time += frame_duration

    def create_video(self, video_name, fps=24, duration=None) -> None:
        frame = cv2.imread(self.list_all_images[0])
        height, width, layers = frame.shape

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Use 'mp4v' codec for MP4 format

        if duration is not None:
            fps = len(self.list_all_images) / duration

        video = cv2.VideoWriter(video_name, fourcc, fps, (width, height))

        # Write each image to the video
        for image in self.list_all_images:
            frame = cv2.imread(image)
            video.write(frame)
            logging.info(f"Image {os.path.basename(image)} added to the video.")

        # Release the video writer
        video.release()
        logging.info(f"Video {video_name} created successfully.")

    def print_help(self):
        print("Usage: image2video [-h] [-s] [--height] [--width] [--output_folder]")
        print()
        print("This script resizes images in the current directory and saves them in a new folder called resized_images")
        print()
        print("Options:")
        print("  -h, --help             Show this help message and exit")
        print("  -s                     Specify the image suffix (default is '.png')")
        print("  --fps                  Specify the frames per second of the video (default is 24)")
        print("  -d --duration          Specify the duration of the video in seconds (default is None)")
        print("  -m --move              Move all images into a new folder called 'source_images'")
        print("  -n --name              Specify the name of the video (default is 'video.mp4')")
        print("  -o --output_folder     Specify the folder name where the video will be saved")
        print("                         (default is in the current working directory)")
        print("  -l --log               Enable logging")
        print("  --subtitles            Create a subtitles file for the video")
        print()


if __name__ == '__main__':
    if '-h' in sys.argv or '--help' in sys.argv:
        Image2Video().print_help()
        sys.exit(0)

    if '-s' in sys.argv:
        img_sufix = sys.argv[sys.argv.index('-s') + 1]
    else:
        img_sufix = '.png'

    if '--fps' in sys.argv:
        fps = int(sys.argv[sys.argv.index('--fps') + 1])
    else:
        fps = 24

    if '-d' in sys.argv :
        duration = int(sys.argv[sys.argv.index('-d') + 1])
    elif '--duration' in sys.argv:
        duration = int(sys.argv[sys.argv.index('--duration') + 1])
    else:
        duration = None

    if '-m' in sys.argv or '--move' in sys.argv:
        move_images = True
    else:
        move_images = False

    if '-n' in sys.argv or '--name' in sys.argv:
        video_name = sys.argv[sys.argv.index('--name') + 1]
    else:
        video_name = 'video.mp4'

    if '-o' in sys.argv or '--output_folder' in sys.argv:
        source_image_folder_path = sys.argv[sys.argv.index('--output_folder') + 1]
    else:
        source_image_folder_path = ''

    if '-l' in sys.argv or '--log' in sys.argv:
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s | %(levelname)s | %(message)s')
    else:
        logging.disable(logging.CRITICAL)


    video_maker = Image2Video(img_sufix=img_sufix)
    video_maker.find_all_images()
    video_maker.sort_images()
    video_maker.create_video(video_name='video.mp4', fps=fps, duration=duration)
    video_maker.create_subtitles(fps=fps)