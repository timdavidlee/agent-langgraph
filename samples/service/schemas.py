import datetime
from enum import StrEnum
from pydantic import BaseModel, field_validator
from samples.service.meta import Country
from samples.service.generator import VacationOpening, Reservation
from typing import Any


class ResponseStatus(StrEnum):
    CONFIRMED = "confirmed"
    NOT_AVAILABLE = "not-available"
    NOT_FOUND = "not-found"
    FOUND = "found"


class BookingRequest(BaseModel):
    vid: str
    user: str
    home_country: Country
    phone_number: str
    start_date: datetime.date
    end_date: datetime.date
    people_count: int

    @classmethod
    @field_validator("start_date", mode="pre")
    def parse_start_date(cls, value: str):
        try:
            return datetime.datetime.strptime(value, "%Y-%m-%d").date
        except Exception:
            try:
                return datetime.datetime.strptime(value, "%Y-%m-%d %H:%M:%S").date
            except Exception as e:
                raise e


    @classmethod
    @field_validator("end_date", mode="pre")
    def parse_end_date(cls, value: str):
        try:
            return datetime.datetime.strptime(value, "%Y-%m-%d").date
        except Exception:
            try:
                return datetime.datetime.strptime(value, "%Y-%m-%d %H:%M:%S").date
            except Exception as e:
                raise e


class SearchResultsRequest(BaseModel):
    country: Country | None = None
    start_date: datetime.date | None = None
    end_date: datetime.date | None = None
    rate: float | int | None = None
    limit: int | None = None


class SearchResultsResponse(BaseModel):
    status: ResponseStatus = ResponseStatus.FOUND
    results_count: int
    search_params: dict[str, Any]
    results: list[VacationOpening]


class GetUserReservationsResponse(BaseModel):
    status: ResponseStatus
    reservations: dict[str, Reservation]


class BookingResponse(BaseModel):
    msg: str = ""
    status: ResponseStatus
    details: Reservation | None = None
