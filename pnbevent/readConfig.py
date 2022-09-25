from calendar import c
from configparser import ConfigParser, Error
import logging


logger = logging.getLogger(__name__)

class Config:
     def __init__(self,configFile,sectionStr):
        """
        :param configFile: config file path.
        :param section: choose the section to be loaded
        """
        config = ConfigParser() 
        try: 
            config.read(configFile, encoding='UTF-8')
            section = config[sectionStr]
           
        except KeyError:
            logger.error(
                "Couldn't get the environment configs %s from the %s",
                section, configFile)
            raise
        try:
            self.clientId = section['client_Id']
            self.clientSecret = section['client_Secret']
            self.merchantId = section['merchant_Id']
            self.genaratePaymentQrcode = section['qrcode_url_dev']
            self.notifyUrl = section['notifyUrl']

            self.paymentMethod = section['payMethod']
            self.txnChannel = section['txnChannel']

            self.paymentCountry = section['country']
            self.currency = section['currency']

        except KeyError:
            logger.error(
                "Couldn't get the attribute values from the %s",
                section)
            raise




