import unittest
import os
import sys
sys.path.append(os.getcwd().replace('tests', 'memeshot'))
from subgrab import SubtitleGrabber


class TestSubgrabber(unittest.TestCase):
    def test_valid_init(self):
        subby = SubtitleGrabber("valid.srt")
        self.assertGreater(len(subby.srt_dict), 0)

    def test_srtnotfound(self):
        with self.assertRaises(SubtitleGrabber.SrtNotFound):
            subby = SubtitleGrabber("RandomFileThatDoesn'tExist")
        with self.assertRaises(SubtitleGrabber.InavlidSrt):
            subby = SubtitleGrabber("invalid.srt")

    def test_valid_timestamps(self):
        subby = SubtitleGrabber("valid.srt")
        timestamps = subby.get_timestamps("the")
        self.assertIsInstance(timestamps, list)
        self.assertIsNotNone(timestamps)
        self.assertEqual(len(timestamps), 4)

    def test_valid_dialogues(self):
        subby = SubtitleGrabber("valid.srt")
        dialogues = subby.get_dialogues("the")
        self.assertIsInstance(dialogues, list)
        self.assertIsNotNone(dialogues)
        self.assertEqual(len(dialogues), 4)
