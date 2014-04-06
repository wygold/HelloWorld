__author__ = 'wangyong'

import pattern
from pyalgotrade import dataseries
from pyalgotrade.dataseries import bards

class HammerPattern(pattern.CandleStick) :
    def __init__(self, barDs) :
        self.__barDs = barDs
        self.__openDs = barDs.getOpenDataSeries
        self.__closeDs = barDs.getCloseDataSeries
        self.__highDs = barDs.getHighDataSeries
        self.__lowDs = barDs.getLowDataSeries


    def validatePatter(self) :
        if self.__openDs.getLength() > 1 :
            open= self.__openDs.get




