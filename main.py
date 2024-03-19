# main.py
from file_dialogue import FileDialogue
from invoker import FileOperationInvoker
from commands import RemuxCommand, CorrectNameCommand, ReplaceAudioCommand, RemoveBlackBarsCommand, VideoCropperCommand, AVItoMP4Command
import os
from multiprocessing import Process, cpu_count
import multiprocessing
from multiprocessing import Lock

OPTIONS = {
    "1": "Remux",
    "2": "Correct name",
    "3": "Replace audio",
    "4": "Remove Black Bars",
    "5": "Crop Video",
    "6": "Convert AVI to MP4",
    "7": "Custom Command"
}

DELETE_ORIGINAL_FLV = False
MOVE_FLV_TO_SUBFOLDER = "flv-originals"
AUTOMATCH_AUDIO = True
AUTOMATCH_AUDIOSUBFOLDER = "auphonic-results"
MOVE_ORIG = "original-mp4"
CROP_DIMENSIONS = (0, 0, 1680, 866)  # (x, y, width, height)


def show_main_menu():
    print("Select an option:")
    for key, value in OPTIONS.items():
        print(f"{key}: {value}")
    print("0: Exit")


def get_selected_option():
    try:
        option = input("Enter the number of the option: ")
        if option == "0":
            return option
        if option in OPTIONS:
            return option
        else:
            print("Invalid option")
            return get_selected_option()
    except KeyboardInterrupt:
        return "0"


def process_files(commands):
    invoker = FileOperationInvoker()
    for command in commands:
        invoker.add_command(command)
    invoker.execute_commands()


def remux_files(file_paths):
    processes = []
    for file_path in file_paths:
        p = Process(target=process_files, args=(
            [RemuxCommand(file_path, DELETE_ORIGINAL_FLV, MOVE_FLV_TO_SUBFOLDER)],))
        p.start()
        processes.append(p)
    for p in processes:
        p.join()


def correct_name_files(file_paths):
    processes = []
    for file_path in file_paths:
        p = Process(target=process_files, args=(
            [CorrectNameCommand(file_path)],))
        p.start()
        processes.append(p)
    for p in processes:
        p.join()


def replace_audio_files(video_paths):
    processes = []
    for video_path in video_paths:
        if AUTOMATCH_AUDIO and (AUTOMATCH_AUDIOSUBFOLDER in os.listdir(os.path.dirname(video_path))):
            audio_folder_path = os.path.join(
                os.path.dirname(video_path), AUTOMATCH_AUDIOSUBFOLDER)
            audio_path = os.path.join(audio_folder_path, os.path.basename(
                video_path).rsplit('.', 1)[0] + '.wav')
        else:
            file_dialogue = FileDialogue()
            audio_path = file_dialogue.open_file_dialogue(
                "wav", multiple=False, title="Select audio file")
        p = Process(target=process_files, args=([ReplaceAudioCommand(
            video_path, audio_path, auto_match_audio=AUTOMATCH_AUDIO, audio_subfolder=AUTOMATCH_AUDIOSUBFOLDER, move_old_mp4=MOVE_ORIG)],))
        p.start()
        processes.append(p)
    for p in processes:
        p.join()
    print("All processes finished for ReplaceAudioCommand")


def remove_black_bars_files(file_paths):
    processes = []
    for file_path in file_paths:
        p = Process(target=process_files, args=([RemoveBlackBarsCommand(
            video_path=file_path, crop_dimensions=CROP_DIMENSIONS)],))
        p.start()
        processes.append(p)
    for p in processes:
        p.join()


def crop_video_files(file_paths):
    invoker = FileOperationInvoker()
    for file_path in file_paths:
        invoker.add_command(VideoCropperCommand(
            file_path, None, crop_dimensions=CROP_DIMENSIONS))
    invoker.execute_commands()


def convert_avi_to_mp4_files(file_paths):
    processes = []
    for file_path in file_paths:
        p = Process(target=process_files, args=(
            [AVItoMP4Command(file_path)],))
        p.start()
        processes.append(p)
    for p in processes:
        p.join()
    print("All processes finished for AVItoMP4Command")


def custom_command_files(file_paths):
    processes = []
    for file_path in file_paths:
        p = Process(target=process_files, args=([RemoveBlackBarsCommand(file_path, crop_dimensions=CROP_DIMENSIONS),
                                                 AVItoMP4Command(os.path.join(os.path.dirname(
                                                     file_path), "processed_black_bars", os.path.basename(file_path).rsplit('.', 1)[0] + ".avi")),
                                                 ReplaceAudioCommand(os.path.join(os.path.dirname(file_path), "processed_black_bars/converted", os.path.basename(file_path).rsplit('.', 1)[0] + ".mp4"), None, auto_match_audio=AUTOMATCH_AUDIO, audio_subfolder=AUTOMATCH_AUDIOSUBFOLDER)],))
        p.start()
        processes.append(p)
    for p in processes:
        p.join()
    print("All processes finished for command")


def main():
    while True:
        show_main_menu()
        option = get_selected_option()

        invoker = FileOperationInvoker()
        file_dialogue = FileDialogue()

        if option == "0":
            break

        elif option == "1":  # Remux flv to mp4
            file_paths = file_dialogue.open_file_dialogue("flv")
            remux_files(file_paths)

        elif option == "2":  # Correct name
            file_paths = file_dialogue.open_file_dialogue("all")
            correct_name_files(file_paths)

        elif option == "3":  # Replace audio
            video_paths = file_dialogue.open_file_dialogue("all")
            replace_audio_files(video_paths)

        elif option == "4":  # Remove black bars
            file_paths = file_dialogue.open_file_dialogue(
                "all", multiple=True, title="Select video files with black bars")
            remove_black_bars_files(file_paths)

        elif option == "5":  # Crop video
            file_paths = file_dialogue.open_file_dialogue(
                "mp4", multiple=True, title="Select video files to crop")
            crop_video_files(file_paths)

        elif option == "6":  # Convert AVI to MP4
            file_paths = file_dialogue.open_file_dialogue("avi")
            convert_avi_to_mp4_files(file_paths)

        elif option == "7":  # Custom Command
            file_paths = file_dialogue.open_file_dialogue(
                "mp4", multiple=True, title="Select Files to process")
            custom_command_files(file_paths)

        # invoker.execute_commands()
        # invoker.print_history("history.json")


if __name__ == "__main__":
    multiprocessing.set_start_method('spawn')
    main()
