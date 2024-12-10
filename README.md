# **CV Hackathon 2024**

# Visual Question Answering (VQA) Application

## Overview

This project is a Visual Question Answering (VQA) application developed for the **CV Hackathon**. The app allows users to query an image and receive the most relevant textual response based on the content of the image. The application leverages the **Dandelin ViLT** model, a Transformer-based Vision-Language model for tasks such as image understanding and textual question answering. The app is built using **Flet**, a framework for building interactive desktop, web and mobile applications.

### Key Features:
- Upload an image for analysis.
- Ask questions related to the image.
- Get accurate, context-aware answers based on the content of the image.

## Tech Stack

- **Flet**: A framework for building real-time, multi-user, desktop and web applications in Python. [Flet Documentation](https://flet.dev)
- **Dandelin ViLT**: A Vision-Language Transformer model - `dandelin/vilt-b32-finetuned-vqa` for visual question answering. [ViLT](https://github.com/dandelin/ViLT)
- **Python**: The main programming language used for building the application.
  
## Installation
Follow these steps to set up the VQA application locally.

**Prerequisites**
Make sure you have the following installed:
- Python 3.7+
- `pip` for installing dependencies

### Clone the Repository

```bash
# clone the repository and switch to `dev` branch
git clone https://github.com/r0-h-1t/cving.git
cd Cving
git switch dev
```

### Install packages
```bash
# create virtualenv
python3 -m venv venv

# activate virtualenv
.\venv\Scripts\Activate.ps1 # for Windows

source ./venv/bin/actiavte

# install the requirements
pip install -r ./requirements.txt 
```

### Run the app
```bash
# run as desktop app
flet run ./app

# run as web app
flet run --web -p 8000 ./app
```
