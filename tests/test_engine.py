"""Tests for the engine module."""

from unittest.mock import patch
from src.engine import Roller, Joker, Enhancement, Edition, Seal, GENERATE_TAROT, GENERATE_PLANET
import pytest


def test_roller_without_oops_joker() -> None:
    """Test roller without Oops! All 6s joker."""
    with patch("src.engine.random.random", return_value=0.3):
        roller = Roller()
        result = roller.roll(1, 5)
        assert result is False


def test_roller_with_oops_joker_doubles_numerator() -> None:
    """Test roller with Oops! All 6s joker."""
    oops_joker = Joker("Oops! All 6s")

    with patch("src.engine.random.random", return_value=0.3):
        roller = Roller()
        roller.jokers = [oops_joker]

        result = roller.roll(1, 5)
        assert result is True


@pytest.mark.parametrize(
    "enhancement, expected_chips, expected_mult, expected_money",
    [
        (Enhancement.NONE, 1, 1, 1),
        (Enhancement.BONUS, 31, 1, 1),
        (Enhancement.MULT, 1, 5, 1),
        (Enhancement.WILD, 1, 1, 1),
        (Enhancement.GLASS, 1, 2, 1),
        (Enhancement.STEEL, 1, 1, 1),
        (Enhancement.STONE, 51, 1, 1),
        (Enhancement.GOLD, 1, 1, 1),
        (Enhancement.LUCKY, 1, 21, 21),
    ],
)
def test_enhancement_play(
    enhancement: Enhancement,
    expected_chips: int,
    expected_mult: int,
    expected_money: int,
) -> None:
    """Test enhancement play."""
    roller = Roller()
    if enhancement == Enhancement.LUCKY:
        with patch.object(roller, "roll", side_effect=[True, True]):
            assert Enhancement.play(
                enhancement, chips=1, mult=1, money=1, roller=roller
            ) == (expected_chips, expected_mult, expected_money)
    else:
        assert Enhancement.play(
            enhancement, chips=1, mult=1, money=1, roller=roller
        ) == (expected_chips, expected_mult, expected_money)


@pytest.mark.parametrize(
    "enhancement, expected_chips, expected_mult, expected_money",
    [
        (Enhancement.NONE, 1, 1, 1),
        (Enhancement.BONUS, 1, 1, 1),
        (Enhancement.MULT, 1, 1, 1),
        (Enhancement.WILD, 1, 1, 1),
        (Enhancement.GLASS, 1, 1, 1),
        (Enhancement.STEEL, 1, 1.5, 1),
        (Enhancement.STONE, 1, 1, 1),
        (Enhancement.GOLD, 1, 1, 4),
        (Enhancement.LUCKY, 1, 1, 1),
    ],
)
def test_enhancement_held(
    enhancement: Enhancement,
    expected_chips: int,
    expected_mult: int,
    expected_money: int,
) -> None:
    """Test enhancement held."""
    assert Enhancement.held(enhancement, chips=1, mult=1, money=1) == (
        expected_chips,
        expected_mult,
        expected_money,
    )


@pytest.mark.parametrize(
    "edition, expected_chips, expected_mult, expected_money",
    [
        (Edition.BASE, 1, 1, 1),
        (Edition.FOIL, 51, 1, 1),
        (Edition.HOLOGRAPHIC, 1, 11, 1),
        (Edition.POLYCHROME, 1, 1.5, 1),
    ],
)
def test_edition_play(
    edition: Edition,
    expected_chips: int,
    expected_mult: float,
    expected_money: int,
) -> None:
    """Test edition play."""
    assert Edition.play(edition, chips=1, mult=1, money=1) == (
        expected_chips,
        expected_mult,
        expected_money,
    )


@pytest.mark.parametrize(
    "edition, expected_chips, expected_mult, expected_money",
    [
        (Edition.BASE, 1, 1, 1),
        (Edition.FOIL, 1, 1, 1),
        (Edition.HOLOGRAPHIC, 1, 1, 1),
        (Edition.POLYCHROME, 1, 1, 1),
    ],
)
def test_edition_held(
    edition: Edition,
    expected_chips: int,
    expected_mult: int,
    expected_money: int,
) -> None:
    """Test edition held."""
    assert Edition.held(edition, chips=1, mult=1, money=1) == (
        expected_chips,
        expected_mult,
        expected_money,
    )


@pytest.mark.parametrize(
    "seal, expected_chips, expected_mult, expected_money",
    [
        (Seal.NONE, 1, 1, 1),
        (Seal.GOLD, 1, 1, 4),
        (Seal.RED, 1, 1, 1),
        (Seal.BLUE, 1, 1, 1),
        (Seal.PURPLE, 1, 1, 1),
    ],
)
def test_seal_play(
    seal: Seal,
    expected_chips: int,
    expected_mult: int,
    expected_money: int,
) -> None:
    """Test seal play."""
    assert Seal.play(seal, chips=1, mult=1, money=1) == (
        expected_chips,
        expected_mult,
        expected_money,
    )


@pytest.mark.parametrize(
    "seal, expected_chips, expected_mult, expected_money",
    [
        (Seal.NONE, 1, 1, 1),
        (Seal.GOLD, 1, 1, 1),
        (Seal.RED, 1, 1, 1),
        (Seal.BLUE, 1, 1, 1),
        (Seal.PURPLE, 1, 1, 1),
    ],
)
def test_seal_held(
    seal: Seal,
    expected_chips: int,
    expected_mult: int,
    expected_money: int,
) -> None:
    """Test seal held."""
    assert Seal.held(seal, chips=1, mult=1, money=1) == (
        expected_chips,
        expected_mult,
        expected_money,
    )


@pytest.mark.parametrize(
    "seal, expected_action",
    [
        (Seal.NONE, None),
        (Seal.GOLD, None),
        (Seal.RED, None),
        (Seal.BLUE, None),
        (Seal.PURPLE, GENERATE_TAROT),
    ],
)
def test_seal_discard(seal: Seal, expected_action: str | None) -> None:
    """Test seal discard."""
    assert Seal.discard(seal) == expected_action


@pytest.mark.parametrize(
    "seal, expected_action",
    [
        (Seal.NONE, None),
        (Seal.GOLD, None),
        (Seal.RED, None),
        (Seal.BLUE, GENERATE_PLANET),
        (Seal.PURPLE, None),
    ],
)
def test_seal_final_hand(seal: Seal, expected_action: str | None) -> None:
    """Test seal final_hand."""
    assert Seal.final_hand(seal) == expected_action


def test_my_failing_test() -> None:
    assert False