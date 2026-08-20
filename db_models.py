from sqlalchemy import  Column, Integer, String
from database import Base

# 1. The Task Database Table 
class DBTask(Base):
    __tablename__ = "tasks"

    # Define the columns
    task_id = Column(String, primary_key=True, index=True)
    task_name = Column(String, index=True)
    description = Column(String, nullable=True)
    estimated_duration_minutes = Column(Integer)
    status = Column(String, default="pending")
    type = Column(String)
    cognitive_load = Column(String)
    deadline = Column(String, nullable=True)

# 2. The Daily Check-in Database Table
class DBDailyCheckIn(Base):
    __tablename__ = "daily_checkins"

    checkin_id = Column(String, primary_key=True, index=True)
    user_id = Column(String, index=True)
    timestamp = Column(String) # I will store the datetime as an ISO-formatted string
    mood = Column(String)
    energy_level = Column(Integer)
    focus_level = Column(Integer) 
    stress_level = Column(Integer)
    sleep_quality = Column(String)
    physical_comfort = Column(String)
    excitement_to_work = Column(Integer)
    notes = Column(String, nullable=True)