__author__ = 'wangyong'

from pyalgotrade import strategy
from pyalgotrade import dataseries
from pyalgotrade.dataseries import aligned
from pyalgotrade import plotter
from pyalgotrade.tools import yahoofinance
from pyalgotrade.technical import ma
from pyalgotrade.technical import trend

import numpy as np
import statsmodels.api as sm

class MyStrategy(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument, smaPeriod,cash):
        strategy.BacktestingStrategy.__init__(self,feed, cash)
        self.getBroker().setUseAdjustedValues(True)
        self.__position = None
        self.__positions = []
        self.__cash = cash
        self.__i1 = instrument
        self.__sma = ma.SMA(feed[self.__i1].getAdjCloseDataSeries(), smaPeriod)
        self.__slope=trend.Slope(feed[self.__i1].getAdjCloseDataSeries(),45)
        self.__slope2=trend.Slope(feed[self.__i1].getAdjCloseDataSeries(),15)


    def onStart(self):
        print "Initial portfolio value: $%.2f" % self.getBroker().getEquity()

    def onEnterOk(self, position):
        execInfo = position.getEntryOrder().getExecutionInfo()
        print "%s: BUY at $%.2f for $%.2f" % (execInfo.getDateTime(), execInfo.getPrice(), execInfo.getQuantity())
        self.__cash = self.__cash - execInfo.getPrice() * execInfo.getQuantity()
        self.__positions.append(position)
#        positionTracker=position.getPosTracker()
#        print position.getReturnImpl(10,True)
#        print positionTracker.getCost()


    def onEnterCanceled(self, position):
        self.__position = None

    def onExitOk(self, position):
        execInfo = position.getExitOrder().getExecutionInfo()
        print "%s: SELL at $%.2f" % (execInfo.getDateTime(), execInfo.getPrice())
        self.__cash = self.__cash + execInfo.getPrice() * execInfo.getQuantity()
        self.__position = None
        self.__positions = []

    def onExitCanceled(self, position):
        # If the exit was canceled, re-submit it.
        self.__position.exit()

    def onBars(self, bars):
        # Wait for enough bars to be available to calculate a SMA.
        bar=bars[self.__i1]

        if self.__slope[-1] is None:
            return

        #print bar.getDateTime(), bar.getAdjClose(),  self.__slope[-1], self.__slope2[-1], self.__position
        #print self.__cash, len(self.__positions)

        if self.__cash >0 :
                # Buy if both long and short slope indicates the price is going up
            if self.__slope[-1]> 0 and self.__slope2[-1]>0 and len(self.__positions) == 0 :
                # Buy 10 percent of our total cash for the stock
                share = int(self.__cash * 0.1 / bar.getAdjClose)
                self.__position = self.enterLong(self.__i1, share, True)
                #keep buy in if both indicates shows position
            elif self.__slope[-1]> 0 and self.__slope2[-1]>0 :
                share = int(self.__cash * 0.1 / bar.getAdjClose)
                self.__position = self.enterLong(self.__i1, share, True)
                #eliminate all position if things goes wrong
            elif (self.__slope2[-1] < 0  ) and self.__position.exitActive() is False:

                self.__position.exit(goodTillCanceled=True)



    def onFinish(self, bars):
        print "Final portfolio value: $%.2f" % self.getBroker().getEquity()


def main(plot):

    smaPeriod = 10
    cash = 20000

    # Download the bars.
    # In the instruments,I can provide more instruments.The instruments name can be got from yahoo finance.
    instruments = ["c07.si","C09.SI","C31.SI"]
    #instruments = ["c07.si"]
    #feed is a Feed type defined in yahoofeed.py
    feed = yahoofinance.build_feed(instruments, 2012, 2013, ".")

    for instrument in instruments:
        myStrategy = MyStrategy(feed, instrument, smaPeriod, cash)
        myStrategy.run()
        print "Result for %s : %.2f" % (instrument, myStrategy.getResult())


if __name__ == "__main__":
    main(False)