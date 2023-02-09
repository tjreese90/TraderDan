"""
Instruments endpoint
"""
API_DATE_ARGS = {
    'from_date': 'from',
    'to_date': 'to',
}


class Instrument:
    """Class holding instruments functions
    Instrument
        Docs: http://developer.oanda.com/rest-live-v20/instrument-ep/
    """

    def __init__(self, api):
        self._api = api

    def get_candles(self, instrument, **kwargs):
        """Fetch a Candlestick data for a instrument.

        Args:
            instrument:	Name of the Instrument [required]

        optional:
            price:	The Price component(s) to get candlestick data for.
                    Can contain any combination of the characters “M” (midpoint candles)
                    “B” (bid candles) and “A” (ask candles). [default=M]
            granularity: The granularity of the candlesticks to fetch [default=S5]
            count: The number of candlesticks to return in the response.
                  Count should not be specified if both the start and end parameters are
                  provided, as the time range combined with the granularity will determine
                  the number of candlesticks to return. [default=500, maximum=5000]
            from_date: The start of the time range to fetch candlesticks for.
            to_date: The end of the time range to fetch candlesticks for.
            smooth:	A flag that controls whether the candlestick is “smoothed” or not.
                    A smoothed candlestick uses the previous candle’s close price as its open price,
                    while an unsmoothed candlestick uses the first price from its
                    time range as its open price. [default=False]
            includeFirst: A flag that controls whether the candlestick that is covered by
                         the from time should be included in the results.
                         This flag enables clients to use the timestamp of the last
                         completed candlestick received to poll for future candlesticks
                         but avoid receiving the previous candlestick repeatedly. [default=True]
            dailyAlignment: The hour of the day (in the specified timezone) to use
                            for granularities that have daily alignments. [default=17, minimum=0, maximum=23]
            alignmentTimezone: The timezone to use for the dailyAlignment parameter.
                              Candlesticks with daily alignment will be aligned to the dailyAlignment
                              hour within the alignmentTimezone. Note that the returned times will
                              still be represented in UTC. [default=America/New_York]
            weeklyAlignment: The day of the week used for granularities that have weekly alignment. [default=Friday]


        Returns:
            OANDAFactoryResponse: A object with instrument information.

        Raises:
            OandaError: An error occurred while requesting the OANDA API.
        """
        endpoint = 'instruments/{0}/candles'.format(instrument)
        qs_params = (
            'price', 'granularity', 'count', 'to_date', 'from_date',
            'smooth', 'includeFirst', 'dailyAlignment', 'alignmentTimezone',
            'weeklyAlignment',
        )
        params = {}
        for qs in qs_params:
            if qs not in kwargs:
                continue

            # Change the dates params
            param = API_DATE_ARGS.get(qs, qs)
            # Add the ordered parameters
            params[param] = kwargs.get(qs)

        return self._api.search(endpoint, params=params)

    def get_orderbook(self, instrument, **kwargs):
        """Fetch a OrderBook for an instrument.
        Args:
            instrument:	Name of the Instrument [required]
        optional:
            time: The time of the snapshot to fetch.
                  If not specified, then the most recent snapshot is fetched.
        Returns:
            OANDAFactoryResponse: A object with instrument information.
        Raises:
            OandaError: An error occurred while requesting the OANDA API.
        """
        endpoint = 'instruments/{0}/orderBook'.format(instrument)

        params = {}
        if 'time' in kwargs:
            params['time'] = kwargs.get('time')

        return self._api.search(endpoint, params=params)

    def get_positionbook(self, instrument, **kwargs):
        """Fetch a position book for an instrument.
        Args:
            instrument:	Name of the Instrument [required]
        optional:
            time: The time of the snapshot to fetch.
                  If not specified, then the most recent snapshot is fetched.
        Returns:
            OANDAFactoryResponse: A object with instrument information.
        Raises:
            OandaError: An error occurred while requesting the OANDA API.
        """
        endpoint = 'instruments/{0}/positionBook'.format(instrument)

        params = {}
        if 'time' in kwargs:
            params['time'] = kwargs.get('time')

        return self._api.search(endpoint, params=params)
