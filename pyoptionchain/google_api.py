import requests
import demjson

class GoogleFinanceOption(object):

    API_URL = "https://www.google.com/finance/option_chain"
    DEFAULT_EXCHANGE = "NASDAQ"
    DEFAULT_EXCHANGE_SYMBOL = "AAPL" #Apple Inc
    DEFAULT_VALID_EXCHANGE = [DEFAULT_EXCHANGE]
    DEFAULT_VALID_EXCHANGE_SYMBOL = [DEFAULT_EXCHANGE_SYMBOL]

    def __init__(self, *args, **kwargs):

        self.__getData = {
            "q" : "%s:%s" % (GoogleFinanceOption.DEFAULT_EXCHANGE, GoogleFinanceOption.DEFAULT_EXCHANGE_SYMBOL),
            "output" : "json"
        }

        self.__expirations = []
        self.__puts = []
        self.__calls = []
        self.__expiry = {}

        self.setParameters(kwargs.get("params"))

    def setParameters(self, params = {}):

        if isinstance(params, dict):
            if len(params) > 0:
                self.__getData.update(params)

                return True

        return False

    def fetchData(self):

        response = requests.get(GoogleFinanceOption.API_URL, params=self.__getData)
        fetchedData = ""
        decodedJson = {}

        if response.status_code == 200:

            for line in response.iter_lines():
                fetchedData += line

            try:
                decodedJson = demjson.decode(fetchedData)
                self.__expirations = decodedJson.get("expirations", [])
                self.__puts = decodedJson.get("puts", [])
                self.__calls = decodedJson.get("calls", [])
                self.__expiry = decodedJson.get("expiry", {})
                return True
            except:
                pass

        return False

    def getExpirations(self):

        return self.__expirations

    def getPuts(self):

        return self.__puts

    def getCalls(self):

        return self.__calls

    def getExpiry(self):

        return self.__expiry

