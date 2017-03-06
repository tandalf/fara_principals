from unittest import TestCase

from fara_principals.core.principals import ForeignPrincipal
from fara_principals.exceptions import (
    BadPrincipalSchemaError
)

partial_principal = {
    "url": "f/?p=blah", "country": "Nigeria", "state": "Abuja", 
    "address": "no. 11 banjul street", "reg_number": "0419", 
    "principal_reg_date": "12/3/2018", "principal_reg_date": "12/3/2018", 
    "registrant": "Mena360", "principal_name": "Fetchr"
}
class TestPrincipal(TestCase):

    def setUp(self):
        pp = partial_principal
        self.principal = ForeignPrincipal(url=pp["url"], country=pp["country"], 
            state=pp["state"], address=pp["address"], reg_number=pp["reg_number"], 
            principal_name=pp["principal_name"], 
            principal_reg_date=pp["principal_reg_date"], 
            principal_reg_date=pp["reg_date"], 
            registrant=pp["registrant"])

    def test_is_partial(self):
        self.assertEqual(True, self.principal)

    def test_partial_dict(self):
        self.assertEqual(partial_principal, self.principal.partial_dict())


    def test_validate_on_partial_fails(self):
        with self.assertRaises(BadPrincipalSchemaError):
            self.principal.validate_data()
