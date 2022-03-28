from pandas.io.formats.format import CategoricalFormatter
import tripgo_parser as tgp
import pandas as pd
import json

vista_dataset = pd.read_csv('../API-Input-Combined-good.csv') #read input file
results = {}                                    #set up a dict for results return storage
results['trip_id']={}                           #for later tracking and checking 
results['travel_time']={}                            #main output 
results['mode']={}                              #in case the output (later in the spiral) will be mode specific
results['startime']={}                          #include start time of the actual trips as travel_time is depending on this
results['travdate']={}                         #similar to startime, day/dates will also impact on travel_time


for i in range(len(vista_dataset)):
    # for i in range(len(vista_dataset)):             #i = row number -2
    key = '-'    #tripgo API key
    olt = vista_dataset.orig_lat[i]             #All parameters should be strings
    oln = vista_dataset.orig_lon[i]    
    dlt = vista_dataset.lat_alt01[i]            #ensure the list name matches the input data header(column name)
    dln = vista_dataset.lon_alt01[i]
    mpm = vista_dataset.startime[i]             #start time of the trip, counted in minutes from midnight                  
    dot = vista_dataset.travdate[i]             #in the format of dd/mm/yyyy
    tripid = vista_dataset.tripid[i] 

    results['trip_id'][i]=vista_dataset.tripid[i]                   #ensure output can be referenced easily 
    results['mode'][i]=vista_dataset.travel_mode[i]
    results['startime'][i]=vista_dataset.startime[i]
    results['travdate'][i]=vista_dataset.travdate[i]

    print(i)
    print(vista_dataset.tripid[i])
    print(vista_dataset.travel_mode[i])
    if olt == dlt and oln == dln :                                  #checking in case of origin = destination                             
        results['travel_time'][i]= 0                                #if so, skip the tripgo API query, input travel time = 0
    elif vista_dataset.travel_mode[i]== 'Cycling':                                                                   #otherwise query from tripgo
        data = tgp.get.Response(key, olt, oln, dlt, dln, mpm, dot,tripid=tripid, modes=['cy_bic']).fetch()           #if mode = cycling, directly query cycling_traveltime this is due to allModes=True wouldn't return cycling or walking time
        parsedData = tgp.parse.Parse(data).getCompiledData()                                                         #compile the returned data from API into form that we want
        print('Biking')
        print(parsedData)
        results['travel_time'][i]=parsedData['cycling_travelTime']/60                                                #travel time will be in minutes
    elif vista_dataset.travel_mode[i]== 'Walking':                                                                   #if mode = walking, directly query walking_traveltime 
        data = tgp.get.Response(key, olt, oln, dlt, dln, mpm, dot,tripid=tripid, modes=['wa_wal']).fetch()           
        parsedData = tgp.parse.Parse(data).getCompiledData()                                                   
        print('Walking')
        print(parsedData)
        results['travel_time'][i]=parsedData['walking_travelTime']/60
    elif vista_dataset.travel_mode[i]== 'Driving':                                                                   #if mode = driving, directly query car_traveltime 
        data = tgp.get.Response(key, olt, oln, dlt, dln, mpm, dot,tripid=tripid, allModes=True).fetch()      
        parsedData = tgp.parse.Parse(data).getCompiledData()
        print(parsedData)
        if parsedData['car'] == 1:
            results['travel_time'][i]=parsedData['car_travelTime']/60  
            results['mode'][i]='Driving'
        elif parsedData['taxi'] == 1:                                                                        
            print('Driving --> Taxi')
            results['travel_time'][i]=parsedData['taxi_travelTime']/60
            results['mode'][i]= 'Taxi from Driving'                                                        #need to mark it to differ from pure driving
        else:
            results['travel_time'][i]=9999999999                                                
            print('Problematic coordinates')
        
    elif vista_dataset.travel_mode[i]== 'Taxi':                                                                   #if mode = taxi, directly query taxi_traveltime 
        data = tgp.get.Response(key, olt, oln, dlt, dln, mpm, dot,tripid=tripid, modes=['ps_tax']).fetch()           
        parsedData = tgp.parse.Parse(data).getCompiledData()                                                   
        print('Taxi')
        print(parsedData)
        results['travel_time'][i]=parsedData['taxi_travelTime']/60
    else:       
        data = tgp.get.Response(key, olt, oln, dlt, dln, mpm, dot,tripid=tripid, allModes=True).fetch()           
        parsedData = tgp.parse.Parse(data).getCompiledData()                                                   
        print("PT")
        print(parsedData)
        if parsedData['transit'] == 1:
            results['travel_time'][i]=parsedData['transit_totalTravelTime']/60
            results['mode'][i]='PT'
        elif parsedData['car'] == 1:                                                                        
            print('Transit --> Driving')
            results['travel_time'][i]=parsedData['car_travelTime']/60
            results['mode'][i]= 'Driving from PT'                         
        elif parsedData['taxi'] == 1:                                                                        
            print('Transit --> Taxi')
            results['travel_time'][i]=parsedData['taxi_travelTime']/60
            results['mode'][i]= 'Taxi from PT'
        else:
            print('Problematic coordinates')
            results['travel_time'][i]= 9999999999
            

df = pd.DataFrame(results)
df.to_csv('CombinedAuto_Dest01.csv',index=True)
