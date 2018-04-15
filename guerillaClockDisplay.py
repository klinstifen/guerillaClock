#!/usr/bin/env python
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
import time

class guerillaClockDisplay(object):
    def __init__(self):
        self.options = RGBMatrixOptions()
        self.options.rows = 16
        self.options.chain_length = 1
        self.options.parallel = 1
        self.options.hardware_mapping = 'regular'  # If you have an Adafruit HAT: 'adafruit-hat'
        self.font = graphics.Font()
        self.font.LoadFont("rpi-rgb-led-matrix/fonts/5x8.bdf")
        self.textColor = graphics.Color(255, 0, 0)
    def initiate(self):
        self.matrix = RGBMatrix(options = self.options)
        self.offscreen_canvas = self.matrix.CreateFrameCanvas()

    def nobus(self):
        self.set("BUSES AT TERMINAL - STANDBY FOR NEXT BUS.")
        self.scroll()

    def set(self, m):
        self.msg = m

    def show(self, b, t):
        self.bus = b + ":"
        self.btime = t
        #self.msg = "test"

        pos = 3 #align left
        btlen = graphics.DrawText(self.offscreen_canvas, self.font, pos, 7, self.textColor, self.btime) #width of bus time
        hold = 1
        while (pos + btlen > 0):
            self.offscreen_canvas.Clear()
            blen = graphics.DrawText(self.offscreen_canvas, self.font, pos, 7, self.textColor, self.bus) #width of bus
            btlen = graphics.DrawText(self.offscreen_canvas, self.font, pos, 15, self.textColor, self.btime) #width of bus time
            pos -= 1
            if (pos + btlen < 0):
              pos = self.offscreen_canvas.width

            time.sleep(0.05)
            self.offscreen_canvas = self.matrix.SwapOnVSync(self.offscreen_canvas)
            if hold:
                time.sleep(10)
                hold = 0


    def scroll(self):
        pos = self.offscreen_canvas.width
        loops = 0
        while (loops < 2):
          self.offscreen_canvas.Clear()
          blen = graphics.DrawText(self.offscreen_canvas, self.font, pos, 10, self.textColor, self.msg)
          pos -= 1
          if (pos + blen < 0):
              pos = self.offscreen_canvas.width
              loops += 1

          time.sleep(0.05)
          self.offscreen_canvas = self.matrix.SwapOnVSync(self.offscreen_canvas)

    def off(self):
        self.offscreen_canvas.Clear()
