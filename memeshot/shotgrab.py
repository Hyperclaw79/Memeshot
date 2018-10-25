#!/usr/bin/env python3

import cv2
from datetime import datetime, timedelta
import os
import re
import sys
from subgrab import SubtitleGrabber


class ScreenshotGrabber:
    """
    The ScreenshotGrabber class extracts screenshot from a video file.
    The __init__() method creates a CV2 video capture object.
    Functions:
        get_screenshots: For getting the screenshot from
            a video at given timestamps.
    Exceptions:
        VideoNotFound: If the video file is not found
            in the specified location.
    """
    def __init__(self, vid_path):
        self.vid_path = vid_path
        if not os.path.exists(self.vid_path):
            raise self.VideoNotFound("Could not find the specified video.")
        else:
            self.cap = cv2.VideoCapture(self.vid_path)
            self.created_ss = []

    def _ts2secs(self, ts) -> int:
        """
        The util function to convert a timestamp into seconds.
        Parameters:
            :ts: A timestamp string in the format HH:MM:SS.
        Returns:
            Time interval in seconds -> <int>
        """
        if not re.match(r'\d{2}\:[0-5]\d\:[0-5]\d', ts):
            raise ValueError("Invalid format for timestamp.")
        else:
            t_obj = datetime.strptime(ts, '%H:%M:%S')
            td = timedelta(
                hours=t_obj.hour,
                minutes=t_obj.minute,
                seconds=t_obj.second
            )
            # Add approx 5 secs to start times to get a better timed image.
            seconds = int(td.total_seconds()) + 5
            return seconds

    def _grabber(self, seconds):
        """
        The util function to generate screenshots.
        The video is streamed to the given time (in seconds) first.
        Then the current frame is screenshotted
            and stored in screenshots folder.
        Parameters:
            :seconds: The time in seconds rounded off as integers.
        Returns:
            None/"success"
        """
        # Set Capture Position at given seconds.
        self.cap.set(cv2.CAP_PROP_POS_MSEC, seconds*1000)
        success, image = self.cap.read()
        if success:
            cv2.imwrite(f"screenshots/memeshot_{seconds}secs.jpg", image)
            self.created_ss.append(f"memeshot_{seconds}secs.jpg")
            print(f"Added memeshot_{seconds}secs.jpg to Screenshots folder.")
            if cv2.waitKey(10) == 27:  # Exit if Escape is hit.
                sys.exit(0)
            return "success"

    def get_screenshots(self, timestamps):
        """
        The main handler function for screenshot generation.
        Converts the timestamps into seconds and grabs screenshots.
        Parameters:
            :timestamps: A list containing timestamps.
        Returns:
            None
        """
        seconds_list = [self._ts2secs(ts) for ts in timestamps]
        success_list = []
        try:
            for seconds in seconds_list:
                success_list.append(self._grabber(seconds))
            if success_list.count("success") > 0:
                print(
                    "Memeshot successfully obtained"
                    f" {len(timestamps)} screenshots."
                )
            else:
                print("Memeshot failed to obtain any screenshots.")
        except Exception as e:
            print(str(e))

    class VideoNotFound(Exception):
        """
        Raised if the video file is not found in the specified location.
        """
        pass

if __name__ == '__main__':
    # Take the user inputs
    vid_path = input("Enter the path to the video:\n")
    srt_path = input("Enter the path to the srt file:\n")
    word = input("Enter the search word:\n")
    try:
        subby = SubtitleGrabber(srt_path)
        timestamps = subby.get_timestamps(word)
        shotty = ScreenshotGrabber(vid_path)
        # Create the screenshots folder if it does not exist.
        if not os.path.exists("screenshots"):
            os.makedirs("screenshots")
        shotty.get_screenshots(timestamps)
    except ScreenshotGrabber.VideoNotFound as e:
        print(str(e))
