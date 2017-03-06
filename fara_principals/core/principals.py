from fara_principals.exceptions import (
    BadPrincipalSchemaError
)

class ForeignPrincipal:

    def __init_(self, url=None, country=None, state=None, address=None, 
        reg_number=None, principal_name=None, principal_reg_date=None, 
        reg_date=None, registrant=None, exhibits=[], partial_data=None, 
        *args, **kwargs):

        self._dict_info = None
        if partial_data:
            self._dict_info = partial_data
        else:
            self._dict_info = {
                "url": url, "country_name": country, "state": state, 
                "address": address, "reg_number": reg_number, 
                "principal_name": principal_name, 
                "principal_reg_date": principal_reg_date, 
                "reg_date": reg_date, "exhibits": exhibits
            }

    def validate_data(self):
        """
        Confirms that certain keys are present in the dict returned by 
        `self.to_dict`

        Raises:
            BadPrincipalSchemaError: raised when certain fields(keys) are 
            unavailable or when required contrains on the schema are not met.

        Note: this method is to be called when it has been populated with 
        it's exhibit info.
        """
        pass

    def validate_partial(self):
        """
        Confirms that certain keys are present given that this instance 
        represents a pricipal whose full data has not yet been collected.

        Raises:
            BadPrincipalSchemaError: raised when certain fields(keys) are 
            unavailable or when required contrains on the schema are not met.
        """
        pass

    def partial_dict(self):
        """
        Returns:
            dict: a dict representation of the principal without it's
            exhibit data.
        """
        pass

    def is_partial(self):
        """
        Returns:
            bool: True if the principal this instance represents does not
            yet contain all it's information including it's exibit data.

        Note: a principal is usually still partial when it has been 
        populate from the list page but not from its detail page.
        """
        pass

    def to_dict(self):
        """
        Returns:
            dict: a dict representation of the Principal instance
        """
        pass

    def to_json(self):
        """
        Returns:
            str: a json string representation of the Principal instance
        """
        pass

    def add_exhibit_dict(self, exibit):
        """
        Args:
            exhibit(dict): dict containing exhibit info
        """
        pass