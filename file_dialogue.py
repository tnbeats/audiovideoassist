from tkinter import filedialog
from tkinter import Tk

class FileDialogue:

    def get_file_types(self, type):
        if type == "flv":
            return [("FLV files", "*.flv")]
        elif type == "mp4":
            return [("MP4 files", "*.mp4")]
        elif type == "html":
            return [("HTML files", "*.html")]
        elif type == "wav":
            return [("WAV files", "*.wav")]
        elif type == "all":
            return [("All files", "*.*")]
        elif type == "avi":
            return [("AVI files", "*.avi")]


    def open_file_dialogue(self, type, multiple=True, title = "Select file(s)"):
        file_types = self.get_file_types(type)
        root = Tk()
        root.withdraw() # we don't want a full GUI, so keep the root window from appearing
        if multiple:
            file_paths = filedialog.askopenfilenames(
                title=title,
                filetypes=file_types
            )
        else:
            file_paths = filedialog.askopenfilename( 
                title=title,
                filetypes=file_types
            )
        return file_paths
    
