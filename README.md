EuskalSense (Formerly BizkaiSense)
==================================

Bizkaisense is an effort on the publication of enviromental Open Data from Basque Country as Linked Open Data. In this project we scrap, store, semantize and visualize air  and drinking water quality measures.

At this moment the scripts scrap information from more than 70 air quality stations, more than 800 water sources and generate more than 9,000,000 observations.

This repository includes the scripts, the Django website in which we visualize the data, and the D2R script that makes the conversion from SQL to RDF.

In the first steps of the project we built some scripts that generate directly RDF data. These data was stored in a RDF store, and the Django website was entirely based on SPARQL queries over that RDF store. 
The performance of the website wasn't acceptable, as the response time of the RDF store to complex SPARQL queries was too high, due to the high volume of stored data.
So we decided to modify the project and build it on top of a traditional SQL database. The RDF data is now generated with D2R (http://d2rq.org/d2r-server), and the mapping file is included on the repository.
In a last update of the project we have improved the performance of the data generation scripts using Hadoop. We have developed some Pig scripts that make the same work as those in Python, but based on distributed computing, decreasing notably the data generation time.

Data included in this repository:

Scripts that get air and drinking water quality measures of Basque Country from Open Data Euskadi (ODE):
- The folder sql_generators/pig contains the Pig script that gets measures from ODE using Hadoop, and stores them in a SQL database.
- The folder sql_generators contains the Python scripts that get measures from ODE and store them in a SQL database.
- The folder rdf_generators contains the Python scripts that get measures from ODE and create RDF triples based on SSN ontology.

Django websites:
- The folder bizkaisense_sql contains the SQL-based website.
- The folder bizkaisense_sparql contains the SPARQL-based website (low performance with high volume of data).

D2R mapping:
- The "bizkaisense_sql/bizkaisense.ttl" file contains the mapping used for the conversion from SQL to RDF.

Slides:
- The slides folder contains a presentation explaining the details of the project (spanish).
