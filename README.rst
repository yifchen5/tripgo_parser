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
   import numpy as np

   key = 'fakekey123'               # TripGo Authentication Key
   olt = '-37.83724'
   oln = '145.201767'
   dlt = '-37.817800'
   dln = '145.018510'
   mpm = '1110'               # Minutes past midnight
   dot = '3/1/20'              # Date of travel: d/m/yy
   modes = ['pt_pub']               # TripGo API format for modes

   # Request the routing data from TripGo
   data = tgp.get.Response(key, olt, oln, dlt, dln, mpm, dot, modes).fetch()
   parsedData = tgp.parse.Parse(data)

This will return:

.. code-block:: python

    code output

For a large OD datasets, it is recommended to save the JSON data. This can be done using the TripGo Parser as follows:

.. code-block:: python

    saved data

Here the files will be saved in the current working directory, and can be parsed using the following:

.. code-block:: python

    this is how you parse



**Single Modes**



**VISTA Dataset**





