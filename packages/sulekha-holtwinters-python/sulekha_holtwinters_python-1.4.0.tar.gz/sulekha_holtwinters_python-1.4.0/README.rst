Author: Sulekha Aloorravi
Email: sulekha.aloorravi@gmail.com
Package: sulekha_holtwinters_python
This package is to forecast timeseries on a Pandas Dataframe using Holt winters Forecasting model.

URL to test this code: https://github.com/sulekhaaloorravi-python/sulekha_holtwinters_python/blob/master/test_holtwinters.ipynb

Example to load existing package data:
        #import package
        from sulekha_holtwinters_python.holtwinters import holtwinters as hw
        #Pandas setup
        import pandas as pd

        #Load data available within this package
        import pkg_resources
        DB_FILE = pkg_resources.resource_filename('sulekha_holtwinters_python', 'data')
        testDF = pd.read_csv(DB_FILE)