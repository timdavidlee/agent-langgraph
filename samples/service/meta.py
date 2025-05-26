import numpy as np
from numpy.typing import ArrayLike
from enum import Enum, StrEnum
import pandas as pd

RANDOM_STATE = np.random.RandomState(1337)


class HotelCompany(StrEnum):
    JINJIAN = "Jin Jiang International"
    WYNDHAM = "Wyndham Hotels & Resorts"
    MARRIOTT = "Marriott Interational"
    HUAZHU = "Huazhu Hotels Group"
    CHOICE = "Choice Hotels International"
    HILTON = "Hilton Worldwide"
    IHG = "IHG Hotels & Resorts"
    BTG = "BTG Home Inns"
    ACCOR = "Accor"
    BWH = "BWH Hotel Group"


class LodgingClass(StrEnum):
    STUDIO = "studio"
    ONE_BED = "one_bedroom"
    TWO_BED = "two_bedroom"
    THREE_BED = "three_bedroom"
    SUITE = "suite"
    CABIN = "cabin"
    LUXURY = "luxury"


LODGING_RATES = {
    LodgingClass.STUDIO: (200, 400),
    LodgingClass.ONE_BED: (300, 600),
    LodgingClass.TWO_BED: (400, 800),
    LodgingClass.THREE_BED: (600, 1200),
    LodgingClass.SUITE: (800, 1500),
    LodgingClass.CABIN: (1000, 1800),
    LodgingClass.LUXURY: (1500, 3000),
}


class Country(StrEnum):
    INDIA = "India"
    CHINA = "China"
    UNITED_STATES = "United States"
    INDONESIA = "Indonesia"
    PAKISTAN = "Pakistan"
    NIGERIA = "Nigeria"
    BRAZIL = "Brazil"
    BANGALDESH = "Bangladesh"
    RUSSIA = "Russia"
    MEXICO = "Mexico"
    JAPAN = "Japan"
    PHILIPPINES = "Philippines"
    ETHIOPIA = "Ethiopia"
    CONGO = "Democratic Republic of the Congo"
    EGYPT = "Egypt"
    VIETNAM = "Vietnam"
    IRAN = "Iran"
    TURKEY = "Turkey"
    GERMANY = "Germany"
    FRANCE = "France"
    UNITED_KINGDOM = "United Kingdom"
    TANZANIA = "Tanzania"
    THAILAND = "Thailand"
    SOUTH_AFRICA = "South Africa"
    ITALY = "Italy"
    COLOMBIA = "Colombia"
    KENYA = "Kenya"
    MYANMAR = "Myanmar"
    SOUTH_KOREA = "South Korea"
    SUDAN = "Sudan"


def _generate_choice_probs(n: int) -> ArrayLike:
    vals = np.arange(1, n + 1)
    fracs = 1 / vals
    prof = fracs / fracs.sum()
    return prof


def _generate_weighted_sample(var_enum: Enum, generated_ct: int):
    vals = list(var_enum)
    probs = _generate_choice_probs(len(vals))
    return RANDOM_STATE.choice(vals, size=generated_ct, p=probs)


def generate_countries(n: int):
    return _generate_weighted_sample(Country, generated_ct=n)


def generate_lodging(n: int):
    lodgings = _generate_weighted_sample(LodgingClass, generated_ct=n)
    collector = []
    for ld in lodgings:
        low, high = LODGING_RATES[ld]
        rate = RANDOM_STATE.randint(low, high)
        collector.append([ld, rate])
    return collector


def generate_hotel(n: int):
    return _generate_weighted_sample(HotelCompany, generated_ct=n)


def generate_start_dates(n: int):
    annual_dates = pd.date_range("2024-01-01", "2024-12-31")
    annual_dates = [ad.date() for ad in annual_dates]
    return RANDOM_STATE.choice(annual_dates, size=n)


def generate_durations(n: int):
    return RANDOM_STATE.randint(1, 30, size=n)
