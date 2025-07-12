"""Joker module."""

import random
from abc import abstractmethod
from enum import Enum, auto

RETRIGGER = "retrigger"
GENERATE_PLANET = "generate_planet"
GENERATE_TAROT = "generate_tarot"


class Rank(int, Enum):
    """Enumeration for card ranks."""

    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    ACE = 14


class Suit(int, Enum):
    """Enumeration for card suits."""

    DIAMONDS = auto()
    CLUBS = auto()
    HEARTS = auto()
    SPADES = auto()


class HandType(int, Enum):
    """Enumeration for hand types."""

    HIGH_CARD = auto()
    PAIR = auto()
    TWO_PAIR = auto()
    THREE_OF_A_KIND = auto()
    STRAIGHT = auto()
    FLUSH = auto()
    FULL_HOUSE = auto()
    FOUR_OF_A_KIND = auto()
    STRAIGHT_FLUSH = auto()
    ROYAL_FLUSH = auto()
    FIVE_OF_A_KIND = auto()
    FLUSH_HOUSE = auto()
    FLUSH_FIVE = auto()


class Hand:
    """Hand type for cards."""

    def __init__(
        self,
        hand_type: HandType,
        base_chips: int,
        base_mult: int,
        chips_on_level: int,
        mult_on_level: int,
    ) -> None:
        self.hand_type = hand_type
        self.base_chips = base_chips
        self.base_mult = base_mult
        self.chips_on_level = chips_on_level
        self.mult_on_level = mult_on_level
        self.level = 1

    def level_hand(self) -> None:
        self.base_chips += self.chips_on_level
        self.base_mult += self.mult_on_level
        self.level += 1


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
    def held(enhancement: "Enhancement", chips: int, mult: int | float, money: int) -> tuple[int, int | float, int]:
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
    NEGATIVE = "negative"

    @staticmethod
    def play(edition: "Edition", chips: int, mult: int | float, money: int) -> tuple[int, int | float, int]:
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
    def held(edition: "Edition", chips: int, mult: int | float, money: int) -> tuple[int, int | float, int]:
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
    def play(seal: "Seal", chips: int, mult: int | float, money: int) -> tuple[int, int | float, int]:
        if seal == Seal.NONE:
            return chips, mult, money
        elif seal == Seal.GOLD:
            return chips, mult, money + 3
        else:
            return chips, mult, money

    @staticmethod
    def held(seal: "Seal", chips: int, mult: int | float, money: int) -> tuple[int, int | float, int]:
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
        suit: Suit,
        rank: Rank,
        enhancement: Enhancement | None = Enhancement.NONE,
        edition: Edition | None = Edition.BASE,
        seal: Seal | None = Seal.NONE,
    ) -> None:
        """Initialize Card with suit and rank."""
        if edition == Edition.NEGATIVE:
            raise ValueError("Negative edition is not allowed for Card.")

        self.suit = suit
        self.rank = rank
        self.enhancement = enhancement
        self.edition = edition
        self.seal = seal
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


class DefaultDeck:
    """DefaultDeck class to represent a standard deck of cards."""

    def __init__(self) -> None:
        """Initialize DefaultDeck with a list of cards."""
        self.cards = [Card(suit=suit, rank=rank) for rank in Rank for suit in Suit]

    @property
    def num_hands(self) -> int:
        """Return the number of hands in the deck."""
        return 3

    @property
    def num_discards(self) -> int:
        """Return the number of discards in the deck."""
        return 3


class Joker:
    """Joker class."""

    def __init__(
        self,
        name: str,
        edition: Edition | None = Edition.BASE,
        sticker: Sticker | None = Sticker.NONE,
    ) -> None:
        """Initialize Joker."""
        self.name = name
        self.edition: Edition | None = edition
        self.sticker: Sticker | None = sticker
