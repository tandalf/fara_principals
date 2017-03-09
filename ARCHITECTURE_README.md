Main Abstractions
=================
In this software certain concepts have been abstracted and they recur throught
the codebase. I will attempt to explain some of the key concepts for the 
project in this section. Listed below are some of the key concepts.

Main Page
---------
This is the first page you encounter when you visit the link 
https://www.fara.gov/quick-search.html​. This first list page is important 
enough to be architecturally significant because, it contains contextual 
information about a users session which will be necessary to navigate to
other pages. Aside holding state information about the user's session, 
the server uses this contextual data to fool scrapers which might not be
providing this context info as expected. View wise, it looks much like 
every other principal list page, but it is more important for scraping any
data at all.

The module `fara_principals.core.pages` contain the code for dealing
with principal and exhibit pages.

Principal
---------
This is the main subject for this scraper, it contains information about 
an active principals as collected from the fara's home page an example json
document structure for a principals would be:
    
    {
        "reg_number": "5945", 
        "url": "https://efile.fara.gov/pls/apex/f?p=171:200:0::NO:RP,200:
            P200_REG_NUMBER,P200_DOC_TYPE,P200_COUNTRY:5945,Exhibit%20AB,AFGHANISTAN", 
        "country": "AFGHANISTAN", "state": "", 
        "reg_date": "06/26/2009", 
        "principal_name": "Transformation and Continuity, Ajmal Ghani", 
        "address": "House #3 MRRD RoadDarul AmanKabul  ", 
        "principal_reg_date": "05/05/2014", "registrant": "Fenton Communications",

        "exhibit": [
            {
                "reg_number": "5945", "registrant": "Fenton Communications", 
                "document_type": "Exhibit AB", 
                "document_link": "http://www.fara.gov/docs/5945-Exhibit-AB-20140505-10.pdf", "date_stamped": "05/05/2014"
            }
        ]
    }

As you may have observed, it contains a nested json document for the exhibt information.
The reason for having a nested list of exhibit info is, a single principal
could have more than one exhibit document associated with it.

Partial Principal
-----------------
This is basically the same concept as a principal, but without it's exhibit info.
One major reason why this is wort it's own `concept` is, there are certain
states of the system where the exhibit information is not yet available even
though the main principal information has been collected. This is usually the
case when the main list page has been scraped for the available principal
data on it, but one more link has to be navigated to view the principal's exhibit
information. At that state, the principal is valid but not complete. An example
json document for this would be:

    {
        "reg_number": "5945", 
        "url": "https://efile.fara.gov/pls/apex/f?p=171:200:0::NO:RP,200:
            P200_REG_NUMBER,P200_DOC_TYPE,P200_COUNTRY:5945,Exhibit%20AB,AFGHANISTAN", 
        "country": "AFGHANISTAN", "state": "", 
        "reg_date": "06/26/2009", 
        "principal_name": "Transformation and Continuity, Ajmal Ghani", 
        "address": "House #3 MRRD RoadDarul AmanKabul  ", 
        "principal_reg_date": "05/05/2014", "registrant": "Fenton Communications",

        "exhibit": []
    }

when a partial principal has gotten it's exhibit info appended to it, it 
then becomes a `Full Principal` or `Principal` for short.

The module `fara_principals.core.principals` contain the code for dealing
with principals and exhibits.

High Level Scraper Logic
------------------------
The scraper has been design to use a simple to describe algorithm because
of the hidden implementation details in the core package. The simple 
(but very vague)psuedo-code explains the scraping mechanism in a high level 
of abstraction.

    for each list page of active principals:
        if page is first page:
            collect contextual/session info from page
            collect all partial_principals(without exhibit) on page
            request exhibits for partial_principals
            request next page
        else:
            collect all partial_principals(without exhibit) on page
            request exhibits for partial_principals
            request next page

        if page does not contain principals:
            raise PaginationEndedException  #stops scraper from queueing page requests