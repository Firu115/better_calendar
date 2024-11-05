from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
import requests
import icalendar as ical

app = FastAPI()


@app.get("/rest/calendars/user/{user}")
def sus(user: str, accessToken: str):
    new = ical.Calendar()
    new.add("PRODID", "Custom calendar by firu")
    new.add("VERSION", "2.0")
    new.add("CALSCALE", "GREGORIAN")

    r: requests.Response = requests.get(
        f"https://felsight.fel.cvut.cz/rest/calendars/user/{user}?accessToken={accessToken}"
    )
    if r.status_code != 200:
        return PlainTextResponse("Nefunguje to", 400)
    r.encoding = 'utf-8'
    print(r.text[:1000], r.encoding)

    felsight = ical.Calendar.from_ical(r.text)
    for event in felsight.walk("VEVENT"):
        new_event = ical.Event()
        new_event.add("SUMMARY", event.get("DESCRIPTION"))
        new_event.add("LOCATION", event.get("LOCATION"))
        new_event.add("DTSTART", event.get("DTSTART"))
        new_event.add("DTEND", event.get("DTEND"))

        description = event.get("SUMMARY").split()[:-1]
        description[0] = f"<b>{description[0]}</b>"
        new_event.add("DESCRIPTION", " ".join(description))
        
        new.add_component(new_event)

    f = open('example.ics', 'wb')
    f.write(new.to_ical())
    f = open('felsight.ics', 'wb')
    f.write(felsight.to_ical())

    return PlainTextResponse(new.to_ical())
