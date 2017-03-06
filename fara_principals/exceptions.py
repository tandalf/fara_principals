class FaraException(Exception):
    """
    Base exception class for this software
    """
    pass

class PrincipalError(FaraException):
    """
    Raised when there is a problem with a principal data
    """
    pass

class BadPrincipalSchemaError(PrincipalError):
    """
    Raise when the schema for a principal does not contain certain required
    fields.
    """
    pass