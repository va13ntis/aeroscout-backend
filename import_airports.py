import pandas as pd
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Airport, Base

# Ensure tables exist
Base.metadata.create_all(bind=engine)

def import_airports():
    df = pd.read_csv("data/airports.csv")

    db: Session = SessionLocal()

    for _, row in df.iterrows():
        if pd.isna(row["ident"]) or pd.isna(row["name"]):
            continue  # Skip invalid rows

        airport = Airport(
            icao=row["ident"],
            iata=row["iata_code"] if pd.notna(row["iata_code"]) else None,
            name=row["name"],
            city=row["municipality"] if pd.notna(row["municipality"]) else None,
            country=row["iso_country"] if pd.notna(row["iso_country"]) else None,
            latitude=row["latitude_deg"],
            longitude=row["longitude_deg"]
        )

        db.add(airport)

    db.commit()
    db.close()
    print("✅ Airport data imported successfully!")

if __name__ == "__main__":
    import_airports()
