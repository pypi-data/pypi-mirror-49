# MVG command line commute monitor  

very simple cli based commute monitor returning a specified number of 
departures for a given station.

## Installation
```pip install mvg-cli-departures```

## Usage
 - either use *Request* module by importing 
 `from mvg_monitor.monitor import Request`
 - or as intended via cli by `mvg-depart START -n 4` for the 
    next 4 departures from *START*
    - e.g. `mvg-depart Universitaet -n 4` for the 4 upcoming departures from station 
    *Univeristaet*

## Up next
- provide route options for start and destination
- find station to provided input 
- provided additional commute related information like delays, errors etc.
- actual monitor function to watch commutes for a given route 

## Repository:
https://gitlab.com/maternusherold/mvg-command-line-departure-monitor