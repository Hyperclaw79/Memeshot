import unittest
import os
import sys
import importlib
sys.path.append(os.getcwd().replace('tests', 'memeshot'))
from shotgrab import ScreenshotGrabber


class TestShotgrabber(unittest.TestCase):
    def test_videonotfound(self):
        with self.assertRaises(ScreenshotGrabber.VideoNotFound):
            shotty = ScreenshotGrabber("a video that doesn't exist")

    def test_ts2secs(self):
        secs = ScreenshotGrabber._ts2secs(self, "00:01:59")
        self.assertEqual(secs, 124)

    def test_invalid_ts2secs(self):
        with self.assertRaises(ValueError):
            secs = ScreenshotGrabber._ts2secs(
                self,
                "wrongly formatted timestamp"
            )

    def test_screenshots(self):
        ss_folder = os.path.join(
            os.getcwd().replace('tests', 'memeshot'),
            "screenshots"
        )
        if not os.path.exists(ss_folder):
            os.makedirs(ss_folder)
        shotty = ScreenshotGrabber("test_vid.mp4")
        shotty.get_screenshots(["00:00:01"])
        self.assertIn("memeshot_6secs.jpg", shotty.created_ss)
