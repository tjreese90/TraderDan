"""
Trades endpoint
"""
API_PARAMS = {
    'before_id': 'beforeID',
    'take_profit': 'takeProfit',
    'stop_loss': 'stopLoss',
    'trailing_stoploss': 'trailingStopLoss'
}


class Trades:
    """Class holding trades functions
    Trades
        Docs: http://developer.oanda.com/rest-live-v20/trades-ep/
    """

    def __init__(self, api):
        self._api = api

    def get_trades(self, account_id, **kwargs):
        """Get a list of all Accounts authorized for the provided token.
        Get a list of Trades for an Account

        Args:
            account_id (str): Account Identifier [required]
            ids (str, list): List of Trade IDs to retrieve.
        Kwargs:
            state: The state to filter the requested Trades by. [default=OPEN]
            instrument (str): The instrument to filter the requested Trades by.
            count (int): The maximum number of Trades to return. [default=50, maximum=500]
            before_id (str): The maximum Trade ID to return.
                            If not provided the most recent Trades in the Account are returned.
        Returns:
            OANDAResponseFactory with the list of Trades requested
        Raises:
            OandaError: An error occurred while requesting the OANDA API.
        """
        endpoint = 'accounts/{0}/trades'.format(account_id)
        qs_params = ('ids', 'state', 'instrument', 'count', 'before_id')
        params = {}
        for qs in qs_params:
            if qs not in kwargs:
                continue

            param = API_PARAMS.get(qs, qs)
            # Add the ordered parameters
            params[param] = kwargs.get(qs)

        return self._api.search(endpoint, params=params)

    def get_open_trades(self, account_id):
        """Get the list of open Trades for an Account
        Args:
            account_id (str): Account Identifier [required]
        Returns:
            OANDAResponseFactory with the Account’s list of open Trades is provided
        Raises:
            OandaError: An error occurred while requesting the OANDA API.
        """
        endpoint = 'accounts/{0}/openTrades'.format(account_id)
        return self._api.search(endpoint)

    def get_trade_details(self, account_id, trade_id):
        """Get the details of a specific Trade in an Account
        Args:
            account_id (str): Account Identifier [required]
            trade_id (str): Specifier for the Trade [required]
        Returns:
            OANDAResponseFactory with the details for the requested Trade is provided

        Raises:
            OandaError: An error occurred while requesting the OANDA API.
        """
        endpoint = 'accounts/{0}/trades/{1}'.format(account_id, trade_id)
        return self._api.search(endpoint)

    def close_trade(self, account_id, trade_id, units):
        """Close (partially or fully) a specific open Trade in an Account
        Args:
            account_id (str): Account Identifier [required]
            trade_id (str): Specifier for the Trade [required]
            units: Indication of how much of the Trade to close. ALL to close all.
        Returns:
            OANDAResponseFactory with the Trade has been closed as requested
        Raises:
            OandaError: An error occurred while requesting the OANDA API.
        """
        endpoint = 'accounts/{0}/trades/{1}/close'.format(account_id, trade_id)

        data = {"units": units}
        return self._api.update(endpoint, data=data)

    def update_client_extensions(self, account_id, trade_id, client_extensions):
        """Update the Client Extensions for a Trade.
        Do not add, update, or delete the Client Extensions
        if your account is associated with MT4.

        Args:
            account_id (str): Account Identifier [required]
            trade_id (str): Specifier for the Trade [required]
            client_extensions (dict): The Client Extensions to update the Trade with.
        Returns:
            OANDAResponseFactory with the Trade has been closed as requested
        Raises:
            OandaError: An error occurred while requesting the OANDA API.
        """
        endpoint = 'accounts/{0}/trades/{1}/clientExtensions'.format(account_id,
                                                                     trade_id)
        data = {"clientExtensions": client_extensions}
        return self._api.update(endpoint, data=data)

    def update_trade(self, account_id, trade_id, **kwargs):
        """Create, replace and cancel a Trade’s dependent Orders
        (Take Profit, Stop Loss and Trailing Stop Loss) through the Trade itself

        Args:
            account_id (str): Account Identifier [required]
            trade_id (str): Specifier for the Trade [required]
        Kwargs:
            take_profit (dict): The specification of the Take Profit to create/modify/cancel
            stop_loss (dict): The specification of the Stop Loss to create/modify/cancel.
            trailing_stop_loss (dict): The specification of the Trailing Stop Loss to create/modify/cancel
        Returns:
            OANDAResponseFactory with the Trade has been closed as requested
        Raises:
            OandaError: An error occurred while requesting the OANDA API.
        """
        endpoint = 'accounts/{0}/trades/{1}/orders'.format(account_id, trade_id)
        data = {}
        qs_params = ('take_profit', 'stop_loss', 'trailing_stop_loss')
        for qs in qs_params:
            if qs not in kwargs:
                continue

            param = API_PARAMS.get(qs, qs)
            # Add the ordered parameters
            data[param] = kwargs.get(qs)

        return self._api.update(endpoint, data=data)
