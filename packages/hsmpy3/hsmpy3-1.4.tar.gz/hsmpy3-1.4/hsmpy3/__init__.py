# Developed By Mahdi Rajabi mrajabi@clemson.edu
import arcpy
from hsmpy3 import fields_IL
from hsmpy3 import common
from hsmpy3 import crash
from hsmpy3 import network
from hsmpy3 import il
from hsmpy3 import nm
from hsmpy3 import fars

#import hsmpy3.fields_SC as fields_SC
#import hsmpy3.fields_IL as fields_IL
#import hsmpy3.common as common
#import hsmpy3.crash as crash
#import hsmpy3.db as db
#import hsmpy3.args as args
#import hsmpy3.network as network
#import hsmpy3.precrash as precrash
#import hsmpy3.il as il



"""
This package provides tools for highway safety analysis
This package is developed for South Carolina data 
but many of the tools can be used for other states by minor adjustments  
The whole process of this package can be divided into following major steps:

1. Importing and formating the raw data into individual geodatabase files
2. Integrating the individual databases to a single master dataset with creating all relationships

Each major step can be divided into several smaller steps:

1.1. Import Digital Elevation Model (DEM)
1.1. Create Routes
1.2. Import Railroads
1.3. Import Bridges
1.4. Create Intersections
1.5. Geocode Location Files
1.6. Import Location Files
1.7. Import Unit Files
1.8. Import Occ Files  

2.1. Create Database
2.2. Add Domains
2.3. Add Tables
2.4. Assign Domains to fields
2.5. Create Rlationships
2.6. Add Representations
"""