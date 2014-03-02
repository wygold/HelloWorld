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


    def onStart(self):
        print "Initial portfolio value: $%.2f" % self.getBroker().getEquity()

    def onEnterOk(self, position):
        execInfo = position.getEntryOrder().getExecutionInfo()
        print "%s: BUY at $%.2f for %.2f stocks, total spend %.2f" % (execInfo.getDateTime(), execInfo.getPrice(), execInfo.getQuantity(), execInfo.getPrice() * execInfo.getQuantity())
        if self.__cut_loss_point < execInfo.getPrice() * 0.9 :
            self.__cut_loss_point = execInfo.getPrice() * 0.9
        self.__cash = self.__cash - execInfo.getPrice() * execInfo.getQuantity()
        self.__positions.append(position)
#        positionTracker=position.getPosTracker()
#        print position.getReturnImpl(10,True)
#        print positionTracker.getCost()


    def onEnterCanceled(self, position):
        self.__positions.pop()

    def onExitOk(self, position):
        execInfo = position.getExitOrder().getExecutionInfo()
        print "%s: SELL at $%.2f" % (execInfo.getDateTime(), execInfo.getPrice())
        self.__positions.pop()
        self.__cash = self.__cash + execInfo.getPrice() * execInfo.getQuantity()
        self.__cut_loss_point = 0

    def onExitCanceled(self, position):
        # If the exit was canceled, re-submit it.
        self.__position.exit()

    def onBars(self, bars):
        # Wait for enough bars to be available to calculate a SMA.
        bar=bars[self.__instrument]

        #print bar.getDateTime(), bar.getAdjClose(),  self.__slope[-1], self.__slope2[-1], self.__position
        #print self.__cash, len(self.__positions)


        if self.__day_counter % self.__sma_period == 0 and self.__sma[-1] is not None :

            if self.__last_sma is None :
                    self.__last_sma = self.__sma[-1]

            print self.__last_sma,self.__sma[-1]

            #set up lowest price
            if self.__sma[-1] < self.__last_sma and self.__first_reverse_point == False :
                self.__lowest_price = self.__sma[-1]
                print bar.getDateTime().strftime("%Y%m%d : ") + "lowest price now is %f" % (self.__sma[-1])

            #possible trend reverse, set up a check flag now
            if self.__sma[-1] > self.__last_sma and self.__last_sma <>0 and self.__first_reverse_point == False :
                self.__first_reverse_point = True
                print bar.getDateTime().strftime("%Y%m%d : ") + "First reverse point"

            #LOOKING FOR NEXT REVERSE POINT
            #set up a second check flag now, store yesterday SME(5) as a buying point
            if self.__sma[-1] < self.__last_sma and self.__first_reverse_point == True and self.__second_reverse_point == False :
                self.__second_reverse_point = True
                self.__buy_point = self.__sma[-1]
                print bar.getDateTime().strftime("%Y%m%d : ") + "Second reverse point. Price is %f" % ( self.__buy_point)

            #LOOKING FOR NEXT REVERSE POINT
            #Trend is still going down!
            if self.__sma[-1] < self.__lowest_price and self.__first_reverse_point == True and self.__second_reverse_point == True :
                self.__first_reverse_point = False
                self.__second_reverse_point = False
                print "no buy!"

            #Trend is going back!
            #IF TODAY SME> buying point, then buy 10% of totally cash, loss cut price is 90% of the buy price.
            if self.__sma[-1] > self.__buy_point and self.__first_reverse_point == True and self.__second_reverse_point == True \
                    and len(self.__positions) == 0:
                share = int(self.__cash * 0.1 / bar.getAdjClose())
                self.enterLong(self.__instrument, share, True)
                self.__first_reverse_point = False
                self.__second_reverse_point = False
                print "buy something"

            self.__last_sma = self.__sma[-1]

        #eliminate all position if things goes wrong
        #if (self.__slope2[-1] < 0  ) and self.__positions is not None:
        if len(self.__positions) > 0 :
            if bar.getAdjClose() < self.__cut_loss_point :
                for position in self.__positions :
                    if position.exitActive() is False:
                        position.exit(goodTillCanceled=True)

            if bar.getAdjClose()*0.9 > self.__cut_loss_point :
                self.__cut_loss_point = bar.getAdjClose()*0.9

        self.__day_counter= self.__day_counter+1

    def onFinish(self, bars):
        print "Final portfolio value: $%.2f" % self.getBroker().getEquity()


def main(plot):

    smaPeriod = 3
    cash = 20000

    # Download the bars.
    # In the instruments,I can provide more instruments.The instruments name can be got from yahoo finance.
    #instruments = ["c07.si","C09.SI","C31.SI"]
    instruments = ["c07.si"]
    #feed is a Feed type defined in yahoofeed.py
    feed = yahoofinance.build_feed(instruments, 2010, 2013, ".")

    for instrument in instruments:
        myStrategy = MyStrategy(feed, instrument, smaPeriod, cash)
        myStrategy.run()
        print "Result for %s : %.2f" % (instrument, myStrategy.getResult())


if __name__ == "__main__":
    main(False)