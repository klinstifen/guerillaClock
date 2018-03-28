# gorillaClock
GorillaClock, a low cost countdown clock, provides bus arrival time by way of 16x32 RBG matrix backed by a Raspberry Pi Zero W.

It is a $100 solution to a $25,000 problem.
## Description
The project utilizes a custom designed 3D printed enclosure to house a 16x32 RGB matrix and costs approximately $100.  (The price could be reduced if a smaller lipo was used, or omitted entirely.)

The Raspberry Pi Zero W connects to a local wifi network and pulls bus arrival time and route details from the [NYC MTA Bus Time API](http://bustime.mta.info/wiki/Developers/Index).  The 16x32 matrix displays the "next" bus' arrival time, for a selected bus stop.

The display is controlled with hzeller's great [rpi-rgb-led-matrix repo](https://github.com/hzeller/rpi-rgb-led-matrix) project.  The [wiring.md](https://github.com/hzeller/rpi-rgb-led-matrix/blob/master/wiring.md) was especially helpful in creating a Pi HAT, utilizing the [Adafruit Perma Proto Bonnet](https://www.adafruit.com/product/3203).

## Scripts
**gorillaClock.py**: Scrape the NYC MTA Bus Time API and gather information about a designated bus stop.
**gorillaClockDisplay.py**: Display and scroll arrival time information on a 16x32 RGB matrix.
## Parts
* 1	×	[16x32 RGB LED Matrix](https://www.adafruit.com/product/420) - $24.95
* 1	×	[Raspberry Pi Zero W](https://www.adafruit.com/product/3400) - $10
* 1	×	[Adafruit Perma Proto Bonnet Mini](https://www.adafruit.com/product/3203) - $4.50
* 1	×	4GB Micro SD Card (https://www.amazon.com/Sandisk-MicroSDHC-Memory-Card-Adapter/dp/B000SMVQK8) - $9.71
* 1	×	PowerBoost 1000C (https://www.adafruit.com/product/2465) - $19.95
* 1	×	Lithium Ion Battery - 3.7V 6600mAh (https://www.adafruit.com/product/353) - $29.50
* 1	×	Rocker Switch SPST 2Pin (http://tinkersphere.com/buttons-switches/1039-rocker-switch-spst-2-pin.html) - $1.49
* 1	×	Various Srews: M2.5 and M4
