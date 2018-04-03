#!/usr/bin/env python
from ConfigParser import SafeConfigParser
import requests
from pprint import pprint
from datetime import datetime
import dateutil.parser
import pytz
from time import strftime
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
from guerillaClockDisplay import *
import logging

#Config logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('--%(levelname)s--%(message)s\n%(detail)s')
#file handler
fileHandler = logging.FileHandler('guerillaclock.log')
fileHandler.setFormatter(formatter)
logger.addHandler(fileHandler)
#Disable requests logging unless 'warning'
logging.getLogger("urllib3").setLevel(logging.WARNING)

logger.info('----------------')
logger.info('Begin logging...')
logger.info('----------------')

#Get config values
config = SafeConfigParser()
config.read('config.ini')
apikey = config.get('main','key')
busStop = config.get('main','stopID')

#Redefine busStop if not in config
#busStop = '504256'
url = 'http://bustime.mta.info/api/siri/stop-monitoring.json?key=' + apikey + '&MonitoringRef=' + busStop
logger.debug('Bus Stop: %s', busStop)
logger.debug('URL: %s', url)

bussesEnroute = 0 #buses en-route
GCD = guerillaClockDisplay()
logger.info('Initiating GCD...')
GCD.initiate()
nextBusInfo = {}
logger.info('Begin main loop...')
while True:
    logger.info('Retrieving bus stop info...')
    try:
        response = requests.get(url)
    except:
        logger.debug('ERROR: Could not connect to API. Retrying...')
        continue
    jsonData = response.json()
    logger.debug('Raw JSON:', extra={'detail':jsonData})
    busStopData = jsonData['Siri']['ServiceDelivery']['StopMonitoringDelivery']
    bussesEnroute = len(busStopData[0]['MonitoredStopVisit'])
    logger.info('Number of buses: %s', str(bussesEnroute))

    #Check if buses en-route
    if bussesEnroute > 0:
        logger.info('Looping through buses...')
        for bus in busStopData[0]['MonitoredStopVisit']:
            routeName = bus['MonitoredVehicleJourney']['PublishedLineName']
            busRef = bus['MonitoredVehicleJourney']['VehicleRef']
            busID = busRef.split("_") #busRef[1] = busID
            logger.debug('----- Bus %s -----', busRef)
            #Bus has passed stop or is on layover
            if 'ProgressStatus' in bus['MonitoredVehicleJourney']:
                if bus['MonitoredVehicleJourney']['ProgressStatus'].find('layover'):
                    expectedArrivalTime = bus['MonitoredVehicleJourney']['OriginAimedDepartureTime']
                    logger.debug('Bus %s Expected Arrival Time: %s',busRef, expectedArrivalTime)
                    timeTillDepart =  dateutil.parser.parse(expectedArrivalTime) - datetime.now(pytz.utc)
                    arrivalTime = str(timeTillDepart.seconds // 60 % 60) + " min."
                    logger.info('Bus %s Arrives in: %s', busRef, arrivalTime)
                    #GCD.show(routeName,arrivalTime)
                    continue
                else:
                    logger.info('Bus %s: Not en-route (%s)', busRef, bus['MonitoredVehicleJourney']['ProgressStatus'])
                    continue
            distanceAway = bus['MonitoredVehicleJourney']['MonitoredCall']['Extensions']['Distances']['PresentableDistance']
            logger.debug('Bus %s Distance Away: %s', busRef, distanceAway)
            stopsAway = str(bus['MonitoredVehicleJourney']['MonitoredCall']['Extensions']['Distances']['StopsFromCall'])
            logger.debug('Bus %s Stops Away: %s', busRef, stopsAway)
            expectedArrivalTime = bus['MonitoredVehicleJourney']['MonitoredCall'].get('ExpectedArrivalTime')
            logger.debug('Bus %s Expected Arrival Time: %s',busRef, expectedArrivalTime)
            timeTillDepart =  dateutil.parser.parse(expectedArrivalTime) - datetime.now(pytz.utc)
            arrivalTime = str(timeTillDepart.seconds // 60 % 60) + " min."

            if len(nextBusInfo):
                if arrivalTime < nextBusInfo["nArrivalTime"]:
                    nextBusInfo = {"route": routeName, "nBusId": busID, "nArrivalTime": arrivalTime}
            else:
                nextBusInfo = {"route": routeName, "nBusId": busID, "nArrivalTime": arrivalTime}

            #Reword if bus has arrived
            if distanceAway == 'at stop':
                nextBusInfo['nArrivalTime'] = 'Arrived!'

            logger.info('Bus %s Arrives in: %s', busRef, arrivalTime)
        if len(nextBusInfo):
            logger.info('!!!!!!!!!!!!!!!!')
            logger.info('Next Bus Arrives In: %s', nextBusInfo['nArrivalTime'])
            logger.info('!!!!!!!!!!!!!!!!')
            GCD.show(nextBusInfo["route"],nextBusInfo["nArrivalTime"])
        else:
            logger.info('No busses en route...')
            GCD.nobus()

    else:
        logger.info('No buses en route..')
        GCD.nobus()

    #Wait and check route again
    time.sleep(10)
    nextBusInfo.clear()
