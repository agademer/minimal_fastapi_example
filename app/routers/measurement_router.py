from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.measurement_schema import MeasurementResponse, MeasurementCreate
from crud import measurement_crud as crud
from core.database import get_db
from typing import List

# Comments in this file were generated with Gemma3:27b (local server) then reviewed by the developer.


router = APIRouter(
    tags=["Measurement"],
    prefix="/measurements"
)

# API endpoint to create a measurement
@router.post("", response_model=MeasurementResponse)
async def create_measurement(measurement: MeasurementCreate, db: Session = Depends(get_db)):
    """
    Creates a new measurement record in the database.

    Args:
        measurement: The MeasurementCreate schema containing the measurement data.
        db: The database session.

    Returns:
        The created MeasurementResponse object.

    Raises:
        HTTPException: If a measurement already exists for the given sensor and timestamp (409 Conflict).
    """
    # Check if a measurement already exists for this sensor and timestamp to prevent duplicates.
    existing = crud.get_measurement_by_sensor_id_and_timestamp(db, measurement.sensor_id, measurement.timestamp)
    if existing:
        raise HTTPException(status_code=409, detail="Une mesure existe déjà pour ce capteur et cette horodatage.")  # Conflict: Resource already exists
    return crud.create_measurement(db, measurement)  # Call the CRUD function to create the measurement.

# API endpoint to get all measurements
@router.get("", response_model=List[MeasurementResponse])
async def get_measurements(db: Session = Depends(get_db)):
    """
    Retrieves all measurement records from the database.

    Args:
        db: The database session.

    Returns:
        A list of MeasurementResponse objects.
    """
    crud.seed_measurements(db)
    return crud.get_all_measurement(db)  # Call the CRUD function to get all measurements.

# API endpoint to get the measurements by sensor_id
@router.get("/{sensor_id}", response_model=List[MeasurementResponse])
async def get_measurement_by_sensor_id(sensor_id: str, db: Session = Depends(get_db)):
    """
    Retrieves all measurements for a given sensor ID.

    Args:
        sensor_id: The ID of the sensor.
        db: The database session.

    Returns:
        A list of MeasurementResponse objects.

    Raises:
        HTTPException: If no measurements are found for the given sensor ID (404 Not Found).
    """
    db_measurement = crud.get_measurement_by_sensor_id(db, sensor_id)
    if db_measurement is None:
        raise HTTPException(status_code=404, detail="No measurements found")  # Not Found: Resource doesn't exist
    return db_measurement

# API endpoint to delete a measurement by ID
@router.delete("/{measurement_id}", response_model=MeasurementResponse)
async def delete_module(measurement_id: int, db: Session = Depends(get_db)):
    """
    Deletes a measurement record by its ID.

    Args:
        measurement_id: The ID of the measurement to delete.
        db: The database session.

    Returns:
        The deleted MeasurementResponse object.

    Raises:
        HTTPException: If the measurement with the given ID is not found (404 Not Found).
    """
    # Check if the measurement exists before attempting to delete it.
    db_measurement = crud.get_measurement_by_id(db, measurement_id)
    if db_measurement is None:
        raise HTTPException(status_code=404, detail="Measurement not found")  # Not Found: Resource doesn't exist
    return crud.delete_measurement(db, db_measurement)