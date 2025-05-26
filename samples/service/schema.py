import datetime
from pydantic import BaseModel
from samples.service.meta import Country


class BookingRequest(BaseModel):
    vid: str
    user: str
    home_country: Country
    phone_number: str
    start_date: datetime.date
    end_date: datetime.date
    people_count: int
