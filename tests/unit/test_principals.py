from unittest import TestCase

from fara_principals.core.principals import ForeignPrincipal
from fara_principals.exceptions import (
    InvalidPrincipalError
)

partial_principal = {
    "url": "f/?p=blah", "country": "Nigeria", "state": "Abuja", 
    "address": "no. 11 banjul street", "reg_number": "0419", 
    "principal_reg_date": "12/3/2018", "reg_date": "12/3/2018", 
    "registrant": "Mena360", "principal_name": "Fetchr",
    "exhibits": []
}
class TestPrincipal(TestCase):

    def setUp(self):
        pp = partial_principal
        self.principal = ForeignPrincipal(url=pp["url"], country=pp["country"], 
            state=pp["state"], address=pp["address"], reg_number=pp["reg_number"], 
            principal_name=pp["principal_name"], 
            principal_reg_date=pp["principal_reg_date"], 
            reg_date=pp["reg_date"], 
            registrant=pp["registrant"])

    def test_is_partial(self):
        self.assertEqual(True, self.principal.is_partial())

        self.principal.add_exhibit_dict({})
        self.assertEqual(False, self.principal.is_partial())

    def test_partial_dict(self):
        self.assertEqual(partial_principal, self.principal.to_dict())


    def test_validate_data_on_partial_fails(self):
        with self.assertRaises(InvalidPrincipalError):
            self.principal.validate_data()

    def test_validate_data_on_valid_data_passes(self):
        self.principal.add_exhibit_dict({})
        try:
            self.principal.validate_data()
        except InvalidPrincipalError as e:
            self.fail(
                "validate_partial() unexpectedly raised InvalidPrincipalError:{}"\
                .format(e))

    def test_validate_partial_on_partial_passes(self):
        try:
            self.principal.validate_partial()
        except InvalidPrincipalError as e:
            self.fail(
                "validate_partial() unexpectedly raised InvalidPrincipalError:{}"\
                .format(e))

    def test_validate_partial_on_valid_data_passes(self):
        self.principal.add_exhibit_dict({})
        try:
            self.principal.validate_partial()
        except InvalidPrincipalError as e:
            self.fail(
                "validate_partial() unexpectedly raised InvalidPrincipalError:{}"\
                .format(e))
