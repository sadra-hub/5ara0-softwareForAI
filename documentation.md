![intro](/assets/intro.png)
## Table of Contents
- [Introduction](#introduction)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Architecture](#architecture)
  - [Data Structure](#data-structure)
  - [Image Recognition Model](#image-recognition-model)
  - [Betting Strategy](#betting-strategy)
- [Usage](#usage)
  - [Running the Bot](#running-the-bot)
  - [Understanding Strategies](#understanding-strategies)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Introduction
The Kuhn Poker Bot is an AI-powered tool designed to play Kuhn poker. It utilizes an image recognition model to detect the cards dealt to the player and implements sophisticated betting strategies based on the number of cards in play (three and four card betting strategies).

## Getting Started

### Prerequisites
Before running the Kuhn Poker Bot, ensure you have the following software installed:
- Python 3.9
- TensorFlow
- DCV
- For a a list of dependencies: [Mac](environment_mac.yml), [Windows](environment.yml), [Linux](environment_linux.yml)

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/tue-5ARA0-2024-Q1/pokerbot-pokerbot-29.git
   cd kuhn-poker-bot
   ```

2. Creata a new Conda environment and Install the required dependencies (choose environment file based on your OS):
    ```bash
    conda env create -f environment.yml
    ```

## Architecture
In this section we go through architecture and design choices we made througout the development process.

### Data Structure
<!-- Yunus is reponsible for documenting the data sets generation and will add his contrbutions later. -->

### Image Recognition Model
<!-- Sadra is responsible for this part -->
The bot employs an image recognition model built using TensorFlow to analyze the visual representation of the poker cards. The model processes images captured from the poker table to accurately identify which cards have been dealt.

### Betting Strategy
<!-- Farah can add his contributions here -->
