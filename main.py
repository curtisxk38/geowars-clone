import pygame
import os
import sys
import control
import game
import menu
import scores
import instructions

def main():
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.init()
    pygame.mixer.init()

    SCREEN_SIZE = (720, 480)
    DESIRED_FPS = 60.0

    pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("Geowars Clone")

    state_dict = {"menu": menu.MenuState(),
                  "game": game.GameState(),
                  "scores": scores.ScoresState(),
                  "instructions": instructions.InstructionsState()
                  }

    game_control = control.Control(1000.0 / DESIRED_FPS)
    game_control.setup_states(state_dict, "menu")
    game_control.main()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
