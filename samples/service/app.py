import numpy as np
import uvicorn
from samples.service.generator import (
    generate_vacation_openings,
    VacationOpening,
    Reservation,
)
from samples.service.schema import BookingRequest
from datetime import date
from fastapi import FastAPI


NP_RANDOM = np.random.RandomState(1337)

app = FastAPI()
OPENINGS_DB = dict()
RESERVATIONS_DB = dict()

# kick off
OPENINGS_DB.update({row.vid: row for row in generate_vacation_openings(n=100)})


@app.get("/healthcheck")
def read_root():
    return {"Hello": "World"}


@app.get("/openings/count")
def get_count():
    return len(OPENINGS_DB)


@app.get("/openings/add")
def generate_openings(n: int = 10):
    new_rows = [row for row in generate_vacation_openings(n=n)]
    OPENINGS_DB.update({n.vid: n for n in new_rows})

    new_ct = len(OPENINGS_DB)
    return {
        "msg": f"{len(new_rows):,} rows added",
        "updated_rows_ct": new_ct,
        "record_ids": [n.vid for n in new_rows],
    }


@app.get("/openings/search")
def search_openings(
    country: str | None = None,
    start_date: date | None = None,
    end_date: date | None = None,
    rate: float | None = None,
    limit: int | None = None,
) -> dict:
    rows: list[VacationOpening] = [r for r in OPENINGS_DB.values()]

    search_params = dict()
    if country is not None:
        search_params["country"] = country
        rows = [r for r in rows if r.country == country]

    if start_date is not None:
        search_params["start_date"] = start_date
        rows = [r for r in rows if r.start_date >= start_date]

    if end_date is not None:
        search_params["end_date"] = end_date
        rows = [r for r in rows if r.end_date <= end_date]

    if rate is not None:
        search_params["rate"] = rate
        rows = [r for r in rows if r.day_rate <= rate]

    if limit:
        rows = rows[:limit]

    results_ct = len(rows)
    return {
        "results_count": results_ct,
        "search_params": search_params,
        "results": rows,
    }


@app.get("/reservations")
def get_reservations_list(user: str) -> list[Reservation]:
    return RESERVATIONS_DB.get(user)


def _pop_opening_and_book_reservation(request: BookingRequest):
    opening = OPENINGS_DB.pop(request.vid)
    if not opening:
        return {"msg": "could not find reservation: {}".format(request.vid)}

    new_booking = {
        "vacation_opening": opening.model_dump(),
        "user": request.user,
        "home_country": request.home_country,
        "phone_number": request.phone_number,
        "start_date": request.start_date,
        "end_date": request.end_date,
        "reservation_people_count": request.people_count,
    }

    ressy = Reservation.model_validate(new_booking)
    RESERVATIONS_DB[ressy.rid] = ressy
    return {"msg": "booking made", "data": ressy}


@app.post("/reservations/book")
def book_reservation(request: BookingRequest):
    # should remove the reservation
    return _pop_opening_and_book_reservation(request)


@app.post("/reservations/competitive_book")
def book_reservation_against_others(request: BookingRequest):
    # to mimick incase reservation doesn't exist again
    if NP_RANDOM.rand() > 0.3:
        return {"msg": "opening is no longer available"}

    return _pop_opening_and_book_reservation(request)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
