from sqlalchemy import Column, String, Integer, Float, DateTime
from core.database import Base

# Comments in this file were generated with Gemma3:27b (local server) then reviewed by the developer.

class Measurement(Base):
    """
    SQLAlchemy model representing a measurement record.
    This class defines the structure of the 'measurements' table in the database.
    """
    __tablename__ = "measurements"  # Specifies the name of the database table this model represents.

    measurement_id = Column(Integer, primary_key=True, autoincrement=True)  # Unique identifier for the measurement.  Automatically incremented.
    sensor_id = Column(String(50), nullable=False)  # Identifier of the sensor that took the measurement.  Cannot be null.
    value = Column(Float, nullable=False)  # The measured value. Cannot be null.
    timestamp = Column(DateTime, nullable=False)  # The timestamp when the measurement was taken. Cannot be null.

    def __str__(self):
        """
        String representation of the Measurement object.
        Useful for debugging and logging.
        """
        return f"{self.sensor_id}: {self.value} @ {self.timestamp}"  # Returns a formatted string containing sensor_id, value, and timestamp.