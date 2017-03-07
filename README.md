# About Fara Principles
This project is a web scraper which collects Foreign Principles from the website [fara.gov](https://www.fara.gov/quick-search.html).
Although, the core components of the software are still under construction, most of the trick the site uses to evade scrapers has
been discovered and is abstracted in the core package. Work being done on the core are usually implemented on the `core` branch.

#Installation
To work with this package, you need to install certain requirements which are specified in the `requirements.txt` file. To install
the requirements, make sure you have python2 and optionally a virtual environment setup. After those, on your terminal enter:

    pip install -r requirements.txt
    
#Running tests
Good test coverage is encouraged for this code base. To run the tests and coverage for the core components, while at the base
directory, enter the following commands:
 
    coverage run --source=fara_principals.core -m unittest discover tests/unit
    coverage report -m
