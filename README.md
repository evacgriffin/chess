# Falcon - Hunter Console Chess

## Table of Contents

- [Description](#description)
- [Installation](#installation)
- [Usage](#usage)
- [Featured Design Principles](#featured-design-principles)
- [License](#license)
- [Roadmap](#roadmap)

## Description

In this text-based Falcon-Hunter Console Chess game, two players take turns to make moves on a chess board in a race to 
capture the opponent's king. The game is played entirely in the terminal. After each move, feedback and an updated view 
of the chess board are printed to the console.

![Game introduction](assets/chess_intro.png)
![White moves a piece](assets/chess_demo1.png)
![Black moves a piece](assets/chess_demo2.png)

## Installation

Note: This project was written and tested in Python 3.11. Although it may run in earlier versions of Python, I recommend 
using Python 3.11 or newer.

1. Clone the repository to your local machine:
    ```shell
    git clone https://github.com/evacgriffin/chess.git
   ```
2. Navigate into the project directory:
   ```shell
   cd chess
   ```
3. Install other required dependencies:
   ```shell
   pip install -r requirements.txt
   ```
4. Run the game:
   ```shell
   python main.py
   ```

## Usage

## Featured Design Principles

- Object-oriented design
- Separation of concerns
- Unit testing
- Type hinting
- Detailed doc strings and comments

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Roadmap

- [ ] Design and implement GUI
- [ ] Port to be playable online
- [ ] Add different game modes
- [ ] Add additional special chess pieces