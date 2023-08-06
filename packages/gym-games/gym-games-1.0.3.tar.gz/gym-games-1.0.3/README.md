# Gym Games

This is a gym compatible version of various games for reinforcenment learning.

For [PyGame Learning Environment](https://pygame-learning-environment.readthedocs.io/en/latest/user/games.html), the default observation is a non-visual state representation of the game. 

For [MinAtar](https://github.com/kenjyoung/MinAtar), the default observation is a visual input of the game.

## Environments

- PyGame learning environment:
  - Catcher-PLE-v0
  - FlappyBird-PLE-v0
  - Pixelcopter-PLE-v0
  - PuckWorld-PLE-v0
  - Pong-PLE-v0

- MinAtar:
  - Asterix-MinAtar-v0
  - Breakout-MinAtar-v0
  - Freeway-MinAtar-v0
  - Seaquest-MinAtar-v0
  - Space_invaders-MinAtar-v0

## Installation

### Gym

Please read the instruction [here](https://github.com/openai/gym).

### Pygame

- On OSX:

      brew install sdl sdl_ttf sdl_image sdl_mixer portmidi
      pip install pygame

- On Ubuntu:

      sudo apt-get -y install python-pygame
      pip install pygame

- Others: Please read the instruction [here](http://www.pygame.org/wiki/GettingStarted#Pygame%20Installation).

### PyGame Learning Environment

    pip install git+https://github.com/ntasfi/PyGame-Learning-Environment.git

## MinAtar

    pip install git+https://github.com/kenjyoung/MinAtar.git

### Gym-games

  - Install from source:
        
        pip install git+https://github.com/qlan3/gym-games.git

  - Install from PyPi:

        pip install gym-games

## Example

Run ``python test.py``.


## Cite

Please use this bibtex to cite this repo:

    @misc{gym-games,
    author = {Qingfeng, Lan},
    title = {Gym Compatible Games for Reinforcenment Learning},
    year = {2019},
    publisher = {GitHub},
    journal = {GitHub Repository},
    howpublished = {\url{https://github.com/qlan3/gym-games}}
    }

## References

- [gym](https://github.com/openai/gym/tree/master/)
- [gym-ple](https://github.com/lusob/gym-ple)
- [SRNN](https://github.com/VincentLiu3/SRNN)
- [MinAtar](https://github.com/kenjyoung/MinAtar)