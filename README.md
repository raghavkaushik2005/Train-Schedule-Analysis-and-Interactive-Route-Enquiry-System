\# # Train Schedule Analysis and Interactive Route Enquiry System



\## Project Overview



The Train Schedule Analysis and Interactive Route Enquiry System is an interactive web application developed as the final capstone project of the Sysslan IT Solutions internship.



The system allows users to search for available trains between two stations and view:



\- Train number

\- Source station

\- Departure time

\- Destination station

\- Arrival time

\- Estimated journey duration



The application uses the provided train schedule dataset and determines valid train routes based on the actual station sequence.



\---



\## Project Objectives



The main objectives of this project are:



\- Allow users to search for trains between two stations.

\- Display all available direct trains for the selected route.

\- Verify the direction of travel using station sequence.

\- Calculate the estimated journey duration.

\- Provide a simple and user-friendly web interface.

\- Store and retrieve train schedule data using MySQL.



\---



\## Technologies Used



\### Backend

\- Python

\- Flask

\- MySQL

\- MySQL Connector/Python



\### Frontend

\- HTML

\- CSS

\- JavaScript



\### Data Processing

\- Pandas



\### Development Tools

\- Visual Studio Code

\- MySQL

\- Git and GitHub



\---



\## Dataset



The application uses the train schedule dataset provided for the internship project.



Dataset details:



\- Records: 186,074

\- Attributes: 12

\- Unique trains: 11,113



The dataset contains information such as:



\- Train number

\- Station name

\- Station code

\- Station sequence

\- Arrival time

\- Departure time

\- Distance

\- Class availability



The original dataset is kept unchanged. A separate working copy was used for the application.



\---



\## System Workflow



```text

Train Schedule Dataset

&#x20;       ↓

&#x20;     MySQL

&#x20;       ↓

&#x20;  Flask Backend

&#x20;       ↓

Route Search Request

&#x20;       ↓

Station Sequence Verification

&#x20;       ↓

Train \& Journey Information

&#x20;       ↓

HTML/CSS Results Page

