import datetime
import json
import os
import sys

import inquirer

from src.image_requester import ImageRequester
from src.util.theme import CustomTheme
from src.util.title_screen import TitleScreen


class Controller:
    """Controller class to handle rover and camera operations."""

    def __init__(self):
        self.theme = CustomTheme()
        self.title_screen = TitleScreen()
        self.rover_options = self.load_rover_options("src/util/rover_options.json")
        self.run()

    def load_rover_options(self, file_path):
        """Load rover options from a JSON file."""
        with open(file_path, "r") as file:
            return json.load(file)

    def display_menu(self, message, choices):
        """Generic method to display a menu and return the selected option."""
        self.title_screen.draw_banner()
        question = [inquirer.List("choice", message=message, choices=choices)]
        return inquirer.prompt(question, theme=self.theme)["choice"]

    def request_attributes(self, selected_rover, selected_camera_key, date_value):
        """Request images based on the selected attributes."""
        request = ImageRequester(selected_rover, selected_camera_key, date_value)
        if isinstance(date_value, int):
            request.request_by_sol()
        else:
            request.request_by_date()

    def post_download_menu(self):
        questions = [
            inquirer.List(
                "action",
                message="What would you like to do next?",
                choices=["Return to Main Menu", "Exit"],
            )
        ]
        return inquirer.prompt(questions, theme=self.theme)["action"]

    def select_rover(self):
        rover_choices = list(self.rover_options.keys()) + ["Exit"]
        return self.display_menu("\033[1;31mSelect rover", rover_choices)

    def select_camera(self, selected_rover):
        camera_choices = [
            f"{cam[0]} - {cam[1]}" for cam in self.rover_options[selected_rover]
        ] + ["Back"]
        return self.display_menu("\033[1;31mSelect camera", camera_choices)

    def select_date(self):
        return self.display_menu(
            "\033[1;31mSelect a date option", ["Sol", "Earth Date", "Back"]
        )

    def run(self):
        current_step = "select_rover"
        while True:
            if current_step == "select_rover":
                selected_rover = self.select_rover()
                if selected_rover == "Exit":
                    sys.exit(0)
                current_step = "select_camera"

            if current_step == "select_camera":
                selected_camera = self.select_camera(selected_rover)
                if selected_camera == "Back":
                    current_step = "select_rover"
                    continue
                selected_camera_key = selected_camera.split(" - ", 1)[0]
                current_step = "select_date"

            if current_step == "select_date":
                date_option = self.select_date()
                if date_option == "Back":
                    current_step = "select_camera"
                    continue

            if date_option == "Sol":
                while True:
                    self.title_screen.draw_banner()
                    sol_value = inquirer.prompt(
                        [inquirer.Text("sol", message="Enter Sol value:")],
                        theme=self.theme,
                    )["sol"]
                    if sol_value.isdigit():
                        self.request_attributes(
                            selected_rover, selected_camera_key, int(sol_value)
                        )

                        next_action = self.post_download_menu()

                        if next_action == "Return to Main Menu":
                            self.run()
                        elif next_action == "Exit":
                            sys.exit(0)

                    else:
                        print(
                            "\033[1;31mInvalid input. Please enter a valid integer.\033[0m"
                        )
            else:
                while True:
                    self.title_screen.draw_banner()
                    date_input = inquirer.prompt(
                        [inquirer.Text("date", message="Enter date (YYYY-MM-DD):")],
                        theme=self.theme,
                    )["date"]
                    try:
                        date_value = datetime.datetime.strptime(
                            date_input, "%Y-%m-%d"
                        ).date()
                        self.request_attributes(
                            selected_rover, selected_camera_key, date_value
                        )

                        next_action = self.post_download_menu()

                        if next_action == "Return to Main Menu":
                            self.run()
                        elif next_action == "Exit":
                            sys.exit(0)

                    except ValueError:
                        print(
                            "\033[1;31m\nInvalid input. Please enter a valid date (YYYY-MM-DD).\033[0m"
                        )
