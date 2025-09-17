# Flappy Bird Clone by Edo

This is a complete, standalone Flappy Bird clone created in Python using the Pygame library. Originally built as a learning exercise, this project covers the full development cycle from basic mechanics to a polished, distributable application with a local high score system.

## Features

* **Classic Gameplay:** Experience the familiar "flap to fly" mechanics.
* **Dynamic Visuals:** Each round randomly selects a bird color (yellow, blue, or red) and a background (day or night).
* **Themed Obstacles:** The pipe colors change to match the background (green for day, red for night).
* **Local High Score System:** The game saves your top 10 scores locally in a `local_scores.db` file, which is created in the same directory as the game.
* **Polished Experience:** Includes sound effects, sprite animations, and a clean user interface.

## How to Play

* **Start/Restart:** Press the `SPACEBAR` on the menu screen to begin a new game.
* **Flap:** Press the `SPACEBAR` during the game to make the bird flap upwards.
* **Objective:** Navigate through the pipes for as long as possible to get the highest score.
* **Save Score:** After a game over, you can type your name and press `ENTER` to save your score to the local leaderboard.

## How to Run (for Developers)

1.  Clone this repository.
2.  Create and activate a Python virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```
3.  Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```
4.  Run the game:
    ```bash
    python main.py
    ```

## Project Structure

* `main.py`: The main, standalone game application.
* `requirements.txt`: A list of the Python packages needed to run the project (primarily `pygame`).
* `sprites/` & `audio/`: Folders containing the game's visual and sound assets.
* `_server_archive/`: **(Archive)** This folder contains the code for a previous client-server version of the game, which included a Flask API (`server.py`) for an online leaderboard. This code is not used by the final application but is kept for educational and reference purposes.

## Assets

The visual and audio assets used in this project are the classic, well-known assets from the original Flappy Bird game.