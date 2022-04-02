========================
Form Generation
========================
Data needs to be accessible without requiring in-depth knowledge 
of a query language
or specialized software. New forms should be easily created with a 
shallow learning curve.  

System Requirements:
    -   "No-code" data access 
    -   Upload and export data via CSV 
    -   Redcap integration 
    -   database backend agnostic 
    -   built-in workflow management and automation

Microsoft Access
-----------------
MS Access provides a full solution for data storage and access. 
It is included at no additional cost with the Office 365 suite, and 
can be very powerful when combined with other Microsoft tools.
It has another advantage of already being implemented and functional.

One major drawback of relying on MS Access is the proprietary .accdb 
format. Databases like mySQL, PostgreSQL, MariaDB, MongoDB, etc. provide 
APIs for nearly every programming language, have a large community for 
support, and come with greater control over data management and distribution.
Using an open-source data format means more choices in how you consume 
it. 

MongoDB integration 
    If working in a noSQL document-based data model, it may be useful 
    to convert or connect the existing MS Access database with 
    a document database such as MongoDB. Drivers exist 
    for some of these databases, that aid in this conversion.

    More
        https://www.progress.com/odbc/mongodb

Advantages: 
    -   Free with MS Office 365 Suite 
    -   Already implemented and working 

Disadvantages:
    -   Proprietary data format (.accdb and .mdb)
    -   Not Python friendly
    -   Unpopular user interface 
    -   Limited 3rd party integrations 
    -   Not very intuitive (learning curve too high)

Budibase
----------
Budibase offers an intuitive web gui for viewing this data store 
and creating documents and forms from it. Similar to Airtable or 
the MS Access frontend, only it can be self-hosted on the pre-existing  
Kubernetes cluster and is fully customizable. Because they offer 
their own hosting solution, and already have a revenue model, there 
is good chance that the self-hosted solution will remain free and 
open-source. 

By storing our data in MongoDB or PostgreSQL, rather than MS Access 
proprietary .accdb or .mdb format, we make it available and easily 
consumable by all of our services, including direct calls by  
python and matlab scripting.

-   Connects to existing database (PostgreSQL, Mongo, etc.)
-   Allows easy graphical manipulation and addition of data via 
    web interface and user-built apps
  
Advantages over MS Access or Airtable:
    -   Free 
    -   HIPAA compliant
        -   Airtable uses a cloud platform that does not meet the criteria for HIPAA compliance, 
         so can't be used to host PHI.
        -   Self-hosted- complete control over security methods
    -   Small learning curve 
    -   Distributed storage (sharding): the ability to break up the database in to chunks, or "shards" 
        accross multiple cluster nodes for load balancing requests 
    -   Intuitive automation pipeline creation interface 
        -   Easily create workflows and notification systems within 
        the user web interface. No code required. 
    -   Upload of data via CSV
    -   Combine tables and export them as CSV or JSON
    -   Ultimate data control: hosting, format, presentation 
    -   Backend agnostic, independent to underlying DB
    -   Data is stored in a non-proprietary format and located outside of Budibase
        -   can be accessed by any other service or script. 
    -   Data is controlled by a single source, but can 
        exist in multiple places.
    -   Replication: the ability to seamlessly sync data to multiple sources, as if it were one 
        -   Minimizes outages by offering more than one server for access. 
        -   If one goes out, the others keep data access live 
    -   Web-based access 
        -   Don't need to be on site to create forms 

Drawbacks:
-   No built-in audit trailing, but there are potential workarounds 
for implementing that..
-   Mature, but not as industry standard as MS Access or SQL. The 
learning curve should be low 

Redcap  
--------
Redcap specializes in making forms, collecting e-signatures, and 
maintaining HIPAA compliance. It is managed by the institute, 
so it is a zero-overhead solution that for the most part, just works. 
It's advantages also include built-in audit trailiing, integration 
with SPSS, SAS, and R, and confidence that it will always cater to 
the needs of research and healthcare.

It however lacks many of the workflow management features offered by 
other data access clients like Airtable, Budibase, or MS Access, so 
the most robust solution will require a cohesive marriage between 
RedCap and whichever other data client is employed. 

Integration
    Data from RedCap can be automatically exported as JSON or CSV using 
    the RedCap API and cron scheduling, or event triggers. The same 
    program can utilize the API provided by the database solution 
    (i.e. MongoDB, PostgreSQL, etc.) to store those values into the 
    central database. Once the data generated by RedCap are replicated 
    into the primary database, a Budibase automation will update the 
    appropriate tables with the added data. This could be automated 
    with the same service orchestrator the other services on the 
    cluster use.

AirTable
--------
Airtable is a very popular solution to data workflow management and 
form creation, but has no free/self-hosted option, and the cloud 
services do not satisfy HIPAA compliance guidelines, so cannot be 
used for the storage of PHI.

