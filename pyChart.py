# Importing the library
import pygame
import pandas as pd
import math

# Initializing Pygame
pygame.init()

class ema_period:
    fast = 8
    slow = 17

class macd_colour:
    neutral = (211, 211, 211),
    lime_green = (46,244,41),
    green = (34,139,34),
    red = (255,0,0),
    firebrick = (178,34,34)

class CandleSticks:
    def __init__(self, candlesticks, points = 100, is_render = False) -> None:
        self.chart_height = 780

        # Initializing surface
        self.surface = pygame.display.set_mode((1500, self.chart_height))

        self.x_offset = 10

        self.points = points

        self.max_price = candlesticks.max().high
        self.min_price = candlesticks.min().low

        self.max_points = (self.max_price - self.min_price) * points

        self.candlesticks = candlesticks

        # convert time in seconds into the datetime format
        self.candlesticks['time'] = pd.to_datetime(candlesticks['time'], unit='s')

        self.candlesticks[['fast', 'slow']] = 0.0

        self.candlesticks = self.calc_ema(self.candlesticks, ema_period.fast, 'fast')
        self.candlesticks = self.calc_ema(self.candlesticks, ema_period.slow, 'slow')

        if is_render:
            self.render()

    def create_candle(self, index, colour):
        candlestick = self.candlesticks.iloc[index]

        top_wick_pos = self.to_relative_pos(candlestick.high)
        top_body_pos = self.to_relative_pos(max(candlestick.open, candlestick.close))

        bottom_body_pos = self.to_relative_pos(min(candlestick.open, candlestick.close))
        bottom_wick_pos = self.to_relative_pos(candlestick.low)

        # Drawing Candle
        pygame.draw.line(self.surface, colour, pygame.Vector2(self.x_offset, top_body_pos), pygame.Vector2(self.x_offset, bottom_body_pos), 1)
        pygame.draw.line(self.surface, colour, pygame.Vector2(self.x_offset + 1, top_wick_pos), pygame.Vector2(self.x_offset + 1, bottom_wick_pos), 1)
        pygame.draw.line(self.surface, colour, pygame.Vector2(self.x_offset + 2, top_body_pos), pygame.Vector2(self.x_offset + 2, bottom_body_pos), 1)

        self.x_offset += 5

    def render(self, length=280):
        index_offset = 1

        if length == 0 or self.candlesticks.shape[0] < length:
            length = self.candlesticks.shape[0]
        elif length < self.candlesticks.shape[0]:
            index_offset = self.candlesticks.shape[0] - length
            length = self.candlesticks.shape[0]

        for i in range(index_offset, length):
            prev_macd = self.calculate_macd(self.candlesticks.iloc[i-1].fast, self.candlesticks.iloc[i-1].slow)
            curr_macd = self.calculate_macd(self.candlesticks.iloc[i].fast, self.candlesticks.iloc[i].slow)

            self.create_candle(i, colour=self.get_renko_colour(prev_macd, curr_macd))

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

        return int(math.floor(value_percentage / 100 * self.chart_height))

    def calc_ema(self, df, period, col_name):
        prev_value = df.iloc[0]['close']
        def func2(row):
            # non local variable ==> will use pre_value from the new_fun function
            nonlocal prev_value
            prev_value = prev_value + (2.0 / (1.0 + period)) * (row['close'] - prev_value)
            return prev_value
        # This line might throw a SettingWithCopyWarning warning
        df.iloc[1:][col_name] = df.iloc[1:].apply(func2, axis=1)
        return df

    def calculate_macd(self, fast_ema, slow_ema):
        return fast_ema - slow_ema

    def get_renko_colour(self, prev_macd, curr_macd):
        if curr_macd > 0:
            if curr_macd > prev_macd:
                return macd_colour.lime_green
            elif curr_macd < prev_macd:
                return macd_colour.green
        elif curr_macd < 0:
            if curr_macd < prev_macd:
                return macd_colour.red
            elif curr_macd > prev_macd:
                return macd_colour.firebrick

        return macd_colour.neutral

