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
  - [Game Variations](#game-variations)
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
- For a a list of dependencies: [Windows](environment.yml), [Linux](environment_linux.yml)

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

#### DVC: Dataset and Model Version Control
We're using DVC and a bucket running on Amazon Web Service (AWS) as storage at the following address: 
`https://pokerbot-29-dvc.s3.eu-north-1.amazonaws.com`

To access the models stored while training, you have the run the following commands: 
```bash
conda install -c conda-forge awscli
conda install -c conda-forge dvc
aws configure
	-> key id : <ask-for-a-key-ID>
	-> secret key: <ask-for-a-secret-key>
	-> region: eu-north-1
	-> format: json
dvc remote add -d s3remote s3://pokerbot-29-dvc
dvc remote modify s3remote endpointurl https://s3.eu-north-1.amazonaws.com
```

### Betting Strategy
<!-- Farah can add his contributions here -->

## Usage

### Running the Bot
 we won't go into details of how to run this spot as the details have already been discussed [here](README.md). Please follow the instructions. To put it briefly, You can play an online game with our client against a bot by running the following command:

```bash
python main.py --token <token UUID here> --play "bot" --global
```

### Game Variations
You can define a `--cards` argument to play a 4-card Kuhn Poker, instead of a regular 3-card game. In case not specified, the bot will default to play a 3-card game. Please refer to [Betting Strategy](#betting-strategy) to better understand how each betting strategy work.

```bash
python main.py --token <token UUID here> --play "bot" --cards "4" --global
```

## Contributing
We welcome contributions from the community! If you would like to contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/YourFeature`).
3. ake your changes and commit them (`git commit -m 'Add new feature'`).
4. Push to the branch (git push origin feature/YourFeature).
5. Open a Pull Request and assign either of us for a review.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE.md) file for details.

## Acknowledgments
+ Thanks to the instructors for their valuable feedback and improvements to this project.
+ Special thanks to the developers of the libraries used in this project: TensorFlow, Pytest, and others.