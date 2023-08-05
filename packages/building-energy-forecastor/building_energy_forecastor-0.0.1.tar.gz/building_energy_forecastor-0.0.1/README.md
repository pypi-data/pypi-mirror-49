# Forecastor for Buildings' Consumption

Go check ce lien pour rédiger le README: 
[Github-flavored Markdown](https://guides.github.com/features/mastering-markdown/)

### 1. Choses à faire 
- [ ] FAUT MODIFIER LE SETUP.PY? VOILA VOILA
- [ ] Ajouter des features
    - [ ] Gérer les exceptions un peu partout pour que ce soit user friendly \*_* (simley avec des étoiles dans les yeux)
- [ ] Ajouter un modele (voir 2 ou 3 soyons fous)
- [ ] comprendre plus encore le sujet mdr

### 2. Features' List for preprocessing data
* **day_of_week(date_serie)**: Input: serie of dates ; Output: serie of corresponding week days (['Monday', 'Tuesday', ...])
* **cycle_time(df)**: From the 3rd competitor of the [Forecast challenge](https://www.drivendata.org/competitions/51/electricity-prediction-machine-learning/) by Schneider Electric ; turns time in a continous element (no break between 23h59 and 00h01) by applying cosinus and sinus functions
* **add_weather(df, weather_df)**: From the 3rd competitor of the [Forecast challenge](https://www.drivendata.org/competitions/51/electricity-prediction-machine-learning/) by Schneider Electric ; add the weather data to the training dataset (*df* here) merging the two dataframes on the 'Timestamp'

### 3. Requirements for dataframes
* The column containing dates must be labeled 'Timestamp'

### 4. Model functions
* **building_regressor()**: returns a linear regressor from Scikit-learn
* **building_train(reg, X, y)**: train the regressor with X the data and Y the targeted values
* **building_prediction(reg, X)**: returns a dataframe showing the prediction of the regressor *reg* given the data *X*



### 5. To install the package
* Command: python -m pip install --index-url https://test.pypi.org/simple/ --no-deps building_energy_forecastor