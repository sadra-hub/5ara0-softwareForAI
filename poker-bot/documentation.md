![intro](assets/intro.png)
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

### Image Normalization
The `normalize_image` function transforms the pixel values of an input image into a normalized 2D matrix with values between 0 and 1. This process first converts the image into a NumPy array and then normalizes pixel values by dividing by 255 to ensure consistent results across images, which the model can then use for card rank prediction.

### Loading the dataset
The `load_data_set` function loads images, normalizes them using `normalize_image`, and extracts labels from the filenames. It then applies a train-validation split as per the provided ratio, returning both image arrays and label matrices.

### Generating the dataset
The dataset is generated using predefined card ranks (`J, ``Q, ``K) with noise levels and slight rotations added to each image for variety. Using ``generate_data_set`, images are randomly rotated by up to 15 degrees and assigned a noise level ranging from 0 to 1. Generated images are labeled and saved.

Each image is saved in the appropriate `training_images` or `test_images` directory. This approach allows for batch generation, provided the number of samples is given.


### Image Recognition Model
The bot employs an image recognition model built using TensorFlow to analyze the visual representation of the poker cards. The model processes images captured from the poker table to accurately identify which cards have been dealt.
![model](assets/model.png)

CNN was chosen as the model for this task due to its ability to process and learn effectively from image data. CNNs automatically extract relevant features from raw pixel values through convolutional layers, building spatial hierarchies from simple edges to complex textures, making them ideal for image classification. 

For this model, 7 layers are used, balancing sufficient complexity for feature extraction without excessive risk of overfitting. The model is defined with seven layers: two convolutional and pooling layers, a flatten layer, a dense hidden layer, and an output layer with softmax activation.

The primary evaluation metric is the loss value, calculated using `sparse categorical crossentropy`. This metric is especially suitable for multi-class classification as it evaluates the probabilities assigned to each class, helping the model distinguish between classes effectively, even with noisy data.


The model is trained using the generated test dataset. `train_model()` normalizes the images, verifies shape compatibility, trains the model for 10 epochs, and saves the model if write_to_file is set to True. The saved model is accessed through the `load_model()` function.
The model can be built and trained through the following commands

```bash
    model = build_model()  # Build a new model
    history = train_model(model, n_validation=200, write_to_file=False)
```

The performance of the model is then evaluated on the test dataset with loss and accuracy as chosen metrics. The function `evaluate_model()` returns a loss value calculated using the loss function that reflects how well the model generalizes to the unseen and noisy test data.

The classification of a raw_image is done using the `identify()` function. The raw image is normalised and reshaped for the model's input. An extra dimension is added to the image array as required by the model and a prediction is made using the preprocessed input image. The class corresponding the index `0 for ‘J’, 1 for ‘Q’, and 2 for ‘K’` with the highest probability in the prediction array is returned

The training histories are stored and used to visualise a training history. The graph plots a learning curve for accuracy and loss of the model over the trained epochs.

![model](assets/learning_curve.png)

On the Accuracy graph generated on the left, the general trend seems to be gradual improvements to 1.0 starting at 0.96. The model's accuracy improvement suggests it is effectively learning patterns in the training data. Peaking near 1.0 after 30 epochs is an indicator of strong training convergence.

On the Loss Graph generated on the right, the general trends is rapid decrease to almost 0 starting at 0.14 by the 50the epoch. This suggests that the model is minimizing errors effectively over the training set and is achieving a good performance.

Overall, with high accuracy and low loss, the model is working efficintly on training data.


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

### Kuhn Poker Strategy
In our poker agent implementation, we focus on maximizing the expected payoff based on the card dealt and the current game state. The game of Kuhn Poker revolves around three cards—Jack (`J), Queen (Q), and King (K)—with ``K` being the highest-ranked card and `J` being the lowest. However, simply holding a higher card doesn't guarantee a win; the key to a successful strategy lies in predicting the opponent’s behavior and adjusting actions accordingly.

Our strategy divides the agent’s behavior into two distinct roles: Initial Player (starting the round) and Responding Player (reacting to the initial player’s action). Each role uses different sets of probabilities depending on the player's card and the available moves.

#### Initial Player Strategy
When acting as the Initial Player, the agent’s first action depends on whether a previous move has been made in the round:

First Move: If the game just started (no previous moves), the agent must choose between `CHECK` or `BET. The probabilities for this decision are based on the card held (J, ``Q, or ``K). For instance, with a ``J, the agent is more likely to ``CHECK` defensively, while a `K` increases the likelihood of betting.

Next Move: If a betting action has already occurred, the agent evaluates whether to `CALL` or `FOLD, again based on the card held. For example, a ``K` is more likely to `CALL` as it is the highest-ranked card.

#### Responding Player Strategy
When the agent is the Responding Player, the strategy hinges on how the Initial Player acted:

Initial Player Checked: The agent now chooses whether to `CHECK` or `BET. The decision weights vary by card. For example, a ``Q` is highly likely to `CHECK`.

Initial Player Bet: The agent must decide whether to `CALL` or `FOLD. As with the Initial Player, the agent's choice is informed by the card it holds. A ``K` will always `CALL, while a ``J` is more inclined to `FOLD`.

### Probabilistic Approach
Each decision made by the agent is driven by assigned probabilities tailored to the specific card held. These probabilities are adjusted randomly to introduce some level of unpredictability, ensuring the agent is not easily predictable across rounds.

For example, the following probabilities are assigned for the Initial Player when deciding whether to `CHECK` or `BET` on the first move:

`J`: $[1 - \alpha, \alpha]$ 
`K`: $[1 - 3\alpha, \alpha]$ 
`Q`: $[1, 0]$ 
Similarly, for the third move, when deciding between `CALL` and `FOLD` the probabilities shift depending on the card.

For the Initial Player's next move after the Responding Player's move, when deciding whether to `CALL` or `FOLD`, the probabilities shift depending on the strength of the card. This decision is triggered after the first player has already made an action and is now facing the decision to call or fold.

`J`: $[0, 1]$ 
`K`: $[1, 0]$ 
`Q`: $[1/3 + \alpha, 2/3 - \alpha]$ 

The above reflects that holding a `J` is always going to lead to a fold, whereas `K` are always called, and `Q` are also more likely to fold but still have some chance of calling based on the randomness introduced by $\alpha$.

Then, for the Responding Player: they can react to the first player's decision, where no bets have been placed, and the opponent has checked. The responding player must now decide whether to CHECK or BET. Again, the card held by the agent influences this decision.

`J`: $[2/3, 1/3]$ 
`K`: $[0, 1]$ 
`Q`: $[1, 0]$ 

In this scenario, `Q` is always going to check, while `J` are more likely to check. `K`, on the other hand, always bet.

In the other case, the Responding Player is facing a bet from the first player and must now decide whether to CALL or FOLD.

`J`: $[0, 1]$ 
`K`: $[1, 0]$ 
`Q`: $[1/3, 2/3]$ 

The `J` will always fold when facing a bet. `K` will always call and `Q` are also more likely to fold but may occasionally call.

### Agent Implementation
The agent’s strategy is implemented in two main functions:

`InitialPlayerStrategy`: Determines the action for the player who starts the round, taking into account whether any moves have been made and the card held.

`RespondingPlayerStrategy`: Determines the action for the player who responds to the Initial Player, based on the available actions and the card.

These functions are invoked by the `make_action` method, which first identifies the player’s turn order and then selects the appropriate strategy. The state of the game and round (including the current card and available actions) are passed into these strategies to make a decision.

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

## References
https://en.wikipedia.org/wiki/Kuhn_poker - Check optimal strategy section
## Acknowledgments
+ Thanks to the instructors for their valuable feedback and improvements to this project.
+ Special thanks to the developers of the libraries used in this project: TensorFlow, Pytest, and others.