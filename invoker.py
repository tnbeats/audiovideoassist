import os
import json
from multiprocessing import Lock


class FileOperationInvoker:
    def __init__(self, lock=None):
        self.commands = []
        self.history = []
        self.lock = lock

    def add_to_history(self, command):
        self.history.append({'command': command.__class__.__name__,
                             'inputs': [command.file_path if
                                        hasattr(command, 'file_path') else
                                        command.video_path, command.audio_path if
                                        hasattr(command, 'audio_path') else None],
                             'status': command.status,
                             'reason': command.reason if command.status == 'Failed' else None,
                             'output': command.output_path if command.status == 'Success' else None}
                            )

    def add_command(self, command):
        self.commands.append(command)

    def execute_commands(self):
        for command in self.commands:
            command.execute()
            self.add_to_history(command)

    def print_history(self, file_path):
        if self.lock:
            self.lock.acquire()
        Successful_commands = [[h['command'], h['inputs'], h['output']]
                               for h in self.history if h['status'] == 'Success']

        Failed_commands = [[h['command'], h['inputs'], h['reason']]
                           for h in self.history if h['status'] == 'Failed']

        print(f"\n {len(Successful_commands)} commands executed successfully")
        print(f"\n {len(Failed_commands)} commands failed")

        # for command, inputfiles, outputfile in Successful_commands:
        #     print(f"{command}: {inputfiles} -> {outputfile}")
        # for command, inputfiles, reason in Failed_commands:
        #     print(f"{command}: {inputfiles} -> {reason}")

        old_history = []
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                old_history = json.load(f)
        with open(file_path, 'w') as f:
            json.dump(self.history + old_history, f, indent=4)

        if self.lock:
            self.lock.release()
