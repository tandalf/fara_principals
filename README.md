# About Fara Principles
This project is a web scraper which collects Foreign Principles from the website [fara.gov](https://www.fara.gov/quick-search.html).Most of the trick the site uses to evade scrapers has been discovered and is abstracted in the core package. Work being done on the core are usually implemented on the `core` branch. There is also the `scraper` branch where work on the scraper has be done.

#Installation
It is considered very good practice to setup a virtual environment before installing apps like this so, please do that. This project is targeted for python2 so please make sure at least python 2.7 is installed on your system.
You can download or clone this repo to install the scraper. At your terminal, enter the following commands. You can litrarily copy and paste this commands at your terminal to get this working.
    
    git clone https://github.com/tandalf/fara_principals.git
    cd fara_principals
    python setup.py install
    pip install -r requirements.txt
    
This install the scraper and it's dependencies.

#Scraping Active Principals
After the installation has completed successfull, you can start collecting principal data by running the command below while in
the project's directory.

    scrapy crawl active_principals -o outputfile.json
    
where outputfile.json is the path to the file which the principal json lines will be stored.
    
#Running tests
Good test coverage is encouraged for this code base. To run the tests and coverage for the core components, while at the base
directory, enter the following commands:
 
    coverage run --source=fara_principals.core -m unittest discover tests/unit
    coverage report -m
