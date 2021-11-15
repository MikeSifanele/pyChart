# Importing the library
import pygame
import pandas as pd

# Initializing Pygame
pygame.init()

class CandleSticks:
    def __init__(self, candlesticks) -> None:
        # Initializing surface
        self.surface = pygame.display.set_mode((1200,700))

        # Initialing Colours
        self.colour_red = (255,0,0)
        self.colour_lime_green = (46,244,41)
        self.colour_light_gray = (211, 211, 211)

        self.x_offset = 10

        self.candlesticks = candlesticks

    def create_candle(self):
        colour = self.colour_light_gray

        top_body_pos = 30
        top_wick_pos = 10

        bottom_body_pos = 60
        bottom_wick_pos = 90


        # Drawing Candle
        pygame.draw.line(self.surface, colour, pygame.Vector2(self.x_offset, top_body_pos), pygame.Vector2(self.x_offset, bottom_body_pos), 1)
        pygame.draw.line(self.surface, colour, pygame.Vector2(self.x_offset + 1, top_body_pos), pygame.Vector2(self.x_offset + 1, bottom_body_pos), 1)

        pygame.draw.line(self.surface, colour, pygame.Vector2(self.x_offset + 2, top_wick_pos), pygame.Vector2(self.x_offset + 2, bottom_wick_pos), 1)

        pygame.draw.line(self.surface, colour, pygame.Vector2(self.x_offset + 3, top_body_pos), pygame.Vector2(self.x_offset + 3, bottom_body_pos), 1)
        pygame.draw.line(self.surface, colour, pygame.Vector2(self.x_offset + 4, top_body_pos), pygame.Vector2(self.x_offset + 4, bottom_body_pos), 1)

        self.x_offset += 8

    def render(self, length=0):

        if length == 0 or self.candlesticks.shape[0] < length:
            length = self.candlesticks.shape[0]

        for i in range(length):
            self.create_candle()

        pygame.display.flip()

        self.stop_rendering = False

        while not self.stop_rendering:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.stop_rendering = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        print('Pressed Up')
                    elif event.key == pygame.K_DOWN:
                        print('Presed Down')
                    elif event.key == pygame.K_LEFT:
                        print('Closing.')
                        self.close()
    
    def close(self):
        self.stop_rendering = True
