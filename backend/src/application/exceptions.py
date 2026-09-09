class DuplicateUserEmailError(Exception):
    """Raised when a user email already exists."""


class ReferencedArtistDeletionError(Exception):
    """Raised when an artist cannot be deleted because it is referenced."""