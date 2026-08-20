from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# 1. The Daily Check-in Model
class DailyCheckIn(BaseModel):
    checkin_id: str
    user_id: str
    timestamp: datetime
    mood: str
    energy_level: int = Field(..., ge=1, le=5)
    focus_level: int = Field(..., ge=1, le=5)
    stress_level: int = Field(..., ge=1, le=5)
    sleep_quality: str
    physical_comfort: str
    excitement_to_work: int = Field(..., ge=1, le=5)
    notes: Optional[str] = None

    # 2. The Task Model
class Task(BaseModel):
    task_id: str
    task_name: str
    description: Optional[str] = None
    estimated_duration_minutes: int
    status: str = "pending"
    type: str
    cognitive_load: str
    deadline: Optional[str] = None
        