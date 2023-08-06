class ChallengeError(Exception):
    """Raised when challenge cannot be completed.
    """
    pass


class AlienMatterError(Exception):
    """Raised when integrity of key material cannot be verified
    """
    pass
