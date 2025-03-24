#!/usr/bin/env python3
"""
Main entry point for the roguelike game.
This file initializes the game and contains the main game loop.
"""
from game import Game


def main():
    """
    Main function that starts the game and contains the main game loop.
    """
    # Initialize the game
    game = Game()
    
    # Start the game
    game.start()
    
    # Main game loop
    while game.running:
        game.process_input()
        game.update()
        game.render()
    
    print("Thanks for playing!")


if __name__ == "__main__":
    main()
