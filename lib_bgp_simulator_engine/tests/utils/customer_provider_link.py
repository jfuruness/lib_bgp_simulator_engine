class CustomerProviderLink:
    """Customer provider link for unit tests

    Without this provider and customer order are easily swapped
    """

    # Kwargs is used here to prevent args to avoid out of order problems
    def __init__(self, **kwargs):
        self.customer = kwargs["customer"]
        self.provider = kwargs["provider"]
