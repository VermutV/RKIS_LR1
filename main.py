#!/usr/bin/env python3
from game import Game


def main():
    # Запуск
    game = Game()
    
    # Старт
    game.start()
    while game.running:
        game.process_input()
        game.update()
        game.render()
    
    print("Спасибо за тест!")


if __name__ == "__main__":
    main()
