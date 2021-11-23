# Importing the library
import pygame
import pandas as pd
import math

# Initializing Pygame
pygame.init()

class CandleSticks:
    def __init__(self, candlesticks, points = 100) -> None:

        self.chart_height = 780

        # Initializing surface
        self.surface = pygame.display.set_mode((1500, self.chart_height))

        # Initialing Colours
        self.colour_red = (255,0,0)
        self.colour_lime_green = (46,244,41)
        self.colour_light_gray = (211, 211, 211)

        self.x_offset = 10
        self.y_padding = 10

        self.points = points

        self.max_price = candlesticks.max().high
        self.min_price = candlesticks.min().low

        self.max_points = (self.max_price - self.min_price) * points

        self.candlesticks = candlesticks

    def create_candle(self, index):
        colour = self.colour_light_gray

        candlestick = self.candlesticks.iloc[index]

        top_wick_pos = self.to_relative_pos(candlestick.high)
        top_body_pos = self.to_relative_pos(max(candlestick.open, candlestick.close))

        bottom_body_pos = self.to_relative_pos(min(candlestick.open, candlestick.close))
        bottom_wick_pos = self.to_relative_pos(candlestick.low)

        # Drawing Candle
        pygame.draw.line(self.surface, colour, pygame.Vector2(self.x_offset, self.y_padding + top_body_pos), pygame.Vector2(self.x_offset, self.y_padding + bottom_body_pos), 1)
        pygame.draw.line(self.surface, colour, pygame.Vector2(self.x_offset + 1, self.y_padding + top_wick_pos), pygame.Vector2(self.x_offset + 1, self.y_padding + bottom_wick_pos), 1)
        pygame.draw.line(self.surface, colour, pygame.Vector2(self.x_offset + 2, self.y_padding + top_body_pos), pygame.Vector2(self.x_offset + 2, self.y_padding + bottom_body_pos), 1)

        self.x_offset += 5

    def render(self, length=280):
        index_offset = 0

        if length == 0 or self.candlesticks.shape[0] < length:
            length = self.candlesticks.shape[0]
        elif length < self.candlesticks.shape[0]:
            index_offset = self.candlesticks.shape[0] - length
            length = self.candlesticks.shape[0]

        for i in range(index_offset, length):
            self.create_candle(i)

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

    def to_relative_pos(self, value):
        value_percentage = ((self.max_price - value) * self.points) / self.max_points * 100

        return int(math.floor(value_percentage / 100 * (self.chart_height - self.y_padding)))

    def to_points(self, value):
        return value * self.points
