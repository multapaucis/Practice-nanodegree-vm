A data analysis summary tool that Highlights the Most Popular Authors, Most Popular Articles, and days with higher error rate using data from a specific Database.

Instructions

To run this program you will need both Python and PostgreSQL installed on your machine
and the newsdata.sql data file.
The newsdata.sql file can be found at
    https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip
To load the data, while in the directory containg the SQL file use the command
    psql -d news -f newsdata.sql


To open Program in IDLE:

    Open IDLE
    Press CTRL+O (CMD+O for Macs) and select the catalog.py file from wherever it is saved on your computer.
    Press F5 to run the program
    The program will then provide a text output summarizing the data

To open the Program in Terminal:

    Open terminal
    Use CD to open the directory containing the catalog.py file
    Enter $ python catalog.py
    The program will then provide a text output summarizing the data
