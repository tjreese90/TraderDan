"""
Positions endpoints
"""


class Positions:
    """Class holding positions functions
    Positions
        Docs: http://developer.oanda.com/rest-live-v20/positions-ep/
    """
    def __init__(self, api):
        self._api = api

    def get_positions(self, account_id):
        """Get a List all Positions for an Account.
        The Positions returned are for every instrument
        that has had a position during the lifetime of an the Account.
        Args:
            account_id str: Account Identifier [required]
        Returns:
            A response factory with the Account’s Positions are provided.
        Raises:
            OandaError: An error occurred while requesting the OANDA API.
        """
        endpoint = 'accounts/{0}/positions'.format(account_id)
        return self._api.search(endpoint)

    def get_open_positions(self, account_id):
        """Get a List List all open Positions for an Account.
        An open Position is a Position in an Account that
        currently has a Trade opened for it..
        Args:
            account_id str: Account Identifier [required]
        Returns:
            A response factory with the Account’s Positions are provided.
        Raises:
            OandaError: An error occurred while requesting the OANDA API.
        """
        endpoint = 'accounts/{0}/openPositions'.format(account_id)
        return self._api.search(endpoint)

    def get_position_details(self, account_id, instrument):
        """Get Get the details of a single Instrument’s Position in an Account.
        The Position may by open or not.
        Args:
            account_id str: Account Identifier [required]
            instrument str: Name of the Instrument [required
        Returns:
            A response factory with the Account’s Positions are provided.
        Raises:
            OandaError: An error occurred while requesting the OANDA API.
        """
        endpoint = 'accounts/{0}/positions/{1}'.format(account_id, instrument)
        return self._api.search(endpoint)

    def close_position(self, account_id, instrument, long_units,
                       long_client_extensions, short_units,
                       short_client_extensions):
        """Closeout the open Position for a specific instrument in an Account.
        Args:
            This function takes no arguments.
        Returns:
            A response factory with the Account’s Positions are provided.
        Raises:
            OandaError: An error occurred while requesting the OANDA API.
        """
        endpoint = 'accounts/{0}/positions/{1}/close'.format(account_id, instrument)

        data = {}
        if long_units:
            data["longUnits"] = long_units

        if short_client_extensions:
            data["longClientExtensions"] = long_client_extensions

        if short_units:
            data["shortUnits"] = short_units

        if long_client_extensions:
            data["longClientExtensions"] = long_client_extensions

        return self._api.update(endpoint, data=data)
