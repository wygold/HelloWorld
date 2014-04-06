__author__ = 'wangyong'

from pyalgotrade import strategy
from pyalgotrade import dataseries
from pyalgotrade.dataseries import aligned
from pyalgotrade import plotter
from pyalgotrade.stratanalyzer import returns
from pyalgotrade.tools import yahoofinance
from pyalgotrade.technical import ma
from pyalgotrade.technical import trend


import numpy as np
import statsmodels.api as sm

class MyStrategy(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument, smaPeriod,cash):
        strategy.BacktestingStrategy.__init__(self,feed, cash)
        self.getBroker().setUseAdjustedValues(True)
        self.__positions = []
        self.__cash = cash
        self.__instrument = instrument
        self.__sma = ma.SMA(feed[self.__instrument].getAdjCloseDataSeries(), smaPeriod)

        self.__last_sma = 0
        self.__sma_period=smaPeriod
        self.__lowest_price = 0
        self.__buy_point = 0
        self.__cut_loss_point = 0
        self.__first_reverse_point = False
        self.__second_reverse_point = False
        self.__day_counter = 0
        self.__cost = 0
        self.__last_status_day = 0



    def onStart(self):
        print "Initial portfolio value: $%.2f" % self.getBroker().getEquity()

    def onEnterOk(self, position):
        execInfo = position.getEntryOrder().getExecutionInfo()
        print execInfo.getDateTime().strftime("%Y%m%d : ") + "BUY at $%.2f for %.2f stocks, total spend %.2f" % (execInfo.getPrice(), execInfo.getQuantity(), execInfo.getPrice() * execInfo.getQuantity())
        if self.__cut_loss_point < execInfo.getPrice() * 0.9 :
            self.__cut_loss_point = execInfo.getPrice() * 0.9
        self.__cash = self.__cash - execInfo.getPrice() * execInfo.getQuantity()
        self.__positions.append(position)
#        positionTracker=position.getPosTracker()
#        print position.getReturnImpl(10,True)
#        print positionTracker.getCost()

    def getSMA(self):
        return self.__sma

    def onEnterCanceled(self, position):
        self.__positions.pop()

    def onExitOk(self, position):
        execInfo = position.getExitOrder().getExecutionInfo()
        print execInfo.getDateTime().strftime("%Y%m%d : ") + "SELL at $%.2f" % (execInfo.getPrice())
        self.__positions.pop()
        self.__cash = self.__cash + execInfo.getPrice() * execInfo.getQuantity()
        self.__cut_loss_point = 0
        self.__cost =  execInfo.getPrice()

    def onExitCanceled(self, position):
        # If the exit was canceled, re-submit it.
        self.__position.exit()

    def onBars(self, bars):
        # Wait for enough bars to be available to calculate a SMA.
        bar=bars[self.__instrument]

        #print bar.getDateTime(), bar.getAdjClose(),  self.__slope[-1], self.__slope2[-1], self.__position
        #print self.__cash, len(self.__positions)

        barDs = self.getFeed().getDataSeries(self.__instrument)

        abc = barDs.getOpenDataSeries()
        print abc.getLength()



    def onFinish(self, bars):
        print "Final portfolio value: $%.2f" % self.getBroker().getEquity()

    def kill(self):
        del self

def main(plot, instruments, smaPeriod, cash):

    # Download the bars.
    # In the instruments,I can provide more instruments.The instruments name can be got from yahoo finance.
    #instruments = ["c07.si","C09.SI","C31.SI","E5H.SI"]
    #instruments = ["h78.si"]
    #feed is a Feed type defined in yahoofeed.py
    feed = yahoofinance.build_feed(instruments, 2008, 2014, "./Historical_Price")

    for instrument in instruments:
        myStrategy = MyStrategy(feed, instrument, smaPeriod, cash)

        if plot == True :
            # Attach a returns analyzers to the strategy.
            returnsAnalyzer = returns.Returns()
            myStrategy.attachAnalyzer(returnsAnalyzer)

            # Attach the plotter to the strategy.
            plt = plotter.StrategyPlotter(myStrategy)
            # Include the SMA in the instrument's subplot to get it displayed along with the closing prices.
            #plt.getInstrumentSubplot(instrument).addDataSeries("SMA", myStrategy.getSMA())
            # Plot adjusted close values instead of regular close.
            plt.getInstrumentSubplot(instrument).setUseAdjClose(True)
            # Plot the strategy returns at each bar.
            #plt.getOrCreateSubplot("returns").addDataSeries("Net return", returnsAnalyzer.getReturns())
            #plt.getOrCreateSubplot("returns").addDataSeries("Cum. return", returnsAnalyzer.getCumulativeReturns())

        myStrategy.run()
        print "Result for %s : %.2f" % (instrument, myStrategy.getResult())

        # Plot the strategy.
        if plot == True :
            plt.plot()

if __name__ == "__main__":
    #instruments = [["c07.si"],["C09.SI"],["C31.SI"],["E5H.SI"],["bn4.si"], ["d05.si"]]
    instruments = [["c09.si"]]
    smaPeriod = 3
    cash = 20000
    for instrument in instruments:
        main(True,instrument, smaPeriod,cash)
