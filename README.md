<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="./readme_images/logo_dark.png">
    <img src="./readme_images/logo_light.png">
  </picture>
</p>

---

This project is broken down into multiple parts:

- An interactive Python terminal for communicating with the [Mars Photo API](https://github.com/corincerami/mars-photo-api) by CorinCerami.
- An image processing tool for preparing the data.
- A machine learning model using OpenCV4 for feature extraction.

![](documentation_images/App.png)

---

## Installation

Install the required packages with pip:

```
python -m pip install -r requirements.txt
```

Then run:

```
python parser.py -f input_file.txt -o output_file.txt -v
```

---

## How to use

- Use the terminal to query the API and download images filtered by Rover, Camera and Sol/Earth Date.
- Once the images are downloaded, run the image processor from the main menu.
- Finally, run the machine learning model.

The model included is traind specifcally for for geological feature extraction, however, you can add your own model to the model folder in the directory to run it against that.
