import strawberry
from typing import List
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Airport

@strawberry.type
class AirportType:
    id: int
    icao: str
    iata: str
    name: str
    city: str
    country: str
    latitude: str
    longitude: str

def get_airports(name: str = "") -> List[AirportType]:
    db: Session = SessionLocal()
    query = db.query(Airport)
    if name:
        query = query.filter(Airport.name.ilike(f"%{name}%"))
    airports = query.all()
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
