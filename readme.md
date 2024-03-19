
# Video/Audio Processing Tool

This Python project offers a variety of video processing functions through a user-friendly command-line interface. It leverages multiprocessing for efficient handling of video file operations, including remuxing, audio replacement, cropping, and more.

## Features

- **Remux Video Files**: Convert FLV files to MP4 without re-encoding.
- **Correct Video File Names**: Rename files based on a predefined scheme.
- **Replace Audio in Video**: Substitute the existing audio track with a new one.
- **Remove Black Bars**: Automatically crop black bars from videos.
- **Crop Video**: Manually crop videos to specified dimensions.
- **Convert AVI to MP4**: Transcode AVI files to MP4 format.
- **Custom Command Execution**: Execute a custom sequence of operations on video files.

## Requirements

- Python 3.x
- Additional Python libraries as specified in `requirements.txt` (if any).

## Setup

1. Ensure Python 3.x is installed on your system.
2. (Optional) Install necessary Python libraries by running `pip install -r requirements.txt` in your terminal.

## How to Use

1. Open your terminal or command prompt.
2. Navigate to the directory containing the script.
3. Run the script by typing `python main.py`.
4. Follow the on-screen prompts to select the desired video processing option.

### Options Menu

- **1**: Remux
- **2**: Correct name
- **3**: Replace audio
- **4**: Remove Black Bars
- **5**: Crop Video
- **6**: Convert AVI to MP4
- **7**: Custom Command
- **0**: Exit

## Configuration

The script includes several configurable options at the beginning of the file, allowing you to tailor its behavior to your needs:

- `DELETE_ORIGINAL_FLV`: Set to `True` to delete the original FLV files after remuxing.
- `MOVE_FLV_TO_SUBFOLDER`: Specify a subfolder name to move original FLV files after processing.
- `AUTOMATCH_AUDIO`: Enable automatic matching of audio files based on video file names.
- `CROP_DIMENSIONS`: Set the default crop dimensions.

## Customization

Feel free to modify the script to add new commands or change existing functionality to better suit your workflow.

## Contributing

Contributions, issues, and feature requests are welcome. Feel free to check [issues page] if you want to contribute.

## License

Distributed under the MIT License. See `LICENSE` for more information.