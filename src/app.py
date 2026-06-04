"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

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

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Soccer Team": {
        "description": "Team practices and matches to develop soccer skills",
        "schedule": "Mondays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 18,
        "participants": ["nina@mergington.edu", "ryan@mergington.edu"]
    },
    "Swim Club": {
        "description": "Swim training and water safety for all skill levels",
        "schedule": "Tuesdays and Fridays, 3:45 PM - 5:00 PM",
        "max_participants": 16,
        "participants": ["lisa@mergington.edu", "alex@mergington.edu"]
    },
    "Art Workshop": {
        "description": "Explore drawing, painting, and mixed media projects",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 14,
        "participants": ["mia@mergington.edu", "zach@mergington.edu"]
    },
    "Drama Club": {
        "description": "Practice acting and put on school performances",
        "schedule": "Tuesdays, 4:00 PM - 5:30 PM",
        "max_participants": 20,
        "participants": ["sara@mergington.edu", "leo@mergington.edu"]
    },
    "Science Olympiad": {
        "description": "Compete in science and engineering challenges",
        "schedule": "Mondays, 4:00 PM - 5:30 PM",
        "max_participants": 15,
        "participants": ["oliver@mergington.edu", "nora@mergington.edu"]
    },
    "Debate Team": {
        "description": "Build public speaking and critical thinking skills",
        "schedule": "Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 18,
        "participants": ["emma@mergington.edu", "jack@mergington.edu"]
    }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")

def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Add student
    # Validate student is not already signed up 
    if email in activity["participants"]:
        raise HTTPException(status_code=400, detail="Student already signed up for this activity")
    
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}


@app.delete("/activities/{activity_name}/signup")
def remove_participant(activity_name: str, email: str):
    """Remove a student from an activity"""
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    activity = activities[activity_name]
    normalized_email = email.strip().lower()

    participant_index = next(
        (index for index, participant in enumerate(activity["participants"])
         if participant.strip().lower() == normalized_email),
        None
    )

    if participant_index is None:
        raise HTTPException(status_code=404, detail="Participant not found")

    removed_email = activity["participants"].pop(participant_index)
    return {"message": f"Removed {removed_email} from {activity_name}"}
