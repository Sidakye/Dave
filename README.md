# Dave

MORE DETAILS ON [THIS](https://gainful-power-e3e.notion.site/Dave-Research-Thoughts-aa34889588f74158bcaa0400b3b4889f) NOTION PAGE

### Folder/File Info
- *app/src* -> All code besides notebooks go here
- *app/src/api/* -> All api routes go here
- *app/src/assests/* -> All images & icons for the views go here
- *app/src/models/* -> All database calls & queries go here
- *app/src/services/* -> All logic goes in this folder
- *app/src/view/* -> All front end code goes into this folder
------------------------------------
- *config/* -> Dave server setup code goes here
- *data/* -> All excel, csv, etc. files that contain data go into this folder
- *notebooks/* -> All notebooks used for training models are saved in this folder
- *saved_models/* -> All saved models that the api uses will be saved here
------------------------------------
- *requirements.txt* -> All required libraries & their versions are saved here
- *README.md* -> File with overview of Dave & other details
- *setup.py* -> Python script run to setup Dave server

------------------------------------
**NB**: For each main folder besides api & assests, code should be put into function
    specific folders.
    E.g. All database query code for gdp will go to the folder
        ***app/src/models/indicator/gdp***