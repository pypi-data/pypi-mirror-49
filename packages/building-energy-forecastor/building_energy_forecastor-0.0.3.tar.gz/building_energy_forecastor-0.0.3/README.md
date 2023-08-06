# Forecastor for Buildings' Consumption

Go check ce lien pour rédiger le README: 
[Github-flavored Markdown](https://guides.github.com/features/mastering-markdown/)

### Installation
Command line:
*pip install building_energy_forecastor*

### Features' list for preprocessing data from *src/building_preprocess*
* **day_of_week(date_serie)**: Takes a pandas.Series of dates and returns a pandas.Series of corresponding week days
(['Monday', 'Tuesday', ...]).
* **set_time_index(df, timeindex='Timestamp')**: Set the time column as index of the dataframe df. By default the column's
label is 'Timestamp'.
* **time_to_cycle(df, timeindex='Timestamp')**: From the 3rd competitor of the [Forecast challenge](https://www.drivendata.org/competitions/51/electricity-prediction-machine-learning/)
by Schneider Electric. Add column to a copy of df containing cosinus and sinus functions of the time of the day, the month of the year and the day of the year.
* **add_weather(df, weather, timeindex='Timestamp', freq_temp='D')**: From the 3rd competitor of the [Forecast challenge](https://www.drivendata.org/competitions/51/electricity-prediction-machine-learning/) by Schneider Electric.
Adds the weather data to the training dataset (*df* here) merging the two dataframes on the 'Timestamp' and rouding the time
value in weather to the precised freq_temp ('D' by default).
* **fill_temperature(df, tempindex='Temperature')**: fill the NaN values in the tempindex column by computing the mean on the
two closest framing values.

### Model functions from *src/building_model*
* **building_regressor()**: Returns a linear regressor from Scikit-learn.
* **building_train(reg, X, y)**: Trains the regressor with X the data and Y the targeted values.
* **building_prediction(reg, X)**: Returns a pandas.DataFrame showing the prediction of the regressor *reg* given the data *X*.
