import requests
from bs4 import BeautifulSoup
from datetime import datetime
from dateutil.relativedelta import relativedelta
import numpy as np
import pandas_datareader as pdr
from sklearn import linear_model
from sklearn.preprocessing import PolynomialFeatures
import matplotlib.pyplot as plt

class StockMarketPrice:
    def __init__(self, tickerSymbol):
        self.tickerSymbolOfCompany = tickerSymbol
        self.url = f"https://finance.yahoo.com/quote/{self.tickerSymbolOfCompany}/history?p={self.tickerSymbolOfCompany}"
        self.getRequest = requests.get(self.url).text
        # xml very fast and lenient
        self.soup = BeautifulSoup(self.getRequest, 'lxml')
        self.df = self.getDataForHD()
        self.currency = self.getCurrency()

    def getCurrency(self):
        currency = self.soup.find('span', {'class' : 'Fz(xs)'}).find_all('span')[0].text
        return currency

    def getDataForLive(self):
        currentPrice = self.soup.find('div', {'class': 'D(ib) Mend(20px)'}).find_all('span')[0].text
        priceDelta = self.soup.find('div', {'class': 'D(ib) Mend(20px)'}).find_all('span')[1].text
        return str(currentPrice) + " " + str(priceDelta)

    def displayLivePrice(self):
        now = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        return f"Current price for {self.tickerSymbolOfCompany} at {now} is {self.getDataForLive()} ({self.currency})"

    def getDataForHD(self):
        # historical data dataframe
        # data from 1 years ago from now
        historicalDF = \
            pdr.get_data_yahoo(symbols=self.tickerSymbolOfCompany,
                               start=datetime.today() - relativedelta(years=1), end=datetime.today())
        # include Date index in dataframe
        historicalDF.reset_index(inplace=True, drop=False)
        return historicalDF

    def pricePrediction(self, whichCol, howManyDaysAfterTodayToPredict):
        date_time = self.df['Date']
        # starting date of historical date is 0
        indepVar = np.arange(date_time.size)
        # making dependent variable a 2d numpy array
        _2DindepVar = np.reshape(indepVar, (-1, 1))

        whichDateToPredict = _2DindepVar[len(_2DindepVar) - 1][0] + howManyDaysAfterTodayToPredict

        # what to predict
        depVar = self.df[whichCol].to_numpy()
        _2DdepVar = np.reshape(depVar, (-1, 1))

        # polynomial regression
        poly_features = PolynomialFeatures(degree=10)
        # contain original independent variable and its new features
        indepVar_poly = poly_features.fit_transform(_2DindepVar)
        model = linear_model.LinearRegression()
        model.fit(indepVar_poly, _2DdepVar)  # Fit the model
        to_predict = poly_features.fit_transform(np.array([[whichDateToPredict]]))
        predicted = model.predict(to_predict)
        pricePredicted = "{:.2f}".format(predicted[0][0]) # two decimal points

        # print predicted High
        return f"Predicted {whichCol} price for {self.tickerSymbolOfCompany} " \
               f"in {howManyDaysAfterTodayToPredict} day(s) is {pricePredicted} ({self.currency})"


    def plotTrend(self):
        # https://queirozf.com/entries/pandas-dataframe-plot-examples-with-matplotlib-pyplot
        ax = plt.gca()

        self.df.plot(kind='line', x='Date', y='Close', ax=ax)
        self.df.plot(kind='line', x='Date', y='High', color='red', ax=ax)
        self.df.plot(kind='line', x='Date', y='Low', color='blue', ax=ax)
        plt.show()

    def getEarningRate(self, priceYouPaid, numOfStocks):
        # ((current price of stocks / price you paid when buying stocks) - 1) * 100
        currentPrice = self.soup.find('div', {'class': 'D(ib) Mend(20px)'}).find_all('span')[0].text
        currentPrice = float(currentPrice)
        earningRate = ((currentPrice / priceYouPaid) - 1) * 100
        earningRate = "{:.2f}".format(earningRate) # two decimal places
        earnings = (currentPrice - priceYouPaid) * numOfStocks
        earnings = "{:.2f}".format(earnings) # two decimal places
        return f"Your earning rate is {earningRate}% and you have earned {earnings} ({self.currency})"

