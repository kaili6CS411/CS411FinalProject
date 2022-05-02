# CS411FinalProject
Title: AcademicWorld Analysis

Purpose: Provide analytic data for users who are interested in knowing about the academic world databases. Users are primarily students who are interested in researching, like graduate students. They can find useful information for their research

Demo: https://mediaspace.illinois.edu/media/t/1_ig1ny8eb

Installation: Just git clone the repo, locate the app.py file, and run ‘python3 app.py’ in the terminal

Usage: Lauch the app, and navigate to the default localhost http://127.0.0.1:8050/ There are some dashboards that help users learn about the data. Users can choose data from dropdown or insert data to get result

What’s the design of the application: On this 3X2 dashboard, there are totally 6 widgets. 3 of them accept user input to display data on charts, one of them displays constant data, 2 of them accept user inputs to update faculty and university information. 

How to implement it: Utilize Dash framework to build frontend and backend, use pymql and mysql database for data consistency

Database techniques: Using mysql database. I use Amazon RDS for accessing active MySQL environment.  Using ‘view’ in widget 4 to display data, use 'indexing' to improve the performance, use stored procedures for reusability and readability, use transaction to commit the data into database

Extra credit: No

Contributions: solely myself, approximately 25 hours  
