from .profanity_filter import ProfanityFilter


class Censor(ProfanityFilter):
    """
    DEPRECATED

    Use `ProfanityFilter` instead
    """

    pass


__all__ = ["ProfanityFilter", "Censor"]
