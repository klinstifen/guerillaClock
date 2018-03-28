# rpi.gorillabus
RaspberryPi powered LED matrix that provides local bust stop information.
## Description
Using the [rpi-rgb-led-matrix repo](https://github.com/hzeller/rpi-rgb-led-matrix) and the [NYC MTA Bus Time API](http://bustime.mta.info/wiki/Developers/Index) this project displays bus route information for a desired stop.
## Scripts
**gettime.py**: Scrape the NYC MTA Bus Time API and gather information about designated bus stop.
**scrollRouteUpdate.py**: Display scraped data on LED matrix.
## Parts
* Raspberry Pi
* 16x32 RGB LED Matrix
* Medium 6V 2W Solar panel
