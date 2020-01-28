*************************
TripGo Routing API Parser
*************************

A simple parser for use with the TripGo routing API. This package should be used to
obtain trip information based on Origin-Destination pairs.

Getting Started
###############

Installation
*************
**Windows**

If using an Anaconda environment, enter the following in the Anaconda command prompt.

.. code-block:: python

    conda install pip
    pip install tripgo-parser

**Mac/Linux**

.. code-block:: python

    pip install tripgo-parser

Usage
*****
**All Modes**

Note: The TripGo routing API does not give all *possible* modes for a given O-D pair.
Instead, the API returns the trips for modes (and mode combinations) it deems reasonable.

For example:

.. code-block:: python

   import tripgo_parser as tgp

   key = 'fakekey123'               # TripGo Authentication Key
   olt = '-37.83724'
   oln = '145.201767'
   dlt = '-37.817800'
   dln = '145.018510'
   mpm = '1110'               # Minutes past midnight
   dot = '3/1/20'              # Date of travel: d/m/yy

   # Request the routing data from TripGo
   data = tgp.get.Response(key, olt, oln, dlt, dln, mpm, dot).fetch()
   parsedData = tgp.parse.Parse(data).getCompiledData()

This will return:

.. code-block:: python

    code output
    {'car': 1,                              # 1 = Information for this mode exists
     'car_calorieCost': 30,                 # TripGo calculated calorie cost
     'car_distances': {'me_car': 23851},    # Dict of distances for each mode used
     'car_fuelCost': 2.12,                  # TripGo estimated fuel cost
     'car_hassleCost': 4,                   # TripGo estimated hassle cost
     'car_modeCount': 1,                    # Number of modes used in trip
     'car_numberOfTransfers': 0,            # Number of public transport transfers
     'car_parkingCost': 0,                  # If exists, cost of parking
     'car_parkingExists': False,            # Does off-street parking exist?
     'car_travelTime': 1816,                # Total travel time
     'car_tripModes': {0: 'me_car'},        # Dict of ordered modes used
     'car_walkingDistance': 0,              # If exists, walking distance within trip
     'car_weightedScore': 44.1,             # Tripgo calculated weighted score (ranking)
     'cycling': 1,
     'cycling_Calorie Cost': 375,
     'cycling_distances': {'cy_bic': 20002},
     'cycling_hassleCost': 8.7,
     'cycling_modes': 'cy_bic',
     'cycling_travelTime': 4175,
     'cycling_weightedScore': 106.8,
     'startime': '',
     'taxi': 1,
     'taxi_hassleCost': 2,
     'taxi_numberOfTransfers': 0,
     'taxi_travelTime': 2205,
     'taxi_waitTime': 0,
     'taxi_walkingDistance': 0,
     'taxi_weightedScore': 69.3,
     'transit': 1,
     'transit_allModes': {0: 'me_car',
                      1: 'stationary_parking-onstreet',
                      2: 'stationary_transfer',
                      3: 'pt_pub_train',
                      4: 'wa_wal'},
     'transit_distances': {'me_car': 3828,
                       'pt_pub_train': 0,
                       'stationary_parking-onstreet': 0,
                       'stationary_transfer': 0,
                       'wa_wal': 999},
     'transit_end': {'pt_pub_train': {'Hawthorn Railway Station': 1609661820}},
     'transit_hassleCost': 6,
     'transit_mainMode': 'pt_pub_train',
     'transit_modes': ['me_car',
                   'stationary_parking-onstreet',
                   'stationary_transfer',
                   'pt_pub_train',
                   'wa_wal'],
     'transit_numberOfTransfers': 0,
     'transit_start': {'pt_pub_train': {'Heatherdale Railway Station': 1609660080}},
     'transit_timeOnEachMode': {'me_car': 289,
                            'pt_pub_train': 1740,
                            'stationary_parking-onstreet': 240,
                            'stationary_transfer': 180,
                            'wa_wal': 872},
     'transit_timeOnMainMode': 1740,
     'transit_timeOnOtherModes': 1581,
     'transit_totalTravelTime': 3339,
     'transit_waitTime': 0,
     'transit_weightedScore': 50.7,
     'walking': 0}

For a large OD datasets, it is recommended to save the JSON data. The 'save' function takes one required parameter
and one optional parameter. These are respectively:

- Destination Folder ('myFolder') - written in the current working directory
- Unique ID (..,unique_id='myuniqueid') - name of file

This can be done using the TripGo Parser as follows:

.. code-block:: python

    data = tgp.get.Response(key, olt, oln, dlt, dln, mpm, dot).save('MyFolder', unique_id='trip1')

And the resulting file will be saved as ../MyFolder/trip1.json.
This file can then be parsed using the following:

.. code-block:: python

    import json

    with open('MyFolder/trip1.json') as file:
        data = json.loads(file.read())

    parsedData = tgp.parse.Parse(data)

This will yield the same result as the above example.

**Specific Modes**

Specific modes can be specified to be used with the API. Please note that if multiple modes are listed,
the trip will be classified as the dominant mode. For example:

.. code-block:: python

    modes = ['me_car', 'pt_pub']
    data = tgp.get.Response(key, olt, oln, dlt, dln, mpm, dot, modes=modes).save('MyFolder', unique_id='trip2')


**VISTA Dataset**

For use with the VISTA dataset, significant area (SA1) values must be converted to coordinates
using their centroids. Using these coordinates labelled (e.g. 'origlat' for latitude origin coordinate)
and the associated trip ID and start time (minutes past midnight) we are able to use the TripGo routing
API to obtain trip attributes.

.. code-block:: python

    import pandas as pd
    import json

    vista_dataset = pd.read_csv('vista.csv')

    i = 0
    key = 'fakekey123'
    olt = vista_dataset.origlat[i]              # All parameters should be strings
    oln = vista_dataset.origlon[i]
    dlt = vista_dataset.destlat[i]
    dln = vista_dataset.destlon[i]
    startime = vista_dataset.startime[i]        # For example: '1020'
    travdate = vista_dataset.travdate[i]
    modes = ['pt_pub']

    tripid = vista_dataset.tripid[i]            # For example: 'Y14H1050101P01T02'

    data = tgp.get.Response(key, olt, oln, dlt, dln, mpm, dot, tripid=tripid, modes=modes).save('VISTA_trips')


This will result in the file being saved as:

../VISTA_trips/Y14H1050101P01T02-1020.json
