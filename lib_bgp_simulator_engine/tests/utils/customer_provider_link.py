class CustomerProviderLink:
    """Customer provider link for unit tests

    Without this provider and customer order are easily swapped
    """

    def __init__(self, customer=None, provider=None):
        self.customer = customer
        self.provider = provider
        assert all([customer, provider])
