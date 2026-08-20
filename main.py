from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from ai_service import analyze_task_complexity, synthesize_user_data

from models import DailyCheckIn, Task # Pydantic (Vaildation)
import db_models                      # SQLAlchemy (Schema)
from database import engine, SessionLocal

# 1. Crate the database tables on the hard drive
db_models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="MindGage API")

app.add_middleware(
    CORSMiddleware, 
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Dependency: The Database Connection Manager
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Root Endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to the MindGage API!"}

# 3. GET Endpoint: Retrieve Tasks from SQLite
@app.get("/tasks/{user_id}", response_model=List[Task])
async def get_tasks(user_id: str, db: Session = Depends(get_db)):
    # Ask SQLAlchemy to query the database for all tasks
    tasks = db.query(db_models.DBTAsk).all()
    return tasks

# 4. POST Endpoint: Create a Task in SQLite
@app.post("/tasks/{user_id}")
async def create_task(user_id: str, task: Task, db: Session = Depends(get_db)):
    # Step A : Convert the validated Pydantic model into a Database model
    db_task = db_models.DBTask(
        task_id = task.task_id,
        task_name = task.task_name, 
        description = task.description,
        estimated_duration_minutes = task.estimated_duration_minutes,
        status = task.status,
        type = task.type, 
        cognitive_load = task.cognitive_load,
        deadline = str(task.deadline) if task.deadline else None
    )

    # Step b : Save it to the hard drive
    db.add(db_task)         # Stages the data
    db.commit()             # Actually writes it ti the database file
    db.refresh(db_task)     # Refreshes the variable with the new data

    return {"message": "Task successfully saved to database", "task_id": db_task.task_id}

# 5. GET Endpoint: Retrieve Daily Check-ins
@app.get("/checkins/{user_id}", response_model=List[DailyCheckIn])
async def get_checkins(user_id: str, db: Session = Depends(get_db)):
    # Filter the database to only return check-ins for this specific user
    checkins = db.query(db_models.DBDailyCheckIn).filter(db_models.DBDailyCheckIn.user_id == user_id).all()
    return checkins

# 6. POST Endpoint: Create a Daily Check-in
@app.post("/checkins/{user_id}")
async def create_checkin(user_id:str, checkin: DailyCheckIn, db: Session = Depends(get_db)):
    # Convert Pydantic model to SQLAlchemy database model
    db_checkin = db_models.DBDailyCheckIn(
        checkin_id = checkin.checkin_id,
        user_id = user_id,
        timestamp = str(checkin.timestamp),
        mood = checkin.mood,
        energy_level = checkin.energy_level,
        focus_level = checkin.focus_level,
        stress_level = checkin.stress_level,
        sleep_quality = checkin.sleep_quality,
        physical_comfort = checkin.physical_comfort,
        excitement_to_work = checkin.excitement_to_work,
        notes = checkin.notes
    )

    # Save to the database
    db.add(db_checkin)         
    db.commit()             
    db.refresh(db_checkin)

    return {"message": "Daily check-in securely logged!", "checkin_id": db_checkin.checkin_id}

# 7. POST Endpoint: Analyze Task Cognitive Load via Gemini
@app.post("/tasks/{task_id}/analyze")
async def analyze_task(task_id: str, db: Session = Depends(get_db)):
    # 1. Fetch the specific task from SQLite database
    task = db.query(db_models.DBTask).filter(db_models.DBTask.task_id == task_id).first()

    # If the task doesn't exist, throw a 404 error
    if not task:
        raise HTTPException(status_code=404, detail="Task not found in database.")

    # 2. Hand the data over the AI Service
    # Using 'await' because Gemini takes a second to generate the response
    task_description = task.description if task.description else "No description provided."
    ai_insight = await analyze_task_complexity(task.task_name, task_description)

    # 3. Return the AI's analysis to the user
    return{
        "task_id": task.task_id,
        "task_name": task.task_name,
        "ai_cognitive_analysis": ai_insight
    }

# 8. GET Endpoint: AI Synthesis of User Trends
@app.get("/users/{user_id}/synthesis")
async def synthesis_insights(user_id: str, db: Session = Depends(get_db)):
    # 1. Fetch both datasets using SQLAlchemy
    user_checkins = db.query(db_models.DBDailyCheckIn).filter(db_models.DBDailyCheckIn.user_id == user_id).all()
    user_tasks = db.query(db_models.DBTask).all() # Grabbing all tasks for the demo

    # 2. Compress the data so it won't overwhelm the AI context window
    tasks_text = str([{"name": t.task_name, "load": t.cognitive_load} for t in user_tasks])
    checkins_text = str([{"energy": c.energy_level, "sleep": c.sleep_quality} for c in user_checkins])

    # 3. Stream to Gemini and wait for the JSON response
    insight_json = await synthesize_user_data(tasks_text, checkins_text)

    return {
        "user_id": user_id,
        "synthesis_engine": insight_json
    }