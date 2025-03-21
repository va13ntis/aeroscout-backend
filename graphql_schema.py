import strawberry
from typing import List, Optional
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Airport
import math

@strawberry.type
class AirportType:
    id: int
    icao: str
    iata: Optional[str]
    name: str
    city: Optional[str]
    country: Optional[str]
    latitude: float
    longitude: float

# Haversine formula to calculate distance between two coordinates
def haversine(lat1, lon1, lat2, lon2):
    r = 6371  # Earth radius in km
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    d_lat = lat2 - lat1
    d_lon = lon2 - lon1
    a = math.sin(d_lat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(d_lon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return r * c * 0.539957  # Convert km to nautical miles

def get_airports(
    name: Optional[str] = None,
    icao: Optional[str] = None,
    city: Optional[str] = None,
    country: Optional[str] = None,
    lat: Optional[float] = None,
    lon: Optional[float] = None,
    max_distance: Optional[float] = None
) -> List[AirportType]:
    db: Session = SessionLocal()
    query = db.query(Airport)

    if name:
        query = query.filter(Airport.name.ilike(f"%{name}%"))
    if icao:
        query = query.filter(Airport.icao.ilike(f"%{icao}%"))
    if city:
        query = query.filter(Airport.city.ilike(f"%{city}%"))
    if country:
        query = query.filter(Airport.country.ilike(f"%{country}%"))

    airports = query.all()

    # Filter by distance if lat/lon is provided
    if lat and lon and max_distance:
        airports = [
            airport for airport in airports
            if haversine(lat, lon, airport.latitude, airport.longitude) <= max_distance
        ]

    db.close()

    return [AirportType(
        id=airport.id,
        icao=airport.icao,
        iata=airport.iata,
        name=airport.name,
        city=airport.city,
        country=airport.country,
        latitude=airport.latitude,
        longitude=airport.longitude
    ) for airport in airports]


@strawberry.type
class Query:
    airports: List[AirportType] = strawberry.field(resolver=get_airports)

schema = strawberry.Schema(query=Query)
