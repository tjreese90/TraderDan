"""
Transactions endpoint
"""
API_PARAMS = {
    'from_date': 'from',
    'to_date': 'to',
    'page_size': 'pageSize',
    'type_list': 'type',
}


class Transactions:
    """Class holding transactions functions

    Transactions
        Docs: http://developer.oanda.com/rest-live-v20/transactions-ep/
    """

    def __init__(self, api):
        self._api = api

    def get_transactions(self, account_id, **kwargs):
        """Get a list of Transactions pages that satisfy a time-based Transaction query.
        Args:
            account_id (str): Account Identifier [required]
        Kwargs:
            from_date (DateTime): The starting time (inclusive) of the time range
                                  for the Transactions being queried. [default=Account Creation Time]
            to_date (DateTime): The ending time (inclusive) of the time range for the
                                Transactions being queried. [default=Request Time]
            page_size (int): The number of Transactions to include in each page of the results.
                            [default=100, maximum=1000]
            type_list (list): A filter for restricting the types of Transactions to retrieve.

        Returns:
            OANDAResponseFactory with the requested time range of Transaction pages are provided.
        Raises:
            OandaError: An error occurred while requesting the OANDA API.
        """
        endpoint = 'accounts/{0}/transactions'.format(account_id)

        params = {}
        qs_params = ('from_date', 'to_date', 'page_size', 'type_list')
        for qs in qs_params:
            if qs not in kwargs:
                continue

            param = API_PARAMS.get(qs, qs)

            if qs == 'type_list':
                if not isinstance(qs, list):
                    qs = [qs]
                else:
                    qs = "%2C".join(qs)

            # Add the ordered parameters
            params[param] = kwargs.get(qs)

        return self._api.search(endpoint, params=params)

    def get_transaction_details(self, account_id, transaction_id):
        """Get the details of a single Account Transaction.
        Args:
            account_id (str):	Account Identifier [required]
            transaction_id (str): A Transaction ID [required]
        Returns:
            OANDAResponseFactory with the details of the requested Transaction are provided.
        Raises:
            OandaError: An error occurred while requesting the OANDA API.
        """
        endpoint = 'accounts/{0}/transactions{1}'.format(account_id,
                                                         transaction_id)

        return self._api.search(endpoint)

    def get_transaction_idrange(self, account_id, **kwargs):
        """Get a range of Transactions for an Account based on the Transaction IDs.
        Args:
            account_id (str): Account Identifier [required]
        Kwargs:
            from_date (DateTime): The starting time (inclusive) of the time range
                                  for the Transactions being queried. [default=Account Creation Time]
            to_date (DateTime): The ending time (inclusive) of the time range for the
                                Transactions being queried. [default=Request Time]
            type_list (list): A filter for restricting the types of Transactions to retrieve.


        Returns:
            OANDAResponseFactory with the requested time range of Transactions are provided.
        Raises:
            OandaError: An error occurred while requesting the OANDA API.
        """
        endpoint = 'accounts/{0}/transactions/idrange'.format(account_id)

        params = {}
        qs_params = ('from_date', 'to_date', 'type_list')
        for qs in qs_params:
            if qs not in kwargs:
                continue

            param = API_PARAMS.get(qs, qs)

            if qs == 'type_list':
                if not isinstance(qs, list):
                    qs = [qs]
                else:
                    qs = "%2C".join(qs)

            # Add the ordered parameters
            params[param] = kwargs.get(qs)

        return self._api.search(endpoint, params=params)

    def get_transaction_sinceid(self, account_id, last_transaction_id):
        """Get a range of Transactions for an Account starting at (but not
        including) a provided Transaction ID.
        Args:
            account_id (str): Account Identifier [required]
            last_transaction_id (str): The ID of the last Transaction fetched.
                                       This query will return all Transactions newer
                                       than the TransactionID. [required]
        Returns:
            OANDAResponseFactory with the requested time range of Transactions are provided.
        Raises:
            OandaError: An error occurred while requesting the OANDA API.
        """
        endpoint = 'accounts/{0}/transactions/sinceid'.format(account_id)

        params = {"id": last_transaction_id}
        return self._api.search(endpoint, params=params)

    def get_transaction_stream(self, account_id):
        """Get a stream of Transactions for an Account starting from when the request is made.
        Args:
            account_id (str): Account Identifier [required]
        Returns:
            Connecting to the Transaction Stream was successful.
        Raises:
            OandaError: An error occurred while requesting the OANDA API.
        """
        endpoint = 'accounts/{0}/transactions/stream'.format(account_id)
        return self._api.search(endpoint, stream=True)
