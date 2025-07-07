"""Joker module."""

from typing import Optional
from abc import abstractmethod
from enum import Enum
import random

RETRIGGER = "retrigger"
GENERATE_PLANET = "generate_planet"
GENERATE_TAROT = "generate_tarot"


class Roller:
    """Roller class to handle random number generation."""

    def __init__(self) -> None:
        """Initialize Roller."""
        self._jokers: list[Joker] = []

    @property
    def jokers(self) -> list["Joker"]:
        """Return the list of jokers."""
        return self._jokers

    @jokers.setter
    def jokers(self, jokers: list["Joker"]) -> None:
        """Set the list of jokers."""
        self._jokers = jokers

    def roll(self, numerator: int, denominator: int) -> int:
        """Roll the dice and return the result."""
        for joker in self.jokers:
            if joker.name == "Oops! All 6s":
                numerator *= 2

        return random.random() < (numerator / denominator)


class Playable:
    """Playable interface for card enhancements, editions, and seals."""

    @staticmethod
    @abstractmethod
    def play(*args, **kwargs) -> tuple[int, int | float, int]:
        """Play the card and return the updated chips, multiplier, and money."""
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def held(*args, **kwargs) -> tuple[int, int | float, int]:
        """Return the held state of the card."""
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def discard(*args, **kwargs) -> str | None:
        """Discard the card."""
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def final_hand(*args, **kwargs) -> str | None:
        """Return action for final hand."""
        raise NotImplementedError


class Enhancement(Playable, Enum):
    """Enumeration for card enhancements."""

    NONE = "none"
    BONUS = "bonus"
    MULT = "mult"
    WILD = "wild"
    GLASS = "glass"
    STEEL = "steel"
    STONE = "stone"
    GOLD = "gold"
    LUCKY = "lucky"

    @staticmethod
    def play(
        enhancement: "Enhancement",
        chips: int,
        mult: int | float,
        money: int,
        roller: Roller,
    ) -> tuple[int, int | float, int]:
        if enhancement == Enhancement.NONE:
            return chips, mult, money
        elif enhancement == Enhancement.BONUS:
            return chips + 30, mult, money
        elif enhancement == Enhancement.MULT:
            return chips, mult + 4, money
        elif enhancement == Enhancement.GLASS:
            return chips, mult * 2, money
        elif enhancement == Enhancement.STONE:
            return (
                chips + 50,
                mult,
                money,
            )
        elif enhancement == Enhancement.LUCKY:
            if roller.roll(1, 5):
                mult += 20
            if roller.roll(1, 15):
                money += 20
            return chips, mult, money
        else:
            return chips, mult, money

    @staticmethod
    def held(
        enhancement: "Enhancement", chips: int, mult: int | float, money: int
    ) -> tuple[int, int | float, int]:
        if enhancement == Enhancement.NONE:
            return chips, mult, money
        elif enhancement == Enhancement.STEEL:
            return chips, mult * 1.5, money
        elif enhancement == Enhancement.GOLD:
            return chips, mult, money + 3
        else:
            return chips, mult, money

    @staticmethod
    def discard(enhancement: "Enhancement") -> None:
        return None

    @staticmethod
    def final_hand(enhancement: "Enhancement") -> None:
        return None


class Edition(Playable, Enum):
    """Enumeration for card editions."""

    BASE = "base"
    FOIL = "foil"
    HOLOGRAPHIC = "holographic"
    POLYCHROME = "polychrome"

    @staticmethod
    def play(
        edition: "Edition", chips: int, mult: int | float, money: int
    ) -> tuple[int, int | float, int]:
        if edition == Edition.BASE:
            return chips, mult, money
        elif edition == Edition.FOIL:
            return chips + 50, mult, money
        elif edition == Edition.HOLOGRAPHIC:
            return chips, mult + 10, money
        elif edition == Edition.POLYCHROME:
            return chips, mult * 1.5, money
        else:
            return chips, mult, money

    @staticmethod
    def held(
        edition: "Edition", chips: int, mult: int | float, money: int
    ) -> tuple[int, int | float, int]:
        return chips, mult, money

    @staticmethod
    def discard(edition: "Edition") -> None:
        return None

    @staticmethod
    def final_hand(edition: "Edition") -> None:
        return None


class Seal(Playable, Enum):
    """Enumeration for card seals."""

    NONE = "none"
    GOLD = "gold"
    RED = "red"
    BLUE = "blue"
    PURPLE = "purple"

    @staticmethod
    def play(
        seal: "Seal", chips: int, mult: int | float, money: int
    ) -> tuple[int, int | float, int]:
        if seal == Seal.NONE:
            return chips, mult, money
        elif seal == Seal.GOLD:
            return chips, mult, money + 3
        else:
            return chips, mult, money

    @staticmethod
    def held(
        seal: "Seal", chips: int, mult: int | float, money: int
    ) -> tuple[int, int | float, int]:
        return chips, mult, money

    @staticmethod
    def discard(seal: "Seal") -> str | None:
        if seal == Seal.PURPLE:
            return GENERATE_TAROT
        else:
            return None

    @staticmethod
    def final_hand(seal: "Seal") -> str | None:
        if seal == Seal.BLUE:
            return GENERATE_PLANET
        else:
            return None


class Sticker(Enum):
    """Enumeration for card stickers."""

    NONE = "none"
    ETERNAL = "eternal"
    PERISHABLE = "perishable"
    RENTAL = "rental"


class Card:
    """Card class to represent a playing card."""

    def __init__(
        self,
        suit: str,
        rank: str,
        enhancement: Optional[Enhancement] = Enhancement.NONE,
        edition: Optional[Edition] = Edition.BASE,
        seal: Optional[Seal] = Seal.NONE,
        sticker: Optional[Sticker] = Sticker.NONE,
    ) -> None:
        """Initialize Card with suit and rank."""
        self.suit = suit
        self.rank = rank
        self.enhancement = enhancement
        self.edition = edition
        self.seal = seal
        self.sticker = sticker
        self.debuffed = False

        self._chips = int(self.rank)
        self._mult = 1

    @property
    def chips(self) -> int:
        """Return the number of chips associated with the card."""
        return self._chips

    @chips.setter
    def chips(self, value: int) -> None:
        self._chips = value

    def play(self, chips: int, mult: int, money: int) -> tuple[int, int, int]:
        """Play the card and return the updated chips, multiplier, and money."""
        return chips, mult, money


class Hand:
    """Hand class to represent a player's hand in the game."""

    def __init__(self) -> None:
        """Initialize Hand with a list of cards."""


class Joker:
    """Joker class."""

    def __init__(
        self,
        name: str,
        edition: Optional[Edition] = Edition.BASE,
        sticker: Optional[Sticker] = Sticker.NONE,
    ) -> None:
        """Initialize Joker."""
        self.name = name
        self.edition: Optional[Edition] = edition
        self.sticker: Optional[Sticker] = sticker
