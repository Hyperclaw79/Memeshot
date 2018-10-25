import re
import sys


class SubtitleGrabber:
    """
    The SubtitleGrabber class extracts information from an .srt file.
    The __init__() method compiles a dictionary that,
        maps timestamps to the dialogues.
    Functions:
        The class includes the following functions:
            1. get_dialogues: For getting dialogues based on search word.
            2. get_timestamps: For getting the start times
                of dialogues with a search word.
    Exceptions:
        The class includes the following Exceptions:
            1. SrtNotFound: If the .srt is not found in the specified location.
            2. InavlidSrt: If the .srt doesn't follow the standard .srt format.
    """
    def __init__(self, srt_path):
        self.srt_path = srt_path
        try:
            with open(self.srt_path) as f:
                srt_raw = f.read().splitlines()
        except FileNotFoundError:
            raise self.SrtNotFound("Could not find the specifed .srt file.")

        lineno_patt = re.compile(r'^\d+$')  # Get rid of line numbers
        srt_lines = [
            line.lower()
            for line in srt_raw
            if not lineno_patt.match(line) and line != ''
        ]
        if not srt_lines:
            raise self.InavlidSrt("Invalid Format/Empty .srt file.")
        try:
            # Concatenate multiline dialogues into a single one.
            srt_lines = self._concatenator(srt_lines)
            self.srt_dict = {
                srt_lines[i]: srt_lines[i+1]
                for i in range(0, len(srt_lines) - 1, 2)
            }
        except Exception as e:
            raise self.InavlidSrt("Invalid Format/Empty .srt file.")

    def _concatenator(self, info) -> list:
        """
        The util function to concatenate multiline dialogues
            into a single line.
        Parameters:
            :info: A list containing lines from .srt file,
                excluding line numbers and empty lines.
        Returns:
            Processed info with alternating timestamps and dialogues -> [list]
        """
        processed = [""] * len(info)
        for i in range(len(info)):
            # Check whether the starting character is a letter.
            if info[i][0].isalpha():
                dialogue = ''
                j = i
                while i < len(info):
                    if info[i][0].isdigit():
                        break
                    dialogue = dialogue + info[i] + ' '
                    i += 1
                if not any([
                    value for value in processed
                        if dialogue in value
                ]):
                    processed[j] = dialogue
            else:
                processed[i] = info[i]
        # Get rid of empty lines
        refined_info = [line for line in processed if line]
        return refined_info

    # Functions

    def get_timestamps(self, word) -> list:
        """
        Get all the timestamps with search word in the corresponding dialogues.
        Parameters:
            :word: The search word that needs to be found in the dialogues.
        Returns:
            A collection of start times from the timestamps -> [list]
        """
        timestamps = [
            ts.split(',')[0]
            for ts, dialogue in self.srt_dict.items()
            if word in dialogue.split()
        ]
        return timestamps

    def get_dialogues(self, word) -> list:
        """
        Get a list of all the dialogues containing the search word.
        Parameters:
            :word: The search word that needs to be found in the dialogues.
        Returns:
            A collection of dialogues -> [list]
        """
        dialogues = [
            dialogue.title()
            for dialogue in self.srt_dict.values()
            if word in dialogue.split()
        ]
        return dialogues

    # Exceptions

    class SrtNotFound(Exception):
        """
        Raised if .srt file is not found in the specified location.
        """
        pass

    class InavlidSrt(Exception):
        """
        Raised if the .srt cannot be processed into a dictionary mapping
            of timestamps to dialogues.
        """
        pass

if __name__ == '__main__':
    srt_path = input("Enter location to the srt file:\n")
    try:
        st_grabber = SubtitleGrabber(srt_path)
    except SubtitleGrabber.SrtNotFound:
        print("Incorrect path provided for the srt file.")
        sys.exit(1)
    except SubtitleGrabber.InavlidSrt:
        print(
            "The srt file is either empty"
            "or does not follow the standard format."
        )
        sys.exit(1)
    word = input("Enter the searchword:\n").lower()
    modes = [
        {
            "Sl": "1",
            "Type": "Get Timestamp",
            "function": st_grabber.get_timestamps
        },
        {
            "Sl": "2",
            "Type": "Get Dialogues",
            "function": st_grabber.get_dialogues
        }
    ]
    modes_disp_str = '\n'.join([
        f'{_mode["Sl"]}. {_mode["Type"]}' for _mode in modes
    ])
    if len(sys.argv) < 2:
        while True:
            mode = input(
                "Enter the corresponding number for your choice:\n"
                f"\n{modes_disp_str}\n"
            )
            if mode.isdigit() and int(mode) in range(1, len(modes)+1):
                func = [
                    _mode["function"]
                    for _mode in modes
                    if _mode["Sl"] == mode
                ][0]
                print('\n'.join(func(word)))
                break
            else:
                print(f"Only digits from 1 to {len(modes)} are acceptable.")
    else:
        if sys.argv[1].lower() in ["dialogues", "timestamps"]:
            func = st_grabber.__getattribute__(f'get_{sys.argv[1]}')
            print('\n'.join(func(word)))
        else:
            print(f"The only accepted modes are:\n{modes_disp_str}\n")