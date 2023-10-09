# Flight-Management-Dashboard

These days, machine learning has a key role in most fields such as health, business and marketing, transportation, finance, and so forth. and definitely, It will change the world using emerging products and tools developed in this area.<br />
<br>This dashboard was developed for the three most popular NYC airports, John F. Kennedy International Airport(JFK), LaGuardia Airport(LGA), and Newark Liberty International Airport(EWR) using the three datasets published on Kaggle.  

# About Target Audiences

It can be useful for the airline's operations team and flight passengers.

# About Datasets

The datasets used in this project are:
<ul>
<li><code>NYC_Flight_Delay</code>: undoubtedly, It is one of the most challenging datasets that I've ever worked with. This dataset contains all flights that operated in JFK, LGA, and EWR airports in 2013. You can access this dataset on Kaggle using this <a href='https://www.kaggle.com/datasets/lampubhutia/nyc-flight-delay'>link</a></li><br />
<li><code>JFK, NYC, and LGA Weather</code>: I collected this dataset from <a href='https://mesonet.agron.iastate.edu/request/download.phtml?network=NY_ASOS'>The Iowa Environmental Mesonet (IEM)</a> to create the next dataset from combining this one with the previous dataset. This dataset contains the weather of JFK, NYC, and LGA. because there is no data for IATA code EWR and because Newark Liberty International Airport(EWR) is located in west-southwest of Manhattan in New York City, we use the weather records of NYC in 2013 for EWR</li><br />
<li><code>JFK, EWR, and LGA Flights</code>: After 10 hours, the dataset was ready to use for doing the final preprocessing.</li>
</ul>

# About Technologies
<ul>
  <li><code>Bokeh</code>: I used the Bokeh library to implement widgets, tabs, interactive plots, and the current document object.</li><br />
  <li><code>Python</code>: I utilized the Python programming language to implement widget functionalities and production transformers.</li><br />
  <li><code>Bokeh Server</code>: I used Bokeh Serve to run the Python app on the web, manage requests, and retrieve the response.</li><br />
  <li><code>Docker</code>: I utilized Docker to create an image and start a container from the SQL Server image, which has the specific tag 2022-latest.</li>
</ul>


# About Tabs

This dashboard contains 6 different main modules for creating the tabs of the current document that are:
<ul>
  <li>Predicting Arival Time</li>
  <li>The Distribution of Arrival Delay</li>
  <li>The Variability of Arrival Delay</li>
  <li>Search for The relevant details of Airline Carriers</li>
  <li>Departure Time Information</li>
  <li>Arrival Time Information</li>
</ul>

<pre>The Predicting Arrival Time Tab</pre>
With this tab, you can predict the arrival time for different flights in 2013 and any flights operated in the range of 2010-01-01 to the current date. In this module, I used a stacked model that utilized an XGBoost and CatBoost regressor as base estimators and another XGBoost as a final estimator. You can check out the stages of making the model on a Kaggle notebook from this <a href='https://www.kaggle.com/code/amirhoseinsedaghati/arrival-time-prediction-using-stacking-model/'>link</a>.<br />
<br/> In order to predict the arrival time of a flight for an unseen date, It should first find the instances that are related to the provided date and then find the closest departure time to the provided departure time in the text input. because the model has not seen the data for some routes such as EWR to OAK, you should an alternative route, and because it has seen limited data for different routes in a day, it might change the value of the departure time, scheduled departure time, and scheduled arrival time cells because It could not find a departure time that is close to the time you provided.
probably, This flaw will lost or decrease when the size of the training data is 20 X, 200 X, or n X bigger than the current size.<br />

Increasing the size of the training data, we can add a new tab to the dashboard that recommends the flight arrangements of each route daily and achieve a model that can predict the arrival time without changing the provided value.<br />

<img src='https://i.postimg.cc/VNGcKPzd/Screenshot-from-2023-10-09-01-06-38.png'>

As you can see the model returns a string including the amount of arrival delay and the potential landing time.

<pre>The Distribution of Arrival Delay Tab</pre>
This tab shows the normal distribution (or Gaussian distribution) of arrival delay for the first 2 airline carriers, AirTran Airways, and Alaska Airlines by default based on the arrival delay range and the number of bins in 2013. But you can change the airline carriers shown in the checkbox widget, the histogram binning, and the arrival delay range.<br />

<img src='https://i.postimg.cc/xCn81K4D/Screenshot-from-2023-10-09-02-06-01.png'>

<pre>The Variability of Arrival Delay Tab</pre>
It shows the data variability and data density of arrival delay for the U.S. airline carriers based on the selected IATA codes for origin and destination airports in 2013.<br />

<img src='https://i.postimg.cc/Kz7DVrd1/Screenshot-from-2023-10-09-02-09-18.png'>

<pre>Search for The relevant details of Airline Carriers Tab</pre>
It provides a simple search engine that helps you to search values based on the airline carriers, table headers, and the value provided in each column and receive them in a table.<br />

<img src='https://i.postimg.cc/Dzv1wjwF/Merged-document.png'>

<pre>Departure Time Information Tab</pre>
It provides statistical information on the departure time for U.S. airline carriers in 2013 such as the number of flights, the departure time average, the departure time standard deviation, the shortest departure time, and the longest departure time.<br />

<img src='https://i.postimg.cc/RZVxXMxj/Screenshot-from-2023-10-09-03-02-56.png'>

<pre>Arrival Time Information Tab</pre>
It provides statistical information on the Arrival time for U.S. airline carriers in 2013 such as the number of flights, the arrival time average, the arrival time standard deviation, the shortest arrival time, and the longest arrival time.<br />

<img src='https://i.postimg.cc/4y71Q2JK/Screenshot-from-2023-10-09-03-05-25.png'>

# How to run
1. Use this <a href=''>url</a> to see it online.
2. to run it on your local machine, follow the following steps
   - open a cmd or terminal window
   - Install the sqlcmd command-line client from <a href='https://learn.microsoft.com/en-us/sql/tools/sqlcmd/sqlcmd-utility?view=sql-server-ver16&tabs=odbc%2Clinux&pivots=cs1-bash'>Microsoft Websit</a><br />
   - Install the SQL Server image using `docker pull mcr.microsoft.com/mssql/server:2022-latest`
   - Start a container from the SQL Server image using `docker run -e 'ACCEPT_EULA=Y' -e 'SA_PASSWORD=YourPassword' -p 1433:1433 --name your_database_name -d mcr.microsoft.com/mssql/server:2022-latest`
   - Connect to the SQL Server instance and Create a database using `sqlcmd -S localhost,1433 -U sa -P YourPassword -C -Q "CREATE DATABASE your_database_name"`
   - Run create_db_table.py which is located in the database folder after replacing real data with synthetic data.
   - Run main.py using `bokeh serve main.py` after replacing real data with synthetic data.

