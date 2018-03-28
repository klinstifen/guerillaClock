#!/usr/bin/env python
import time
from datetime import datetime
import sys
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics

#Test the various display settings and arrange output

# Configuration for the matrix
options = RGBMatrixOptions()
options.rows = 16
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = 'regular'  # If you have an Adafruit HAT: 'adafruit-hat'

matrix = RGBMatrix(options = options)

offscreen_canvas = matrix.CreateFrameCanvas()
font = graphics.Font()
font.LoadFont("../../fonts/5x8.bdf")
textColor = graphics.Color(255, 0, 0)
pos = offscreen_canvas.width
my_text = "6498:"
my_text2 = "1 min"
waitTime = 0
#while waitTime < 30:
pos = 4
hold = 1
wlen = graphics.DrawText(offscreen_canvas, font, pos, 7, textColor, my_text)
startime = datetime.now()
print "time before loop: " + str(startime)
while (pos + wlen > 0):
    offscreen_canvas.Clear()
    #print pos
    wlen = graphics.DrawText(offscreen_canvas, font, pos, 7, textColor, my_text)
    wlen2 = graphics.DrawText(offscreen_canvas, font, pos, 15, textColor, my_text2)
    pos -= 1
    if (pos + wlen < 0):
      pos = offscreen_canvas.width

    time.sleep(0.05)
    offscreen_canvas = matrix.SwapOnVSync(offscreen_canvas)
    if hold:
        time.sleep(10)
        hold = 0

    curtime = datetime.now()
    while (curtime - startime).seconds < 30:
        curtime = datetime.now()
        print "time in loop: " + str(curtime)
        print "time diff: " + str((curtime - startime).seconds)
    print "30 seconds past"
