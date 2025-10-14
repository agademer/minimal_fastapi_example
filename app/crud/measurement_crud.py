from sqlalchemy.orm import Session
from models.measurement import Measurement
from schemas.measurement_schema import MeasurementCreate
from datetime import datetime, timedelta
import math

# Comments in this file were generated with Gemma3:27b (local server) then reviewed by the developer.

def create_measurement(db: Session, measurement: MeasurementCreate) -> Measurement:
    """
    Creates a new measurement record in the database.

    Args:
        db: The SQLAlchemy database session.
        measurement: A MeasurementCreate object containing the data for the new measurement.

    Returns:
        The newly created Measurement object.
    """
    db_measurement = Measurement(**measurement.model_dump()) # Create a Measurement object from the MeasurementCreate data.  The ** operator unpacks the dictionary into keyword arguments for the Measurement constructor.
    db.add(db_measurement) # Add the new measurement to the database session.  This stages the changes but doesn't commit them yet.
    db.commit() # Commit the changes to the database, making them permanent.
    db.refresh(db_measurement) # Refresh the object from the database, ensuring that any server-side defaults or auto-generated values are reflected in the object.
    return db_measurement

def get_all_measurement(db: Session) -> list[Measurement]:
    """
    Retrieves all measurement records from the database.

    Args:
        db: The SQLAlchemy database session.

    Returns:
        A list of Measurement objects.
    """
    return db.query(Measurement).all() # Query the Measurement table and retrieve all records.

def get_measurement_by_id(db: Session, measurement_id: int) -> Measurement:
    """
    Retrieves a measurement record from the database by its ID.

    Args:
        db: The SQLAlchemy database session.
        measurement_id: The ID of the measurement to retrieve.

    Returns:
        The Measurement object with the given ID, or None if no such record exists.
    """
    return db.query(Measurement).filter(Measurement.measurement_id == measurement_id).first() # Query the Measurement table, filter by measurement_id, and retrieve the first matching record.

def get_measurement_by_sensor_id(db: Session, sensor_id: str) -> list[Measurement]:
    """
    Retrieves all measurement records from the database for a given sensor ID.

    Args:
        db: The SQLAlchemy database session.
        sensor_id: The ID of the sensor to filter by.

    Returns:
        A list of Measurement objects for the given sensor ID.
    """
    return db.query(Measurement).filter(Measurement.sensor_id == sensor_id).all()

def get_measurement_by_sensor_id_and_timestamp(db: Session, sensor_id: str, timestamp: datetime) -> Measurement:
    """
    Retrieves a measurement record from the database for a given sensor ID and timestamp.

    Args:
        db: The SQLAlchemy database session.
        sensor_id: The ID of the sensor to filter by.
        timestamp: The timestamp to filter by.

    Returns:
        The Measurement object with the given sensor ID and timestamp, or None if no such record exists.
    """
    return db.query(Measurement).filter(Measurement.sensor_id == sensor_id, Measurement.timestamp == timestamp).first()

def delete_measurement(db: Session, db_measurement: Measurement) -> Measurement:
    """
    Deletes a measurement record from the database.

    Args:
        db: The SQLAlchemy database session.
        db_measurement: The Measurement object to delete.

    Returns:
        The deleted Measurement object.
    """
    db.delete(db_measurement) # Delete the measurement record from the database.
    db.commit() # Commit the changes to the database.
    return db_measurement

def seed_measurements(db: Session):
    if get_all_measurement(db) == []: # DB empty
        for i in range(20):
            create_measurement(db,MeasurementCreate(sensor_id="sensor0",value=(math.sin(i/7)),timestamp=datetime.now()+timedelta(seconds=i)))
    db.commit()