# Workflow Scripts

Welcome to the Workflow Scripts repository! This collection of scripts is designed to streamline and automate various tasks in your workflow, enhancing productivity and efficiency. Whether you're dealing with image processing, data manipulation, or other routine tasks, these scripts will help you get the job done faster and with fewer errors.

## Features

- **Image Resizing**: Easily resize images while maintaining aspect ratios.

## ImageResizer
Resize images in working directory and move them to the `resize_image` folder. User could specify the output folder name, resize image size or image extension by following options.

```
Usage: resize_image [-h] [-s] [--height] [--width] [--output_folder]"

This script resizes images in the current directory and saves them in a new folder called resized_images

Options:
    -h, --help         Show this help message and exit
    -s                 Specify the image suffix (default is '.png')
    --height           Specify the new height of the image (default is None)
    --width            Specify the new width of the image (default is 800px)
    --output_folder    Specify the folder name where the resized images will be saved (default is 'resized_images')
```

### ImageResizer usage example
Following command

```bash
C:\Users\Username\Pictures\holiday_photos> resize_image --height 1024 --output_folder small_photos
```

resizes all images in `C:\Users\Username\Pictures\holiday_photos` folder to the 1024 px width and move all resized photos to the `small_photos` folder in the working directory. So location of the resized images will be `C:\Users\Username\Pictures\holiday_photos\small_photos`

## Usage
To use workflow scripts, follow these steps:

1. Download Python: [download_link](https://www.python.org/downloads/)

2. Navigate to a directory where you usually store scripts and projects, such as `Documents`.

```bash
cd ~/Documents
```

3. Clone the repository by running the following command in your terminal:

```bash
git clone git@github.com:VladimirPokorny/workflow_scripts.git
```

4. Change to the repository folder:

```bash
cd workflow_scripts
```

5. Include the `workflow_script` folder in your PATH by running the following command:

for PowerShell users
```bash
$env:PATH += ";$(Get-Location)"
```

for Unix-like shells (e.g., Bash, Zsh)

```bash
export PATH=$PATH:$(pwd)
```

6. Test if everything works properly. Just type to the terminal anywhere:

```
workflow_script_test
```

7. It should print `All settings are correct. The script is ready to run.` to the terminal.

8. Now you can easily access and use the scripts in your workflow. Enjoy!
