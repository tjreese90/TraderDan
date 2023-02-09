"""
Orders endpoint
"""


class Orders:
    """Class holding orders functions
    Orders
        Docs: http://developer.oanda.com/rest-live-v20/orders-ep/
    """

    def __init__(self, api):
        self._api = api

    def create_order(self, account_id, order):
        """Get a list of all Accounts authorized for the provided token.
        Create an order for an Account

        Args:
            account_id str: Account Identifier [required]
            order dict: Order specification to create a order

        Returns:
            OANDAFactoryResponse: A object with instrument information.OANDAResponseFactory with order data.

        Raises:
            OandaError: An error occurred while requesting the OANDA API.
        """
        endpoint = 'accounts/{0}/orders'.format(account_id)
        data = {'order': order}
        return self._api.create(endpoint, data=data)

    def get_orders_list(self, account_id, ids, state=None, instrument=None,
                        count=None, before_id=None):
        """Get a list of all Accounts authorized for the provided token.
        Get a list of Orders for an Account
        Args:
            This function takes no arguments.
        Returns:
            OANDAFactoryResponse: A object with instrument information.OANDAResponseFactory with order data.
        Raises:
            OandaError: An error occurred while requesting the OANDA API.
        """
        endpoint = 'accounts/{0}/orders'.format(account_id)
        ids = "%2C".join(ids)
        params = {"ids": ids}

        if state:
            params["state"] = state

        if instrument:
            params["instrument"] = instrument

        if count:
            params["count"] = count

        if before_id:
            params["beforeID"] = before_id

        return self._api.search(endpoint, params=params)

    def get_pending_orders(self, account_id):
        """Get a list of all Accounts authorized for the provided token.
        List all pending Orders in an Account
        Args:
            This function takes no arguments.
        Returns:
            OANDAFactoryResponse: A object with instrument information.OANDAResponseFactory with order data.
        Raises:
            OandaError: An error occurred while requesting the OANDA API.
        """
        endpoint = 'accounts/{0}/pendingOrders'.format(account_id)
        return self._api.search(endpoint)

    def get_order_details(self, account_id, order_id):
        """Get a list of all Accounts authorized for the provided token.
        Get details for a single Order in an Account
        Args:
            This function takes no arguments.
        Returns:
            OANDAResponseFactory with order data.
        Raises:
            OandaError: An error occurred while requesting the OANDA API.
        """
        endpoint = 'accounts/{0}/orders/{1}'.format(account_id, order_id)
        return self._api.search(endpoint)

    def replace_order(self, account_id, order_id, order):
        """Get a list of all Accounts authorized for the provided token.
        Replace an Order in an Account by simultaneously cancelling it and
        creating a replacement Order
        Args:
            This function takes no arguments.
        Returns:
            OANDAResponseFactory with order data.
        Raises:
            OandaError: An error occurred while requesting the OANDA API.
        """
        endpoint = 'accounts/{0}/orders/{1}'.format(account_id, order_id)
        data = {'order': order}
        return self._api.update(endpoint, data=data)

    def cancel_pending_order(self, account_id, order_id):
        """Get a list of all Accounts authorized for the provided token.
        Cancel a pending Order in an Account
        Args:
            This function takes no arguments.
        Returns:
            OANDAResponseFactory with order data.
        Raises:
            OandaError: An error occurred while requesting the OANDA API.
        """
        endpoint = 'accounts/{}/orders/{}/cancel'.format(account_id, order_id)
        return self._api.update(endpoint, data={})

    def update_client_extensions(self, account_id, order_id, comment):
        """Update the Client Extensions for an Order in an Account.
        Do not set, modify, or delete clientExtensions if your account is associated with MT4.
        Args:
            This function takes no arguments.
        Returns:
            OANDAResponseFactory with order data.
        Raises:
            OandaError: An error occurred while requesting the OANDA API.
        """
        endpoint = 'accounts/{}/orders/{}/clientExtensions'.format(account_id, order_id)
        data = {
            "clientExtensions": {
                "comment": comment
            }
        }
        return self._api.update(endpoint, data=data)
