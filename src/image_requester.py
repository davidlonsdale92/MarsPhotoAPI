import os
import sys
from pprint import pprint

import inquirer
import requests

from src.util.title_screen import TitleScreen


class ImageRequester:
    def __init__(self, selected_rover, selected_camera, sol=0, earth_date=""):
        self.api_key = os.getenv("NASA_KEY")
        self.rover = selected_rover
        self.camera = selected_camera
        self.sol = sol
        self.earth_date = earth_date
        self.api_url = f"https://api.nasa.gov/mars-photos/api/v1/rovers/{self.rover.lower()}/photos"
        self.title_screen = TitleScreen()

    def check_directory(self, directory_path):
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
            print(f"Directory '{directory_path}' created.")
        else:
            print(f"Directory '{directory_path}' already exists.")

    def request_by_date(self):
        params = {
            "api_key": self.api_key,
            "camera": self.camera,
            "earth_date": self.earth_date,
        }

        directory_path = f"data/{self.rover}_photos/{params['camera']}/earth_date/{params['earth_date']}"
        self.check_directory(directory_path)

        print(f"{self.api_url}, {params}")

        # Make a GET request to the API
        response = requests.get(self.api_url, params=params)
        if response.status_code == 200:
            print("Downloading images...")
        else:
            print(response)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            data = response.json()

            # Extract and process the photos
            photos = data["photos"]

            for photo in photos:
                photo_id = photo["id"]
                earth_date = photo["earth_date"]
                camera = photo["camera"]["name"]
                img_url = photo["img_src"]
                img_filename = os.path.join(
                    f"data/{self.rover}_photos/{params['camera']}/earth_date/{params['earth_date']}",
                    f"{params['camera']}_{params['earth_date']}_{photo['id']}.jpg",
                )
                earth_date = photo["earth_date"]

                try:
                    response = requests.get(img_url, timeout=10)
                    if response.status_code == 200:
                        print(f"\033[1;33m\nPhoto ID: {photo_id}\033[0m")
                        print(f"Earth Date: {earth_date}")
                        print(f"Camera: {camera}")
                        print(f"Image Source: {img_url}")
                        print("-" * 30)
                        with open(img_filename, "wb") as img_file:
                            img_file.write(response.content)
                    else:
                        print(
                            f"\033[1;31m\nError downloading image {img_url}, \
                            status code: {response.status_code}\033[0m"
                        )
                except requests.exceptions.RequestException as e:
                    print(f"\033[1;31m\nError connecting to {img_url}: {e}\033[0m")

            self.title_screen.draw_banner()
            print("Download complete.")

        else:
            print(f"\033[1;31m\nRequest failed: {response.status_code}\033[0m")

    def request_by_sol(self):
        params = {"api_key": self.api_key, "camera": self.camera, "sol": self.sol}

        directory_path = (
            f"data/{self.rover}_photos/{params['camera']}/sol/{params['sol']}"
        )
        self.check_directory(directory_path)

        print(f"{self.api_url}, {params}")

        # Make a GET request to the API
        response = requests.get(self.api_url, params=params)

        if response.status_code == 200:
            print("Downloading images...")
        else:
            print(response)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()

            # Extract and process the photos
            photos = data["photos"]

            for photo in photos:
                photo_id = photo["id"]
                sol = photo["sol"]
                camera = photo["camera"]["name"]
                img_url = photo["img_src"]
                img_filename = os.path.join(
                    f"data/{self.rover}_photos/{params['camera']}/sol/{params['sol']}",
                    f"{params['camera']}_{params['sol']}_{photo['id']}.jpg",
                )
                earth_date = photo["earth_date"]

                try:
                    response = requests.get(img_url, timeout=10)
                    if response.status_code == 200:
                        print(f"\033[1;33m\nPhoto ID: {photo_id}\033[0m")
                        print(f"SOL: {sol}")
                        print(f"Camera: {camera}")
                        print(f"Image Source: {img_url}")
                        print(f"Earth Date: {earth_date}")
                        print("-" * 30)
                        with open(img_filename, "wb") as img_file:
                            img_file.write(response.content)
                    else:
                        print(
                            f"\033[1;31m\nError downloading image {img_url}, \
                            status code: {response.status_code}\033[0m"
                        )
                except requests.exceptions.RequestException as e:
                    print(f"\033[1;31m\nError connecting to {img_url}: {e}\033[0m")

            self.title_screen.draw_banner()
            print("Download complete.")

        else:
            print(f"\033[1;31m\nRequest failed: {response.status_code}\033[0m")
