from pydantic import BaseModel
from datetime import datetime

# Comments in this file were generated with Gemma3:27b (local server) then reviewed by the developer.

class MeasurementResponse(BaseModel):
    """
    Pydantic model representing a measurement response.
    Used for serializing measurement data for API responses.
    """
    measurement_id: int  # Unique identifier for the measurement.
    sensor_id: str  # Identifier of the sensor that took the measurement.
    value: float  # The measured value.
    timestamp: datetime  # The timestamp when the measurement was taken.

    class Config:
        from_attributes = True  # Allows Pydantic to automatically populate fields from object attributes (e.g., SQLAlchemy model instances).

class MeasurementCreate(BaseModel):
    """
    Pydantic model representing a request to create a new measurement.
    Used for validating and parsing request data.
    """
    sensor_id: str  # Identifier of the sensor.
    value: float  # The measured value.
    timestamp: datetime  # The timestamp when the measurement was taken.

    class Config:
        from_attributes = True  # Allows Pydantic to automatically populate fields from object attributes. This is useful for converting SQLAlchemy model instances into Pydantic models.