# LOAD DATA TO TABLES

There are 3 python files in here.
1) fast_load.py
2) final_load_file.py
3) people_info_processing

## FAST LOAD TO TABLES
If you want to load the data into the tables, the fastest way would be:
1) Enter the csv files in this folder the the folloeing location in your computer:
"C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/"
2) Run the file: fast_load.py

## THE PROCESS OF LOADING THE DATA TO TABLES - FIRST TIME
**For running these files, you need to have the datasets!**
The data needed to be proccessed.
You can find in the file people_info_processing, code that goes over all of the data in two files and prepares the surface to the loading.
As a result of running this code, a file named backup_updated.txt will be generated. We will use this file in the final_load_file.py.
For convenience, the file appears in this folder as well.
By running the file final_load_file.py, all the necessary data wil be loaded into the fitting tables.
