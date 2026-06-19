from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
    "static")), name="static")

# In-memory activity database (4 activities total)
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Coding Club": {
        "description": "Learn programming and build cool projects",
        "schedule": "Mondays, 4:00 PM - 5:30 PM",
        "max_participants": 15,
        "participants": []
    },
    "Music Ensemble": {
        "description": "Practice and perform classical and modern music",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 20,
        "participants": []
    },
    "Photography Club": {
        "description": "Learn the basics of photography and lighting",
        "schedule": "Thursdays, 4:00 PM - 5:00 PM",
        "max_participants": 10,
        "participants": []
    }
}

@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    activity = activities[activity_name]
    
    # NORMALIZACIÓN: Convertimos el email ingresado a minúsculas para evitar duplicados por mayúsculas
    email_normalizado = email.lower()
    
    # Validamos usando la versión en minúsculas
    if email_normalizado in [p.lower() for p in activity.get("participants", [])]:
        raise HTTPException(status_code=400, detail="Student already registered")
        
    if len(activity["participants"]) >= activity["max_participants"]:
        raise HTTPException(status_code=400, detail="Activity is full")
        
    activity["participants"].append(email_normalizado)
    return {"message": "Successfully signed up"}

@app.delete("/activities/{activity_name}/participants")
def unregister_participant(activity_name: str, email: str):
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    activity = activities[activity_name]
    email_normalizado = email.lower()

    registered = [participant.lower() for participant in activity.get("participants", [])]
    if email_normalizado not in registered:
        raise HTTPException(status_code=404, detail="Student not registered")

    activity["participants"] = [participant for participant in activity["participants"] if participant.lower() != email_normalizado]
    return {"message": f"Removed {email_normalizado} from {activity_name}"}
