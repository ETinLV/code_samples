# code_samples
#####A few samples of the code I write



###Instructions:
#####Writen in python 2.7

Clone repo, open folder and install requirements

`pip install -r requirments.txt`


 

##Web Scraping
#####These examples show various ways to scrape a web page for information. One is done with a simple API call, one uses BeautifulSoup to scrap the DOM, and one uses Regular Expressions to scrape a .PHP file.

###weather.py 
#####Example of scraping plain html using BeautifulSoup

Returns the extended weather report for the selected location

(with optional lat and long args, otherwise defaults to Las Vegas)


`python weather.py <lat> <long>`


###hockey.py 
#####Example of scraping using an undocumented API. I found the api by inspecting the page using Dev Tools, and then used the address to make my request.


Returns the current scores for all NHL hockey games

`python hockey.py`

###gen_county.py
#####Example of scraping a .PHP file using Regular Expressions.


Returns active events from the Genessee County 911 Page

`python gen_county.py`


