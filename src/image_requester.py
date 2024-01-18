import os

import requests
from tqdm import tqdm

from src.util.title_screen import TitleScreen


class ImageRequester:
    def __init__(self, selected_rover, selected_camera, sol=0, earth_date=""):
        self.api_key = os.getenv("NASA_KEY")
        self.rover = selected_rover.lower()
        self.camera = selected_camera
        self.sol = sol
        self.earth_date = earth_date
        self.api_url = (
            f"https://api.nasa.gov/mars-photos/api/v1/rovers/{self.rover}/photos"
        )
        self.title_screen = TitleScreen()

    def check_directory(self, directory_path):
        os.makedirs(directory_path, exist_ok=True)
        print(f"Directory checked: '{directory_path}'")

    def download_image(self, photo, directory_path, pbar):
        img_url = photo["img_src"]
        img_filename = os.path.join(directory_path, f"{photo['id']}.jpg")

        try:
            response = requests.get(img_url, stream=True, timeout=10)
            if response.status_code == 200:
                with open(img_filename, "wb") as img_file:
                    for chunk in response.iter_content(chunk_size=8192):
                        img_file.write(chunk)
            else:
                tqdm.write(
                    f"Failed to download {img_url}, status code: {response.status_code}"
                )  # Using tqdm.write
        except requests.exceptions.RequestException as e:
            tqdm.write(f"Error connecting to {img_url}: {e}")  # Using tqdm.write

    def request_images(self, params):
        directory_path = f"data/{self.rover}_photos/{self.camera}/{self.sol if self.sol else self.earth_date}"
        self.check_directory(directory_path)

        print(f"Requesting images from {self.api_url}")
        response = requests.get(self.api_url, params=params)

        if response.status_code == 200:
            photos = response.json().get("photos", [])
            with tqdm(total=len(photos), desc="Downloading images", unit="img") as pbar:
                for photo in photos:
                    self.download_image(photo, directory_path, pbar)
                    pbar.update(1)
            print("Download complete.")
        else:
            print(f"Request failed: {response.status_code}")

        self.title_screen.draw_banner()

    def request_by_date(self):
        params = {
            "api_key": self.api_key,
            "camera": self.camera,
            "earth_date": self.earth_date,
        }
        self.request_images(params)

    def request_by_sol(self):
        params = {"api_key": self.api_key, "camera": self.camera, "sol": self.sol}
        self.request_images(params)
