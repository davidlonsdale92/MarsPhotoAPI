# ----------------------------------------------------------------------------------------------------------#
# ███╗   ███╗ █████╗ ██████╗ ███████╗    ██████╗ ██╗  ██╗ ██████╗ ████████╗ ██████╗      █████╗ ██████╗ ██╗
# ████╗ ████║██╔══██╗██╔══██╗██╔════╝    ██╔══██╗██║  ██║██╔═══██╗╚══██╔══╝██╔═══██╗    ██╔══██╗██╔══██╗██║
# ██╔████╔██║███████║██████╔╝███████╗    ██████╔╝███████║██║   ██║   ██║   ██║   ██║    ███████║██████╔╝██║
# ██║╚██╔╝██║██╔══██║██╔══██╗╚════██║    ██╔═══╝ ██╔══██║██║   ██║   ██║   ██║   ██║    ██╔══██║██╔═══╝ ██║
# ██║ ╚═╝ ██║██║  ██║██║  ██║███████║    ██║     ██║  ██║╚██████╔╝   ██║   ╚██████╔╝    ██║  ██║██║     ██║
# ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝    ╚═╝     ╚═╝  ╚═╝ ╚═════╝    ╚═╝    ╚═════╝     ╚═╝  ╚═╝╚═╝     ╚═╝
# ----------------------------------------------------------------------------------------------------------#
# A Python terminal interface for interacting with the Mars Photo API by CorinCerami:
# https://github.com/corincerami/mars-photo-api
#

import os

from src.controller import Controller
from src.util.title_screen import TitleScreen


class Menu:
    """Menu class to handle the main menu and user interactions."""

    def __init__(self):
        self.title_screen = TitleScreen()
        self.main()

    def main(self):
        """
        Main method to display the menu and handle user choices.
        """
        os.system("clear")
        self.title_screen.title_screen()
        self.title_screen.credits_animated()
        self.controller = Controller()


if __name__ == "__main__":
    app = Menu()
