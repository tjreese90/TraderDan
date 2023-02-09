"""
Pricing endpoint
"""


class Pricing:
    """Class holding pricing functions
    Pricing
        Docs: http://developer.oanda.com/rest-live-v20/pricing-ep/
    """

    def __init__(self, api):
        self._api = api

    def get_pricing(self, account_id, instruments, **kwargs):
        """Get pricing information for a specified list of Instruments within
        an Account.
        Args:
            account_id str: Account Identifier [required]
            instruments str: List of Instruments to get pricing for. [required]
            since dateTime: Date/Time filter to apply to the response.
                           Only prices and home conversions (if requested) with a time
                           later than this filter
            includeUnitsAvailable bol: Flag that enables the inclusion of the
                                       unitsAvailable field in the returned Price objects
            includeHomeConversions bol: Flag that enables the inclusion of the homeConversions
                                        field in the returned response
        Returns:
            A dict with pricing information.

        Raises:
            OandaError: An error occurred while requesting the OANDA API.
        """
        endpoint = 'accounts/{0}/pricing'.format(account_id)
        if not isinstance(instruments, list):
            instruments = [instruments]
        else:
            instruments = "%2C".join(instruments)

        params = {'instruments': instruments}

        qs_params = ('since', 'includeUnitsAvailable', 'includeHomeConversions')
        for qs in qs_params:
            if qs not in kwargs:
                continue
            # Add the ordered parameters
            params[qs] = kwargs.get(qs)

        return self._api.search(endpoint, params=params)

    def get_pricing_stream(self, account_id, instruments, **kwargs):
        """Get a stream of Account Prices starting from when the request is made.
        This pricing stream does not include every single price created for the Account,
        but instead will provide at most 4 prices per second (every 250 milliseconds)
        for each instrument being requested.
        Args:
            account_id str: Account Identifier [required]
            instruments str: List of Instruments to get pricing for. [required]
            since dateTime: Date/Time filter to apply to the response.
                           Only prices and home conversions (if requested) with a time
                           later than this filter
            snapshot bol: Flag that enables/disables the sending of a pricing snapshot
                          when initially connecting to the stream. [default=True]
        Returns:
            A dict with pricing information.

        Raises:
            OandaError: An error occurred while requesting the OANDA API.
        """
        endpoint = 'accounts/{}/pricing/stream'.format(account_id)

        if not isinstance(instruments, list):
            instruments = [instruments]
        else:
            instruments = "%2C".join(instruments)
        params = {'instruments': instruments}

        qs_params = ('since', 'includeUnitsAvailable', 'includeHomeConversions')
        for qs in qs_params:
            if qs not in kwargs:
                continue
            # Add the ordered parameters
            params[qs] = kwargs.get(qs)

        return self._api.search(endpoint, params=params, stream=True)
