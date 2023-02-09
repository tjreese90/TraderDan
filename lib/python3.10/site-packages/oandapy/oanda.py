from .api import (
    Core, Account, Instrument, Orders, Positions, Pricing, Trades, Transactions
)


class APIv20(Core):
    """Oanda REST API v20 Class

    This class instantiates all endpoint classes

    """
    def __init__(self, environment="practice", access_token=None, timeout=3):
        """APIv20 object to communicate with Oanda REST API.

        Args:
            environment (str, optional): Provides the environment for
                OANDA's API. Defaults to 'practice'.
            access_token (str): Specifies the access token.

        """
        super().__init__(environment, access_token, timeout)

        self.account = Account(self)
        self.orders = Orders(self)
        self.positions = Positions(self)
        self.pricing = Pricing(self)
        self.trades = Trades(self)
        self.transactions = Transactions(self)
        self.instrument = Instrument(self)
