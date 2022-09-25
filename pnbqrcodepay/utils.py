from datetime import datetime
import random
import logging
from time import time

logger = logging.getLogger(__name__)

class Utils:
    """
    This class contains the utilities which are common used in a modules
    """
    def getNowtime():
         now  = datetime.now()
         return now
    def getTimestampsStr():
        ## return the string format of a datetime, e.g. 2022 0723 113316 320973
        ## return lenght of 20 characters 
        now = Utils.getNowtime()
        timestampStr = str(now.strftime("%Y%m%d%H%M%S%f"))
        return timestampStr

    def getRandomCharacter(length):
        ## This function get the a string with specific length, and the elements are choosen from A-Z
        ## with random possibility
        randStr = "".join(list(map(chr,random.sample(range(97,123),length))))
        return randStr.upper()
        
       
    def getTxnRef(timestempStr,length):
        """
        @params: len is the total lenght of txn reference
        """
        timestampStr = timestempStr
        if len(timestampStr) > length:
            logger.error("length of timestamp sting is 20 characters which is larger than you specified, please check")
            raise
        txnCharsLen = length - 20
        txnChars = Utils.getRandomCharacter(txnCharsLen)
        txnRef = timestampStr + txnChars
        return txnRef




if __name__ == "__main__":
    print(Utils.getTxnRef(25))