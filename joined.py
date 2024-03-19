# # commands.py
# import subprocess
# import cv2
# import numpy as np
# from moviepy.editor import VideoFileClip
# from better_ffmpeg_progress import FfmpegProcess
# from tkinter import filedialog
# from tkinter import Tk
# import os
# import json
# from multiprocessing import Lock, Process, cpu_count
# from file_dialogue import FileDialogue
# import multiprocessing


# class Command:
#     def execute(self):
#         pass


# class RemuxCommand(Command):

#     def __init__(self, file_path, delete_source_files=False, move_to_folder=None):
#         self.file_path = file_path
#         self.delete_source_files = delete_source_files
#         self.move_to_folder = move_to_folder
#         self.status = "Initialized"
#         self.reason = None

#     def is_valid(self):
#         if not os.path.isfile(self.file_path):
#             self.status, self.reason = "Failed", f"File not found: {self.file_path}"
#             return False
#         if not self.file_path.lower().endswith('.flv'):
#             self.status, self.reason = "Failed", f"Invalid file type: {self.file_path.rsplit('.', 1)[1]}"
#             return False
#         return True

#     def execute(self):
#         if not self.is_valid():
#             return False
#         try:
#             self.output_path = self.file_path.rsplit('.', 1)[0] + '.mp4'
#             subprocess.run(['ffmpeg', '-i', self.file_path, '-c',
#                            'copy', self.output_path], check=True)

#             if self.delete_source_files:
#                 os.remove(self.file_path)

#             else:
#                 if self.move_to_folder is not None:
#                     original_folder = os.path.join(
#                         os.path.dirname(self.file_path), self.move_to_folder)
#                     os.makedirs(original_folder, exist_ok=True)
#                     os.rename(self.file_path, os.path.join(
#                         original_folder, os.path.basename(self.file_path)))

#             self.status = "Success"
#             return True
#         except Exception as e:
#             self.status, self.reason = "Failed", str(e)
#             return False


# class CorrectNameCommand(Command):
#     def __init__(self, file_path):
#         self.file_path = file_path
#         self.status = "Initialized"
#         self.reason = None

#     def is_valid(self):
#         if not os.path.isfile(self.file_path):
#             self.status, self.reason = "Failed", f"File not found: {self.file_path}"
#             return False
#         return True

#     def execute(self):
#         if not self.is_valid():
#             return False
#         try:
#             new_name = self.file_path
#             if "Copy of " in self.file_path:
#                 new_name = self.file_path.replace("Copy of ", "")
#                 os.rename(self.file_path, new_name)
#                 print(f"Renamed: {self.file_path}")
#             self.output_path = new_name
#             self.status = "Success"
#             return True
#         except Exception as e:
#             self.status, self.reason = "Failed", str(e)
#             return False


# class ReplaceAudioCommand(Command):

#     def __init__(self, video_path, audio_path, auto_match_audio=False, audio_subfolder=None, move_old_mp4=None):
#         self.video_path = video_path
#         self.audio_path = audio_path
#         self.output_path = None
#         self.move_old_mp4 = move_old_mp4
#         self.status = "Initialized"
#         self.reason = None

#     def is_valid(self):
#         if not os.path.isfile(self.video_path):
#             self.status, self.reason = "Failed", f"Video file not found: {self.video_path}"
#             return False

#         if not (self.video_path.lower().endswith('.mp4') or self.video_path.lower().endswith('.avi')):
#             self.status, self.reason = "Failed", f"Invalid video file type: {self.video_path.rsplit('.', 1)[1]}"
#             return False

#         if not os.path.isfile(self.audio_path):
#             self.status, self.reason = "Failed", f"File not found: {self.audio_path}"
#             return False

#         if not self.audio_path.lower().endswith('.wav'):
#             self.status, self.reason = "Failed", f"Invalid audio file type: {self.audio_path.rsplit('.', 1)[1]}"
#             return False

#         video_length = float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries',
#                                                       'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1',
#                                                       self.video_path]))

#         audio_length = float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries',
#                                                       'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1',
#                                                       self.audio_path]))

#         if abs(video_length - audio_length) > 1:
#             self.status, self.reason = "Failed", f"Video and audio length mismatch: {video_length} vs {audio_length}"
#             return False

#         return True

#     def execute(self):
#         if not self.is_valid():
#             return False
#         try:
#             output_folder = os.path.join(
#                 os.path.dirname(self.video_path), "ready")
#             os.makedirs(output_folder, exist_ok=True)
#             output_path = os.path.join(output_folder, os.path.basename(
#                 self.video_path).rsplit('.', 1)[0] + ".mp4")
#             subprocess.run(['ffmpeg',
#                             '-i', self.video_path,
#                             '-i', self.audio_path,
#                             '-c:v', 'copy',
#                             '-c:a', 'aac',
#                             '-ar', '48000',
#                             '-ab', '320k',
#                             '-af', 'loudnorm=I=-16:TP=-1',
#                             '-shortest',
#                             output_path], check=True)
#             print(f"Processed: {self.video_path}")
#             if self.move_old_mp4 is not None:
#                 print(f"Moving old mp4 to {self.move_old_mp4} folder...")
#                 old_folder = os.path.join(os.path.dirname(
#                     self.video_path), self.move_old_mp4)
#                 os.makedirs(old_folder, exist_ok=True)
#                 os.rename(self.video_path, os.path.join(
#                     old_folder, os.path.basename(self.video_path)))
#                 print(
#                     f"\n Moved: {os.path.basename(self.video_path)} successfully.")

#             self.output_path = output_path
#             self.status = "Success"
#             return True
#         except Exception as e:
#             self.status, self.reason = "Failed", str(e)
#             return False


# class RemoveBlackBarsCommand(Command):
#     def __init__(self, video_path, output_path=None, crop_dimensions=None, export_frames=False):
#         self.video_path = video_path
#         self.output_path = os.path.join(os.path.dirname(video_path), "processed_black_bars", os.path.basename(
#             video_path).rsplit('.', 1)[0] + ".avi") if output_path is None else output_path
#         self.export_frames = export_frames
#         self.frames_folder = self.create_frames_folder()
#         self.status = "Initialized"
#         self.reason = None
#         self.crop_dimensions = crop_dimensions
#         self.detection_log = {'folder': os.path.dirname(video_path),
#                               'video': os.path.basename(video_path),
#                               'output_folder': os.path.dirname(os.path.join(os.path.dirname(video_path), "processed_black_bars")),
#                               'detection': []}

#     def add_to_history(self):
#         pass

#     def create_frames_folder(self):
#         pass
#         if self.export_frames:
#             # Extract the filename without extension to create a subfolder
#             os.makedirs(os.path.dirname(self.output_path), exist_ok=True)
#             base_name = os.path.splitext(os.path.basename(self.output_path))[0]
#             folder_name = f"{base_name}_frames"
#             if not os.path.exists(folder_name):
#                 os.makedirs(folder_name)
#             return folder_name

#     def has_black_bar(self, frame):
#         threshold = 10
#         self.detected = None
#         self.intensity = None
#         if np.any(np.mean(frame[:, :5], axis=(0, 2)) < threshold):
#             self.detected, self.intensity = "left", np.mean(
#                 frame[:, :5], axis=(0, 2))
#             return True
#         if np.any(np.mean(frame[:, -5:], axis=(0, 2)) < threshold):
#             self.detected, self.intensity = "right", np.mean(
#                 frame[:, -5:], axis=(0, 2))
#             return True
#         if np.any(np.mean(frame[:5, :], axis=(0, 2)) < threshold):
#             self.detected, self.intensity = "top", np.mean(
#                 frame[:5, :], axis=(0, 2))
#             return True
#         return False

#     def save_frame_with_black_bar(self, frame, current_time):
#         minutes = int(current_time // 60)
#         seconds = int(current_time % 60)
#         # print(f"Black bar detected at {minutes:02d}:{seconds:02d} on {self.detected} side.")
#         self.detection_log['detection'].append(
#             {'time': f"{minutes:02d}:{seconds:02d}", 'side': self.detected})
#         if self.export_frames:
#             filename = f"{self.frames_folder}/{minutes:02d}-{seconds:02d}.png"
#             cv2.imwrite(filename, frame)

#     def execute(self):
#         self.status = "Processing"
#         print(f"Processing: {self.video_path}")
#         cap = cv2.VideoCapture(self.video_path)
#         fps = cap.get(cv2.CAP_PROP_FPS)
#         width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
#         height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
#         codec = cv2.VideoWriter_fourcc(*'MJPG')
#         total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

#         left, top, right, bottom = self.crop_dimensions if self.crop_dimensions else (
#             0, height, 0, width)

#         out = cv2.VideoWriter(self.output_path, codec,
#                               fps, (right-left, bottom-top))

#         success, frame = cap.read()
#         if not success:
#             cap.release()
#             out.release()
#             return

#         # Initialize the last good frame with the first frame
#         last_good_frame = frame[top:bottom, left:right]
#         frame_count = 1  # Initialize frame count to handle timecode calculations

#         while True:
#             success, frame = cap.read()
#             if not success:
#                 break

#             frame = frame[top:bottom, left:right]  # Crop the frame

#             if self.has_black_bar(frame):
#                 # If the current frame has a black bar, replace it with the last good frame
#                 out.write(last_good_frame)
#                 current_time = frame_count / fps
#                 self.save_frame_with_black_bar(frame, current_time)
#             else:
#                 # Update the last good frame and write it to the output
#                 last_good_frame = frame
#                 out.write(frame)

#             frame_count += 1  # Increment frame count after processing each frame
#             # print progress in percentage in the console in the same line
#             progress = frame_count * 100 / total_frames
#             print(f"\r Processing: {progress:.2f}%", end="")
#         print("\n")

#         cap.release()
#         out.release()
#         self.status = "Success"
#         detection_log_path = os.path.join(os.path.dirname(self.output_path), 'detection_logs',
#                                           self.output_path.rsplit('.', 1)[0] + ".json")
#         with open(detection_log_path, 'w') as f:
#             json.dump(self.detection_log, f, indent=4)
#         # self.combine_audio()

#     def combine_audio(self):
#         original_clip = VideoFileClip(self.video_path)
#         if self.crop_dimensions:
#             video_clip = VideoFileClip('temp_video.avi').crop(x1=self.crop_dimensions[0], y1=self.crop_dimensions[1],
#                                                               x2=self.crop_dimensions[2], y2=self.crop_dimensions[3])
#         else:
#             video_clip = VideoFileClip('temp_video.avi')
#         final_clip = video_clip.set_audio(original_clip.audio)
#         final_clip.write_videofile(self.output_path, codec='libx264', audio=True, audio_fps=48000, preset='slow',
#                                    audio_codec='aac', rewrite_audio=False, remove_temp=True, threads=8)


# class VideoCropperCommand(Command):
#     def __init__(self, video_path, output_path, crop_dimensions):
#         """
#         Initializes the VideoCropper class with the input video path, output video path, and crop dimensions.
#         :param video_path: Path to the input video file.
#         :param output_path: Path where the cropped video will be saved.
#         :param crop_dimensions: A tuple of (x1, y1, x2, y2) representing the crop area.
#         """
#         self.video_path = video_path
#         self.output_path = os.path.join(os.path.dirname(video_path), "cropped", os.path.basename(
#             video_path)) if output_path is None else output_path
#         self.crop_dimensions = crop_dimensions
#         self.status = "Not tracked"
#         self.reason = None

#     def add_to_history(self):
#         pass

#     def execute(self):
#         """
#         Crops the video based on the specified dimensions and saves the output.
#         """
#         # Load the video
#         clip = VideoFileClip(self.video_path)

#         # Crop the video
#         x1, y1, x2, y2 = self.crop_dimensions
#         cropped_clip = clip.crop(x1=x1, y1=y1, x2=x2, y2=y2)

#         # Get the audio from the original video
#         final_clip = cropped_clip.set_audio(clip.audio)

#         # Create the output folder if it doesn't exist
#         os.makedirs(os.path.dirname(self.output_path), exist_ok=True)

#         # Write the output video file
#         final_clip.write_videofile(self.output_path, codec='libx264', audio=True, audio_fps=48000, preset='slow',
#                                    audio_codec='aac', rewrite_audio=False, remove_temp=True, threads=8)


# class AVItoMP4Command(Command):
#     def __init__(self, video_path, output_path=None, move_old_avi='avi_old'):
#         self.video_path = video_path
#         self.move_old_avi = move_old_avi
#         os.makedirs(os.path.join(os.path.dirname(
#             video_path), "converted"), exist_ok=True)
#         self.output_path = os.path.join(os.path.dirname(video_path), "converted",
#                                         os.path.basename(video_path).rsplit('.', 1)[0] + ".mp4") if output_path is None else output_path
#         self.status = "Initialized"
#         self.reason = None

#     def is_valid(self):
#         if not os.path.isfile(self.video_path):
#             self.status, self.reason = "Failed", f"File not found: {self.video_path}"
#             return False
#         if not self.video_path.lower().endswith('.avi'):
#             self.status, self.reason = "Failed", f"Invalid file type: {self.video_path.rsplit('.', 1)[1]}"
#             return False
#         return True

#     def execute(self):
#         if not self.is_valid():
#             return False
#         try:
#             subprocess.run(['ffmpeg',
#                             '-i', self.video_path,
#                             '-c:v', 'libx264',
#                             '-crf', '18',
#                             '-preset', 'slow',
#                             '-c:a', 'copy',
#                             self.output_path], check=True)
#             if self.move_old_avi is not None:
#                 old_folder = os.path.join(os.path.dirname(
#                     self.video_path), self.move_old_avi)
#                 os.makedirs(old_folder, exist_ok=True)
#                 os.rename(self.video_path, os.path.join(
#                     old_folder, os.path.basename(self.video_path)))
#             self.status = "Success"
#             return True
#         except Exception as e:
#             self.status, self.reason = "Failed", str(e)
#             return False


# class FileDialogue:

#     def get_file_types(self, type):
#         if type == "flv":
#             return [("FLV files", "*.flv")]
#         elif type == "mp4":
#             return [("MP4 files", "*.mp4")]
#         elif type == "html":
#             return [("HTML files", "*.html")]
#         elif type == "wav":
#             return [("WAV files", "*.wav")]
#         elif type == "all":
#             return [("All files", "*.*")]
#         elif type == "avi":
#             return [("AVI files", "*.avi")]

#     def open_file_dialogue(self, type, multiple=True, title="Select file(s)"):
#         file_types = self.get_file_types(type)
#         root = Tk()
#         root.withdraw()  # we don't want a full GUI, so keep the root window from appearing
#         if multiple:
#             file_paths = filedialog.askopenfilenames(
#                 title=title,
#                 filetypes=file_types
#             )
#         else:
#             file_paths = filedialog.askopenfilename(
#                 title=title,
#                 filetypes=file_types
#             )
#         return file_paths


# class FileOperationInvoker:
#     def __init__(self, lock=None):
#         self.commands = []
#         self.history = []
#         self.lock = lock

#     def add_to_history(self, command):
#         self.history.append({'command': command.__class__.__name__,
#                              'inputs': [command.file_path if
#                                         hasattr(command, 'file_path') else
#                                         command.video_path, command.audio_path if
#                                         hasattr(command, 'audio_path') else None],
#                              'status': command.status,
#                              'reason': command.reason if command.status == 'Failed' else None,
#                              'output': command.output_path if command.status == 'Success' else None}
#                             )

#     def add_command(self, command):
#         self.commands.append(command)

#     def execute_commands(self):
#         for command in self.commands:
#             command.execute()
#             self.add_to_history(command)

#     def print_history(self, file_path):
#         if self.lock:
#             self.lock.acquire()
#         Successful_commands = [[h['command'], h['inputs'], h['output']]
#                                for h in self.history if h['status'] == 'Success']

#         Failed_commands = [[h['command'], h['inputs'], h['reason']]
#                            for h in self.history if h['status'] == 'Failed']

#         print(f"\n {len(Successful_commands)} commands executed successfully")
#         print(f"\n {len(Failed_commands)} commands failed")

#         # for command, inputfiles, outputfile in Successful_commands:
#         #     print(f"{command}: {inputfiles} -> {outputfile}")
#         # for command, inputfiles, reason in Failed_commands:
#         #     print(f"{command}: {inputfiles} -> {reason}")

#         old_history = []
#         if os.path.exists(file_path):
#             with open(file_path, 'r') as f:
#                 old_history = json.load(f)
#         with open(file_path, 'w') as f:
#             json.dump(self.history + old_history, f, indent=4)

#         if self.lock:
#             self.lock.release()


# # main.py

# OPTIONS = {"1": "Remux", "2": "Correct name", "3": "Replace audio", "4": "Remove Black Bars",
#            "5": "Crop Video", "6": "Convert AVI to MP4", "7": "Custom Command"}
# DELETE_ORIGINAL_FLV = False
# MOVE_FLV_TO_SUBFOLDER = "flv-originals"
# AUTOMATCH_AUDIO = True
# AUTOMATCH_AUDIOSUBFOLDER = "auphonic-results"
# MOVE_ORIG = "original-mp4"
# CROP_DIMENSIONS = (0, 0, 1680, 866)  # (x, y, width, height)


# def show_main_menu():
#     print("Select an option:")
#     for key, value in OPTIONS.items():
#         print(f"{key}: {value}")
#     print("0: Exit")


# def get_selected_option():
#     try:
#         option = input("Enter the number of the option: ")
#         if option == "0":
#             return option
#         if option in OPTIONS:
#             return option
#         else:
#             print("Invalid option")
#             return get_selected_option()
#     except KeyboardInterrupt:
#         return "0"


# def process_files(commands):
#     invoker = FileOperationInvoker()
#     for command in commands:
#         invoker.add_command(command)
#     invoker.execute_commands()


# def main():

#     while True:
#         show_main_menu()
#         option = get_selected_option()

#         invoker = FileOperationInvoker(lock=Lock())
#         file_dialogue = FileDialogue()

#         match option:
#             case "0":
#                 break

#             case "1":  # Remux flv to mp4
#                 file_paths = file_dialogue.open_file_dialogue("flv")
#                 processes = []
#                 for file_path in file_paths:
#                     p = Process(target=process_files, args=(
#                         [RemuxCommand(file_path, DELETE_ORIGINAL_FLV, MOVE_FLV_TO_SUBFOLDER)],))
#                     p.start()
#                     processes.append(p)
#                 for p in processes:
#                     p.join()

#             case "2":  # Correct name
#                 file_paths = file_dialogue.open_file_dialogue("all")
#                 processes = []
#                 for file_path in file_paths:
#                     p = Process(target=process_files, args=(
#                         [CorrectNameCommand(file_path)],))
#                     p.start()
#                     processes.append(p)
#                 for p in processes:
#                     p.join()

#             case "3":  # Replace audio
#                 video_paths = file_dialogue.open_file_dialogue("all")
#                 processes = []
#                 for video_path in video_paths:

#                     if AUTOMATCH_AUDIO and (AUTOMATCH_AUDIOSUBFOLDER in os.listdir(os.path.dirname(video_path))):
#                         audio_folder_path = os.path.join(
#                             os.path.dirname(video_path), AUTOMATCH_AUDIOSUBFOLDER)
#                         audio_path = os.path.join(audio_folder_path, os.path.basename(
#                             video_path).rsplit('.', 1)[0] + '.wav')
#                     else:
#                         audio_path = file_dialogue.open_file_dialogue(
#                             "wav", multiple=False, title="Select audio file")
#                     # invoker.add_command(ReplaceAudioCommand(video_path, audio_path, auto_match_audio=AUTOMATCH_AUDIO, audio_subfolder=AUTOMATCH_AUDIOSUBFOLDER, move_old_mp4=MOVE_ORIG))
#                     p = Process(target=process_files, args=([ReplaceAudioCommand(
#                         video_path, audio_path, auto_match_audio=AUTOMATCH_AUDIO, audio_subfolder=AUTOMATCH_AUDIOSUBFOLDER, move_old_mp4=MOVE_ORIG)],))
#                     p.start()
#                     processes.append(p)
#                 for p in processes:
#                     p.join()
#                 print("All processes finished for ReplaceAudioCommand")

#             case "4":  # Remove black bars
#                 file_paths = file_dialogue.open_file_dialogue(
#                     "all", multiple=True, title="Select video files with black bars")
#                 processes = []
#                 for file_path in file_paths:
#                     p = Process(target=process_files, args=([RemoveBlackBarsCommand(
#                         video_path=file_path, crop_dimensions=CROP_DIMENSIONS)],))
#                     invoker.add_command(RemoveBlackBarsCommand(
#                         video_path=file_path, crop_dimensions=CROP_DIMENSIONS))

#                     # output_path = os.path.join(os.path.dirname(file_path), "processed_black_bars", os.path.basename(file_path).rsplit('.', 1)[0] + ".avi")

#                     # invoker.add_command(ReplaceAudioCommand(output_path, None, auto_match_audio=AUTOMATCH_AUDIO, audio_subfolder= AUTOMATCH_AUDIOSUBFOLDER))

#             case "5":  # Crop video
#                 file_paths = file_dialogue.open_file_dialogue(
#                     "mp4", multiple=True, title="Select video files to crop")
#                 for file_path in file_paths:
#                     invoker.add_command(VideoCropperCommand(
#                         file_path, None, crop_dimensions=CROP_DIMENSIONS))

#             case "6":  # Convert AVI to MP4
#                 file_paths = file_dialogue.open_file_dialogue("avi")
#                 processes = []
#                 for file_path in file_paths:
#                     # invoker.add_command(AVItoMP4Command(file_path))
#                     p = Process(target=process_files, args=(
#                         [AVItoMP4Command(file_path)],))
#                     p.start()
#                     processes.append(p)
#                 for p in processes:
#                     p.join()
#                 print("All processes finished for AVItoMP4Command")

#             case "7":  # Custom Command

#                 file_paths = file_dialogue.open_file_dialogue(
#                     "mp4", multiple=True, title="Select Files to process")

#                 processes = []
#                 for file_path in file_paths:

#                     p = Process(target=process_files, args=([RemoveBlackBarsCommand(file_path, crop_dimensions=CROP_DIMENSIONS),
#                                                              AVItoMP4Command(os.path.join(os.path.dirname(
#                                                                  file_path), "processed_black_bars", os.path.basename(file_path).rsplit('.', 1)[0] + ".avi")),
#                                                              ReplaceAudioCommand(os.path.join(os.path.dirname(file_path), "processed_black_bars/converted", os.path.basename(file_path).rsplit('.', 1)[0] + ".mp4"), None, auto_match_audio=AUTOMATCH_AUDIO, audio_subfolder=AUTOMATCH_AUDIOSUBFOLDER)],))

#                     p.start()
#                     processes.append(p)
#                 for p in processes:
#                     p.join()
#                 print("All processes finished for command")

#                 # processes = []
#                 # for file_path in file_paths:
#                 #     command = AVItoMP4Command(os.path.join(os.path.dirname(file_path), "processed_black_bars", os.path.basename(file_path).rsplit('.', 1)[0] + ".avi"))

#                 #     p = Process(target=process_files, args=([command],))
#                 #     p.start()
#                 #     processes.append(p)
#                 # for p in processes:
#                 #     p.join()
#                 # print("All processes finished for command[command.__class__.__name__]")

#                 # processes = []
#                 # for file_path in file_paths:
#                 #     command = ReplaceAudioCommand(os.path.join(os.path.dirname(file_path), "processed_black_bars/converted", os.path.basename(file_path).rsplit('.', 1)[0] + ".mp4"), None, auto_match_audio=AUTOMATCH_AUDIO, audio_subfolder= AUTOMATCH_AUDIOSUBFOLDER)

#                 #     p = Process(target=process_files, args=([command],))
#                 #     p.start()
#                 #     processes.append(p)
#                 # for p in processes:
#                 #     p.join()
#                 # print("All processes finished for command[command.__class__.__name__]")

#         # invoker.execute_commands()
#         # invoker.print_history("history.json")


# if __name__ == "__main__":
#     multiprocessing.set_start_method('spawn')
#     main()
