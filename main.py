import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont
from stockPrice import StockMarketPrice

# https://hello-bryan.tistory.com/213
# https://pythonpyqt.com/pyqt-qlineedit/
# https://pythonprogramminglanguage.com/pyqt-line-edit/

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # form
        self.setWindowTitle('Stock Price Live and Prediction')
        self.center() # self.move(500,200)    # 창 위치
        self.resize(700, 600)   # 창 크기

        # input ticker symbol
        self.tickerLabel = QLabel(self)
        self.tickerLabel.setText('Enter ticker symbol of your company:')
        self.tickerLabel.setFont(QFont("Arial", 20))
        self.tickerLine = QLineEdit(self)

        self.tickerLabel.move(20, 20)
        self.tickerLine.move(20, 70)
        self.tickerLine.resize(400, 32)

        self.label = QLabel(self)
        self.label.setText("1. Enter the ticker symbol of your company \nand click \"Enter\" button\n"
                           "2. Make sure the message \"TICKER \nSYMBOL OF YOUR COMPANY HAS \nBEEN ENTERED!!\" shows up\n"
                           "3. Click one of the buttons\n"
                           "4. Make sure you know this application has \nlimits and does not guarantee any accuracy\n"
                           "5. Use this application at your own risk\n")
        self.label.setFont(QFont("Arial", 20))
        self.label.move(20, 160)

        # btnEnter
        btnEnter = QPushButton('Enter', self)
        btnEnter.clicked.connect(self.stockPriceInfo)
        btnEnter.resize(100, 32)
        btnEnter.move(430, 70)

        # btnLive
        btnLive = QPushButton("Live Price", self)  # 버튼 텍스트
        btnLive.move(20, 120)  # 버튼 위치
        btnLive.clicked.connect(self.displayLivePrice)  # 클릭 시 실행할 function

        # btnPredict
        btnPredict = QPushButton("Price Prediction", self)  # 버튼 텍스트
        btnPredict.move(120, 120)  # 버튼 위치
        btnPredict.clicked.connect(self.predictPrice)  # 클릭 시 실행할 functionAAPL

        #btnTrend
        btnTrend = QPushButton("Price Trend", self)  # 버튼 텍스트
        btnTrend.move(223, 120)  # 버튼 위치
        btnTrend.clicked.connect(self.displayPriceTrend)  # 클릭 시 실행할 function

        #btnEarnings
        btnEarningRate = QPushButton("Earning Rate", self) # 버튼 텍스트
        btnEarningRate.move(322, 120) # 버튼 위치
        btnEarningRate.clicked.connect(self.displayEarningRate) # 클릭 시 실행할 function

    # initialize StockMarketPrice object
    def stockPriceInfo(self):
        self.spi = StockMarketPrice(self.tickerLine.text())
        self.tickerSymbolEntered()

    # enter ticker symbol
    def tickerSymbolEntered(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("TICKER SYMBOL OF YOUR COMPANY HAS BEEN ENTERED!!")
        msg.setWindowTitle("Information")
        msg.exec_()

    #display current price
    def displayLivePrice(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(self.spi.displayLivePrice())
        msg.setWindowTitle("Information")
        msg.exec_()

    # display price trend
    def displayPriceTrend(self):
        self.spi.plotTrend()

    # predict price
    def predictPrice(self):
        whichCol, done1 = QInputDialog.getText(
            self, 'Open, High, Low, or Close',
            'Enter what type of stock prices you want to predict: Open, High, Low, or Close: ')

        howManyDaysAfterTodayToPredict, done2 = QInputDialog.getInt(
            self, 'How many days after today?',
            'You want to predict stock price in how many days?: ')

        if done1 and done2:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText(self.spi.pricePrediction(whichCol, howManyDaysAfterTodayToPredict))
            msg.setWindowTitle("Information")
            msg.exec_()

    def displayEarningRate(self):
        priceYouPaid, done3 = QInputDialog.getDouble(
            self, 'price per stock you paid',
            'Enter price per stock you paid when you purchased it (currency should be matching): ')

        numOfStocks, done4 = QInputDialog.getInt(
            self, 'number of stocks you bought',
            'Enter the number of stocks you bought: ')

        if done3 and done4:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText(self.spi.getEarningRate(priceYouPaid, numOfStocks))
            msg.setWindowTitle("Information")
            msg.exec_()

    # window at the center of my monitor
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

def main():
   app = QApplication(sys.argv)
   ex = App()
   ex.show()
   sys.exit(app.exec_())

if __name__ == '__main__':
   main()
