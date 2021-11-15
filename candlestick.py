import math
import pandas as pd

from tkinter import *


width = 1_200
height = 700

x_margin = 10

class Candlestick:
    def __init__(self, candlesticks, points=10, height=700) -> None:
        self.win = Tk()
        self.win.title('Candlesticks')
        self.win.geometry('1280x768+10+10')
        self.win.config(bg='#345')

        self.canvas = Canvas(self.win, width=width, height=height, bg= "black")

        candle_max_height = candlesticks.high.max()
        candles_min_height = candlesticks.low.min()

        self.x_margin = 10
        self.max_points = math.floor((candle_max_height - candles_min_height) * points)
        self.chart_height = height

        self.candlesticks = candlesticks

    def create_rectangle(self, left_margin, top_margin, right_margin, bottom_margin, fill='gray'):
        self.canvas.create_rectangle(left_margin, top_margin, right_margin, bottom_margin, fill=fill, outline="")

    def create_candle(self):
        self.create_rectangle(left_margin=self.x_margin+2, top_margin=10, right_margin=self.x_margin+4, bottom_margin=80)
        self.create_rectangle(left_margin=self.x_margin, top_margin=30, right_margin=self.x_margin+6, bottom_margin=60)
        self.create_rectangle(left_margin=self.x_margin+2, top_margin=10, right_margin=self.x_margin+4, bottom_margin=80)
        
        self.x_margin += 8

    def to_relative_value(self, value):
        value_percentage = value / self.max_points * 100

        return int(math.floor(value_percentage / 100 * self.chart_height))

    def render_chart(self, length=0):

        if length == 0 or self.candlesticks.size < length:
            length = self.candlesticks.size
        
        for i in range(length):
            self.create_candle()

        self.canvas.pack()
        self.win.mainloop()
