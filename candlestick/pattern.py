__author__ = 'wangyong'


from pyalgotrade import dataseries
from pyalgotrade.dataseries import bards

class Pattern:

    __openDs = dataseries.SequenceDataSeries()
    __closeDs = dataseries.SequenceDataSeries()
    __highDs = dataseries.SequenceDataSeries()
    __lowDs = dataseries.SequenceDataSeries()
    tdyPosition = 0

    def __init__(self, barDs) :
        self.__barDs = barDs
        self.__openDs = barDs.getOpenDataSeries()
        self.__closeDs = barDs.getCloseDataSeries()
        self.__highDs = barDs.getHighDataSeries()
        self.__lowDs = barDs.getLowDataSeries()
        self.tdyPosition=self.__openDs.getLength()-1

    def isHammer(self) :
        tdyRealBody = self.__openDs.getValueAbsolute(self.tdyPosition)-self.__closeDs.getValueAbsolute(self.tdyPosition)

        if self.__openDs.getValueAbsolute(self.tdyPosition) > self.__closeDs.getValueAbsolute(self.tdyPosition) :
            tdyLowerShadow = self.__closeDs.getValueAbsolute(self.tdyPosition)-self.__lowDs.getValueAbsolute(self.tdyPosition)
            tdyUpperShadow = self.__highDs.getValueAbsolute(self.tdyPosition)-self.__openDs.getValueAbsolute(self.tdyPosition)
        else :
            tdyLowerShadow = self.__openDs.getValueAbsolute(self.tdyPosition)-self.__lowDs.getValueAbsolute(self.tdyPosition)
            tdyUpperShadow = self.__highDs.getValueAbsolute(self.tdyPosition)-self.__closeDs.getValueAbsolute(self.tdyPosition)

        if tdyLowerShadow > abs(tdyRealBody) and tdyRealBody <> 0 and tdyUpperShadow == 0 :
            return (tdyLowerShadow - abs(tdyRealBody)) / abs(tdyRealBody)
        else :
            return 0

    def isShootingStar(self) :
         # assign today body, bodyhigh, bodylow
        if self.__closeDs.getValueAbsolute(self.tdyPosition) > self.__openDs.getValueAbsolute(self.tdyPosition) :
            tdyRealBody = self.__closeDs.getValueAbsolute(self.tdyPosition)-self.__openDs.getValueAbsolute(self.tdyPosition)
            tdyRealBodyHigh = self.__closeDs.getValueAbsolute(self.tdyPosition)
            tdyRealBodylow = self.__openDs.getValueAbsolute(self.tdyPosition)
        else :
            tdyRealBody = self.__closeDs.getValueAbsolute(self.tdyPosition)-self.__openDs.getValueAbsolute(self.tdyPosition)
            tdyRealBodyHigh = self.__openDs.getValueAbsolute(self.tdyPosition)
            tdyRealBodylow = self.__closeDs.getValueAbsolute(self.tdyPosition)

        if self.tdyPosition > 1 :
            # assign yesterday body, bodyhigh, bodylow
            if self.__closeDs.getValueAbsolute(self.tdyPosition-1) > self.__openDs.getValueAbsolute(self.tdyPosition-1) :
                ystRealBody = self.__closeDs.getValueAbsolute(self.tdyPosition-1)-self.__openDs.getValueAbsolute(self.tdyPosition-1)
                ystRealBodyHigh = self.__closeDs.getValueAbsolute(self.tdyPosition-1)
                ystRealBodylow = self.__openDs.getValueAbsolute(self.tdyPosition-1)
            else :
                ystRealBody = self.__closeDs.getValueAbsolute(self.tdyPosition-1)-self.__openDs.getValueAbsolute(self.tdyPosition-1)
                ystRealBodyHigh = self.__openDs.getValueAbsolute(self.tdyPosition-1)
                ystRealBodylow = self.__closeDs.getValueAbsolute(self.tdyPosition-1)

            if tdyRealBody <> 0 :
                if tdyRealBodylow > ystRealBodyHigh and abs(self.__highDs.getValueAbsolute(self.tdyPosition)- tdyRealBodyHigh) > abs(tdyRealBody) \
                    and (tdyRealBodylow-self.__lowDs.getValueAbsolute(self.tdyPosition))/abs(tdyRealBody) < 0.1:
                    return abs(self.__highDs.getValueAbsolute(self.tdyPosition)- tdyRealBodyHigh) / abs(tdyRealBody)
                else :
                    return 0
        return 0

    def isEngulfing(self) :

        # assign today body, bodyhigh, bodylow
        if self.__closeDs.getValueAbsolute(self.tdyPosition) > self.__openDs.getValueAbsolute(self.tdyPosition) :
            tdyRealBody = self.__closeDs.getValueAbsolute(self.tdyPosition)-self.__openDs.getValueAbsolute(self.tdyPosition)
            tdyRealBodyHigh = self.__closeDs.getValueAbsolute(self.tdyPosition)
            tdyRealBodylow = self.__openDs.getValueAbsolute(self.tdyPosition)
        else :
            tdyRealBody = self.__closeDs.getValueAbsolute(self.tdyPosition)-self.__openDs.getValueAbsolute(self.tdyPosition)
            tdyRealBodyHigh = self.__openDs.getValueAbsolute(self.tdyPosition)
            tdyRealBodylow = self.__closeDs.getValueAbsolute(self.tdyPosition)

        if self.tdyPosition > 1 :
            # assign yesterday body, bodyhigh, bodylow
            if self.__closeDs.getValueAbsolute(self.tdyPosition-1) > self.__openDs.getValueAbsolute(self.tdyPosition-1) :
                ystRealBody = self.__closeDs.getValueAbsolute(self.tdyPosition-1)-self.__openDs.getValueAbsolute(self.tdyPosition-1)
                ystRealBodyHigh = self.__closeDs.getValueAbsolute(self.tdyPosition-1)
                ystRealBodylow = self.__openDs.getValueAbsolute(self.tdyPosition-1)
            else :
                ystRealBody = self.__closeDs.getValueAbsolute(self.tdyPosition-1)-self.__openDs.getValueAbsolute(self.tdyPosition-1)
                ystRealBodyHigh = self.__openDs.getValueAbsolute(self.tdyPosition-1)
                ystRealBodylow = self.__closeDs.getValueAbsolute(self.tdyPosition-1)

            if tdyRealBody <>0 and ystRealBody <>0 and tdyRealBody/ystRealBody<0 \
            and tdyRealBodyHigh > ystRealBodyHigh and tdyRealBodylow < ystRealBodylow :
                return 1
            else :
                return 0

        return 0

    def isDarkCloudCover(self) :
          # assign today body, bodyhigh, bodylow
        if self.__closeDs.getValueAbsolute(self.tdyPosition) > self.__openDs.getValueAbsolute(self.tdyPosition) :
            tdyRealBody = self.__closeDs.getValueAbsolute(self.tdyPosition)-self.__openDs.getValueAbsolute(self.tdyPosition)
            tdyRealBodyHigh = self.__closeDs.getValueAbsolute(self.tdyPosition)
            tdyRealBodylow = self.__openDs.getValueAbsolute(self.tdyPosition)
        else :
            tdyRealBody = self.__closeDs.getValueAbsolute(self.tdyPosition)-self.__openDs.getValueAbsolute(self.tdyPosition)
            tdyRealBodyHigh = self.__openDs.getValueAbsolute(self.tdyPosition)
            tdyRealBodylow = self.__closeDs.getValueAbsolute(self.tdyPosition)

        if self.tdyPosition > 1 :
            # assign yesterday body, bodyhigh, bodylow
            if self.__closeDs.getValueAbsolute(self.tdyPosition-1) > self.__openDs.getValueAbsolute(self.tdyPosition-1) :
                ystRealBody = self.__closeDs.getValueAbsolute(self.tdyPosition-1)-self.__openDs.getValueAbsolute(self.tdyPosition-1)
                ystRealBodyHigh = self.__closeDs.getValueAbsolute(self.tdyPosition-1)
                ystRealBodylow = self.__openDs.getValueAbsolute(self.tdyPosition-1)
            else :
                ystRealBody = self.__closeDs.getValueAbsolute(self.tdyPosition-1)-self.__openDs.getValueAbsolute(self.tdyPosition-1)
                ystRealBodyHigh = self.__openDs.getValueAbsolute(self.tdyPosition-1)
                ystRealBodylow = self.__closeDs.getValueAbsolute(self.tdyPosition-1)

            if tdyRealBody < 0 and ystRealBody > 0 \
            and tdyRealBodyHigh > ystRealBodyHigh and tdyRealBodylow < ystRealBodyHigh and tdyRealBodylow > ystRealBodylow :
                return (ystRealBodyHigh - tdyRealBodylow)/ abs(ystRealBody)
            else :
                return 0

        return 0


    def isPiercingLine(self) :
          # assign today body, bodyhigh, bodylow
        if self.__closeDs.getValueAbsolute(self.tdyPosition) > self.__openDs.getValueAbsolute(self.tdyPosition) :
            tdyRealBody = self.__closeDs.getValueAbsolute(self.tdyPosition)-self.__openDs.getValueAbsolute(self.tdyPosition)
            tdyRealBodyHigh = self.__closeDs.getValueAbsolute(self.tdyPosition)
            tdyRealBodylow = self.__openDs.getValueAbsolute(self.tdyPosition)
        else :
            tdyRealBody = self.__closeDs.getValueAbsolute(self.tdyPosition)-self.__openDs.getValueAbsolute(self.tdyPosition)
            tdyRealBodyHigh = self.__openDs.getValueAbsolute(self.tdyPosition)
            tdyRealBodylow = self.__closeDs.getValueAbsolute(self.tdyPosition)

        if self.tdyPosition > 1 :
            # assign yesterday body, bodyhigh, bodylow
            if self.__closeDs.getValueAbsolute(self.tdyPosition-1) > self.__openDs.getValueAbsolute(self.tdyPosition-1) :
                ystRealBody = self.__closeDs.getValueAbsolute(self.tdyPosition-1)-self.__openDs.getValueAbsolute(self.tdyPosition-1)
                ystRealBodyHigh = self.__closeDs.getValueAbsolute(self.tdyPosition-1)
                ystRealBodylow = self.__openDs.getValueAbsolute(self.tdyPosition-1)
            else :
                ystRealBody = self.__closeDs.getValueAbsolute(self.tdyPosition-1)-self.__openDs.getValueAbsolute(self.tdyPosition-1)
                ystRealBodyHigh = self.__openDs.getValueAbsolute(self.tdyPosition-1)
                ystRealBodylow = self.__closeDs.getValueAbsolute(self.tdyPosition-1)

            if tdyRealBody > 0 and ystRealBody < 0 \
            and tdyRealBodylow < ystRealBodylow and tdyRealBodyHigh > ystRealBodylow and tdyRealBodyHigh < ystRealBodyHigh :
                return (tdyRealBodyHigh - ystRealBodylow)/ abs(ystRealBody)
            else :
                return 0

        return 0

    def isEveningStar(self) :
        if self.tdyPosition > 2 :
            # assign today body, bodyhigh, bodylow
            if self.__closeDs.getValueAbsolute(self.tdyPosition) > self.__openDs.getValueAbsolute(self.tdyPosition) :
                tdyRealBody = self.__closeDs.getValueAbsolute(self.tdyPosition)-self.__openDs.getValueAbsolute(self.tdyPosition)
                tdyRealBodyHigh = self.__closeDs.getValueAbsolute(self.tdyPosition)
                tdyRealBodylow = self.__openDs.getValueAbsolute(self.tdyPosition)
            else :
                tdyRealBody = self.__closeDs.getValueAbsolute(self.tdyPosition)-self.__openDs.getValueAbsolute(self.tdyPosition)
                tdyRealBodyHigh = self.__openDs.getValueAbsolute(self.tdyPosition)
                tdyRealBodylow = self.__closeDs.getValueAbsolute(self.tdyPosition)

            # assign yesterday body, bodyhigh, bodylow
            if self.__closeDs.getValueAbsolute(self.tdyPosition-1) > self.__openDs.getValueAbsolute(self.tdyPosition-1) :
                ystRealBody = self.__closeDs.getValueAbsolute(self.tdyPosition-1)-self.__openDs.getValueAbsolute(self.tdyPosition-1)
                ystRealBodyHigh = self.__closeDs.getValueAbsolute(self.tdyPosition-1)
                ystRealBodylow = self.__openDs.getValueAbsolute(self.tdyPosition-1)
            else :
                ystRealBody = self.__closeDs.getValueAbsolute(self.tdyPosition-1)-self.__openDs.getValueAbsolute(self.tdyPosition-1)
                ystRealBodyHigh = self.__openDs.getValueAbsolute(self.tdyPosition-1)
                ystRealBodylow = self.__closeDs.getValueAbsolute(self.tdyPosition-1)

            #assign the day before yesterday body, bodyhigh, bodylow
            if self.__closeDs.getValueAbsolute(self.tdyPosition-2) > self.__openDs.getValueAbsolute(self.tdyPosition-2) :
                preYstRealBody = self.__closeDs.getValueAbsolute(self.tdyPosition-2)-self.__openDs.getValueAbsolute(self.tdyPosition-2)
                preYstlBodyHigh = self.__closeDs.getValueAbsolute(self.tdyPosition-2)
                preYstRealBodylow = self.__openDs.getValueAbsolute(self.tdyPosition-2)
            else :
                preYstRealBody = self.__closeDs.getValueAbsolute(self.tdyPosition-2)-self.__openDs.getValueAbsolute(self.tdyPosition-2)
                preYstRealBodyHigh = self.__openDs.getValueAbsolute(self.tdyPosition-2)
                preYstRealBodylow = self.__closeDs.getValueAbsolute(self.tdyPosition-2)

            if preYstRealBody > 0 and ystRealBodylow>preYstlBodyHigh and tdyRealBodyHigh<ystRealBodylow \
                    and tdyRealBodylow<preYstlBodyHigh and tdyRealBody < 0:
                return abs(tdyRealBodylow-preYstlBodyHigh)/preYstRealBody
            else :
                return 0
        else :
            return 0

    def isDojiEveningStar(self) :
        if self.tdyPosition > 2 :
            # assign today body, bodyhigh, bodylow
            if self.__closeDs.getValueAbsolute(self.tdyPosition) > self.__openDs.getValueAbsolute(self.tdyPosition) :
                tdyRealBody = self.__closeDs.getValueAbsolute(self.tdyPosition)-self.__openDs.getValueAbsolute(self.tdyPosition)
                tdyRealBodyHigh = self.__closeDs.getValueAbsolute(self.tdyPosition)
                tdyRealBodylow = self.__openDs.getValueAbsolute(self.tdyPosition)
            else :
                tdyRealBody = self.__closeDs.getValueAbsolute(self.tdyPosition)-self.__openDs.getValueAbsolute(self.tdyPosition)
                tdyRealBodyHigh = self.__openDs.getValueAbsolute(self.tdyPosition)
                tdyRealBodylow = self.__closeDs.getValueAbsolute(self.tdyPosition)

            # assign yesterday body, bodyhigh, bodylow
            if self.__closeDs.getValueAbsolute(self.tdyPosition-1) > self.__openDs.getValueAbsolute(self.tdyPosition-1) :
                ystRealBody = self.__closeDs.getValueAbsolute(self.tdyPosition-1)-self.__openDs.getValueAbsolute(self.tdyPosition-1)
                ystRealBodyHigh = self.__closeDs.getValueAbsolute(self.tdyPosition-1)
                ystRealBodylow = self.__openDs.getValueAbsolute(self.tdyPosition-1)
            else :
                ystRealBody = self.__closeDs.getValueAbsolute(self.tdyPosition-1)-self.__openDs.getValueAbsolute(self.tdyPosition-1)
                ystRealBodyHigh = self.__openDs.getValueAbsolute(self.tdyPosition-1)
                ystRealBodylow = self.__closeDs.getValueAbsolute(self.tdyPosition-1)

            #assign the day before yesterday body, bodyhigh, bodylow
            if self.__closeDs.getValueAbsolute(self.tdyPosition-2) > self.__openDs.getValueAbsolute(self.tdyPosition-2) :
                preYstRealBody = self.__closeDs.getValueAbsolute(self.tdyPosition-2)-self.__openDs.getValueAbsolute(self.tdyPosition-2)
                preYstlBodyHigh = self.__closeDs.getValueAbsolute(self.tdyPosition-2)
                preYstRealBodylow = self.__openDs.getValueAbsolute(self.tdyPosition-2)
            else :
                preYstRealBody = self.__closeDs.getValueAbsolute(self.tdyPosition-2)-self.__openDs.getValueAbsolute(self.tdyPosition-2)
                preYstRealBodyHigh = self.__openDs.getValueAbsolute(self.tdyPosition-2)
                preYstRealBodylow = self.__closeDs.getValueAbsolute(self.tdyPosition-2)

            if preYstRealBody > 0 and ystRealBodylow>preYstlBodyHigh and tdyRealBodyHigh<ystRealBodylow \
                    and tdyRealBodylow<preYstlBodyHigh and tdyRealBody < 0 and abs(ystRealBody) <= 0.01 :
                return abs(tdyRealBodylow-preYstlBodyHigh)/preYstRealBody
            else :
                return 0
        else :
            return 0

    def isMorningStar(self) :
        if self.tdyPosition > 2 :
            # assign today body, bodyhigh, bodylow
            if self.__closeDs.getValueAbsolute(self.tdyPosition) > self.__openDs.getValueAbsolute(self.tdyPosition) :
                tdyRealBody = self.__closeDs.getValueAbsolute(self.tdyPosition)-self.__openDs.getValueAbsolute(self.tdyPosition)
                tdyRealBodyHigh = self.__closeDs.getValueAbsolute(self.tdyPosition)
                tdyRealBodylow = self.__openDs.getValueAbsolute(self.tdyPosition)
            else :
                tdyRealBody = self.__closeDs.getValueAbsolute(self.tdyPosition)-self.__openDs.getValueAbsolute(self.tdyPosition)
                tdyRealBodyHigh = self.__openDs.getValueAbsolute(self.tdyPosition)
                tdyRealBodylow = self.__closeDs.getValueAbsolute(self.tdyPosition)

            # assign yesterday body, bodyhigh, bodylow
            if self.__closeDs.getValueAbsolute(self.tdyPosition-1) > self.__openDs.getValueAbsolute(self.tdyPosition-1) :
                ystRealBody = self.__closeDs.getValueAbsolute(self.tdyPosition-1)-self.__openDs.getValueAbsolute(self.tdyPosition-1)
                ystRealBodyHigh = self.__closeDs.getValueAbsolute(self.tdyPosition-1)
                ystRealBodylow = self.__openDs.getValueAbsolute(self.tdyPosition-1)
            else :
                ystRealBody = self.__closeDs.getValueAbsolute(self.tdyPosition-1)-self.__openDs.getValueAbsolute(self.tdyPosition-1)
                ystRealBodyHigh = self.__openDs.getValueAbsolute(self.tdyPosition-1)
                ystRealBodylow = self.__closeDs.getValueAbsolute(self.tdyPosition-1)

            #assign the day before yesterday body, bodyhigh, bodylow
            if self.__closeDs.getValueAbsolute(self.tdyPosition-2) > self.__openDs.getValueAbsolute(self.tdyPosition-2) :
                preYstRealBody = self.__closeDs.getValueAbsolute(self.tdyPosition-2)-self.__openDs.getValueAbsolute(self.tdyPosition-2)
                preYstRealBodyHigh = self.__closeDs.getValueAbsolute(self.tdyPosition-2)
                preYstRealBodylow = self.__openDs.getValueAbsolute(self.tdyPosition-2)
            else :
                preYstRealBody = self.__closeDs.getValueAbsolute(self.tdyPosition-2)-self.__openDs.getValueAbsolute(self.tdyPosition-2)
                preYstRealBodyHigh = self.__openDs.getValueAbsolute(self.tdyPosition-2)
                preYstRealBodylow = self.__closeDs.getValueAbsolute(self.tdyPosition-2)

            if preYstRealBody < 0 and ystRealBodyHigh < preYstRealBodylow and tdyRealBodylow>ystRealBodyHigh \
                    and tdyRealBodyHigh > preYstRealBodylow and tdyRealBody > 0:
                return abs(tdyRealBodyHigh-preYstRealBodylow)/abs(preYstRealBody)
            else :
                return 0
        else :
            return 0


    def isDojiMorningStar(self) :
        if self.tdyPosition > 2 :
            # assign today body, bodyhigh, bodylow
            if self.__closeDs.getValueAbsolute(self.tdyPosition) > self.__openDs.getValueAbsolute(self.tdyPosition) :
                tdyRealBody = self.__closeDs.getValueAbsolute(self.tdyPosition)-self.__openDs.getValueAbsolute(self.tdyPosition)
                tdyRealBodyHigh = self.__closeDs.getValueAbsolute(self.tdyPosition)
                tdyRealBodylow = self.__openDs.getValueAbsolute(self.tdyPosition)
            else :
                tdyRealBody = self.__closeDs.getValueAbsolute(self.tdyPosition)-self.__openDs.getValueAbsolute(self.tdyPosition)
                tdyRealBodyHigh = self.__openDs.getValueAbsolute(self.tdyPosition)
                tdyRealBodylow = self.__closeDs.getValueAbsolute(self.tdyPosition)

            # assign yesterday body, bodyhigh, bodylow
            if self.__closeDs.getValueAbsolute(self.tdyPosition-1) > self.__openDs.getValueAbsolute(self.tdyPosition-1) :
                ystRealBody = self.__closeDs.getValueAbsolute(self.tdyPosition-1)-self.__openDs.getValueAbsolute(self.tdyPosition-1)
                ystRealBodyHigh = self.__closeDs.getValueAbsolute(self.tdyPosition-1)
                ystRealBodylow = self.__openDs.getValueAbsolute(self.tdyPosition-1)
            else :
                ystRealBody = self.__closeDs.getValueAbsolute(self.tdyPosition-1)-self.__openDs.getValueAbsolute(self.tdyPosition-1)
                ystRealBodyHigh = self.__openDs.getValueAbsolute(self.tdyPosition-1)
                ystRealBodylow = self.__closeDs.getValueAbsolute(self.tdyPosition-1)

            #assign the day before yesterday body, bodyhigh, bodylow
            if self.__closeDs.getValueAbsolute(self.tdyPosition-2) > self.__openDs.getValueAbsolute(self.tdyPosition-2) :
                preYstRealBody = self.__closeDs.getValueAbsolute(self.tdyPosition-2)-self.__openDs.getValueAbsolute(self.tdyPosition-2)
                preYstRealBodyHigh = self.__closeDs.getValueAbsolute(self.tdyPosition-2)
                preYstRealBodylow = self.__openDs.getValueAbsolute(self.tdyPosition-2)
            else :
                preYstRealBody = self.__closeDs.getValueAbsolute(self.tdyPosition-2)-self.__openDs.getValueAbsolute(self.tdyPosition-2)
                preYstRealBodyHigh = self.__openDs.getValueAbsolute(self.tdyPosition-2)
                preYstRealBodylow = self.__closeDs.getValueAbsolute(self.tdyPosition-2)

            if preYstRealBody < 0 and ystRealBodyHigh < preYstRealBodylow and tdyRealBodylow>ystRealBodyHigh \
                    and tdyRealBodyHigh > preYstRealBodylow and tdyRealBody > 0 and ystRealBody < 0.01 :
                return abs(tdyRealBodyHigh-preYstRealBodylow)/abs(preYstRealBody)
            else :
                return 0
        else :
            return 0


    def isDoji(self) :
        tdyRealBody = self.__openDs.getValueAbsolute(self.tdyPosition)-self.__closeDs.getValueAbsolute(self.tdyPosition)

        if abs(tdyRealBody) <= 0.01:
            return 1
        else :
            return 0

    def isHarami(self) :

        # assign today body, bodyhigh, bodylow
        if self.__closeDs.getValueAbsolute(self.tdyPosition) > self.__openDs.getValueAbsolute(self.tdyPosition) :
            tdyRealBody = self.__closeDs.getValueAbsolute(self.tdyPosition)-self.__openDs.getValueAbsolute(self.tdyPosition)
            tdyRealBodyHigh = self.__closeDs.getValueAbsolute(self.tdyPosition)
            tdyRealBodylow = self.__openDs.getValueAbsolute(self.tdyPosition)
        else :
            tdyRealBody = self.__closeDs.getValueAbsolute(self.tdyPosition)-self.__openDs.getValueAbsolute(self.tdyPosition)
            tdyRealBodyHigh = self.__openDs.getValueAbsolute(self.tdyPosition)
            tdyRealBodylow = self.__closeDs.getValueAbsolute(self.tdyPosition)

        if self.tdyPosition > 1 :
            # assign yesterday body, bodyhigh, bodylow
            if self.__closeDs.getValueAbsolute(self.tdyPosition-1) > self.__openDs.getValueAbsolute(self.tdyPosition-1) :
                ystRealBody = self.__closeDs.getValueAbsolute(self.tdyPosition-1)-self.__openDs.getValueAbsolute(self.tdyPosition-1)
                ystRealBodyHigh = self.__closeDs.getValueAbsolute(self.tdyPosition-1)
                ystRealBodylow = self.__openDs.getValueAbsolute(self.tdyPosition-1)
            else :
                ystRealBody = self.__closeDs.getValueAbsolute(self.tdyPosition-1)-self.__openDs.getValueAbsolute(self.tdyPosition-1)
                ystRealBodyHigh = self.__openDs.getValueAbsolute(self.tdyPosition-1)
                ystRealBodylow = self.__closeDs.getValueAbsolute(self.tdyPosition-1)

            if tdyRealBody <>0 and ystRealBody <>0 and tdyRealBody/ystRealBody<0 \
            and tdyRealBodyHigh < ystRealBodyHigh and tdyRealBodylow > ystRealBodylow :
                return 1
            else :
                return 0

        return 0

    def isHaramiCross(self) :

        # assign today body, bodyhigh, bodylow
        if self.__closeDs.getValueAbsolute(self.tdyPosition) > self.__openDs.getValueAbsolute(self.tdyPosition) :
            tdyRealBody = self.__closeDs.getValueAbsolute(self.tdyPosition)-self.__openDs.getValueAbsolute(self.tdyPosition)
            tdyRealBodyHigh = self.__closeDs.getValueAbsolute(self.tdyPosition)
            tdyRealBodylow = self.__openDs.getValueAbsolute(self.tdyPosition)
        else :
            tdyRealBody = self.__closeDs.getValueAbsolute(self.tdyPosition)-self.__openDs.getValueAbsolute(self.tdyPosition)
            tdyRealBodyHigh = self.__openDs.getValueAbsolute(self.tdyPosition)
            tdyRealBodylow = self.__closeDs.getValueAbsolute(self.tdyPosition)

        if self.tdyPosition > 1 :
            # assign yesterday body, bodyhigh, bodylow
            if self.__closeDs.getValueAbsolute(self.tdyPosition-1) > self.__openDs.getValueAbsolute(self.tdyPosition-1) :
                ystRealBody = self.__closeDs.getValueAbsolute(self.tdyPosition-1)-self.__openDs.getValueAbsolute(self.tdyPosition-1)
                ystRealBodyHigh = self.__closeDs.getValueAbsolute(self.tdyPosition-1)
                ystRealBodylow = self.__openDs.getValueAbsolute(self.tdyPosition-1)
            else :
                ystRealBody = self.__closeDs.getValueAbsolute(self.tdyPosition-1)-self.__openDs.getValueAbsolute(self.tdyPosition-1)
                ystRealBodyHigh = self.__openDs.getValueAbsolute(self.tdyPosition-1)
                ystRealBodylow = self.__closeDs.getValueAbsolute(self.tdyPosition-1)

            if tdyRealBody == 0  and ystRealBody <>0  \
            and tdyRealBodyHigh < ystRealBodyHigh and tdyRealBodylow > ystRealBodylow :
                return 1
            else :
                return 0

        return 0

    def isPositiveBeltHold(self) :
        tdyRealBody = self.__closeDs.getValueAbsolute(self.tdyPosition)-self.__openDs.getValueAbsolute(self.tdyPosition)

        if self.__openDs.getValueAbsolute(self.tdyPosition) > self.__closeDs.getValueAbsolute(self.tdyPosition) :
            tdyLowerShadow = self.__closeDs.getValueAbsolute(self.tdyPosition)-self.__lowDs.getValueAbsolute(self.tdyPosition)
            tdyUpperShadow = self.__highDs.getValueAbsolute(self.tdyPosition)-self.__openDs.getValueAbsolute(self.tdyPosition)
        else :
            tdyLowerShadow = self.__openDs.getValueAbsolute(self.tdyPosition)-self.__lowDs.getValueAbsolute(self.tdyPosition)
            tdyUpperShadow = self.__highDs.getValueAbsolute(self.tdyPosition)-self.__closeDs.getValueAbsolute(self.tdyPosition)

        if tdyRealBody > 0 and tdyLowerShadow == 0 and abs(tdyRealBody)/self.__openDs.getValueAbsolute(self.tdyPosition) > 0.03 :
            return 1
        else :
            return 0

    def isNegativeBeltHold(self) :
        tdyRealBody = self.__closeDs.getValueAbsolute(self.tdyPosition)-self.__openDs.getValueAbsolute(self.tdyPosition)

        if self.__openDs.getValueAbsolute(self.tdyPosition) > self.__closeDs.getValueAbsolute(self.tdyPosition) :
            tdyLowerShadow = self.__closeDs.getValueAbsolute(self.tdyPosition)-self.__lowDs.getValueAbsolute(self.tdyPosition)
            tdyUpperShadow = self.__highDs.getValueAbsolute(self.tdyPosition)-self.__openDs.getValueAbsolute(self.tdyPosition)
        else :
            tdyLowerShadow = self.__openDs.getValueAbsolute(self.tdyPosition)-self.__lowDs.getValueAbsolute(self.tdyPosition)
            tdyUpperShadow = self.__highDs.getValueAbsolute(self.tdyPosition)-self.__closeDs.getValueAbsolute(self.tdyPosition)

        if tdyRealBody < 0 and tdyUpperShadow == 0 and abs(tdyRealBody)/self.__closeDs.getValueAbsolute(self.tdyPosition) > 0.03 :
            return 1
        else :
            return 0