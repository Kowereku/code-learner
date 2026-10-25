import enum


class Track(str, enum.Enum):
    """Learning area a user picks after registering; courses are preset per area."""

    data_science = "data_science"
    linux = "linux"
    backend = "backend"
