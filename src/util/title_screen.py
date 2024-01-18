import os
from sys import stdout
from time import sleep

from src.util.color import Color


class TitleScreen:
    """
    TitleScreen class to display the title screen and credits for the CLI application.
    """

    def __init__(self):
        self.ascii_art = self.load_ascii_art("src/util/ascii_art.txt")
        self.credit = f">{Color.ENDC} A CLI Interface for https://github.com/corincerami/mars-photo-api{Color.ENDC}\n\n"

    def load_ascii_art(self, file_path):
        """
        Load ASCII art from a file.
        """
        with open(file_path, "r") as file:
            return file.readlines()

    def title_screen(self):
        """
        Display the title screen ASCII art.
        """
        for line in self.ascii_art:
            print(Color.CRED2, line, end="")
            stdout.flush()
            sleep(0.001)

    def credits_animated(self):
        """
        Display animated credits.
        """
        print("")
        for char in self.credit:
            print(char, end="")
            stdout.flush()
            sleep(0.028)

    def credits(self):
        """
        Display credits without animation.
        """
        print("")
        print(self.credit)
        stdout.flush()

    def draw_banner(self):
        """Clear screen and draw the title screen."""
        os.system("clear")
        self.title_screen()
        self.credits()
