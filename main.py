from fastapi import FastAPI, Request, HTTPException, Query
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from database import get_meeting_by_id

# Import the mock database and AI logic you just built
import database
import ai_service

app = FastAPI(title="Fathom AI Clone")

# Mount the static directory to serve CSS and our mock video files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configure the Jinja2 templates directory
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Render the main dashboard, defaulting to the first meeting in the database."""
    meetings_list = database.get_all_meetings()
    
    # If the DB is somehow empty, return a blank template safely
    if not meetings_list:
        return templates.TemplateResponse(
            request=request, name="index.html", context={"meetings": []}
        )
    
    # Default to loading the first meeting in the sidebar
    default_meeting = database.get_meeting_by_id(meetings_list[0]["id"])
    
    return templates.TemplateResponse(
        request=request, 
        name="index.html", 
        context={
            "meetings": meetings_list, 
            "active_meeting": default_meeting
        }
    )

@app.get("/meetings/{meeting_id}", response_class=HTMLResponse)
async def get_meeting(request: Request, meeting_id: str):
    """Render the dashboard when a user clicks a specific historical meeting in the sidebar."""
    meetings_list = database.get_all_meetings()
    meeting = database.get_meeting_by_id(meeting_id)
    
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")
        
    return templates.TemplateResponse(
        request=request, 
        name="index.html", 
        context={
            "meetings": meetings_list, 
            "active_meeting": meeting
        }
    )

@app.post("/meetings/{meeting_id}/regenerate")
async def regenerate_insights(meeting_id: str, template: str = Query("default")):
    # Use the helper function from your database.py
    meeting = get_meeting_by_id(meeting_id) 
    
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")
    
    try:
        insights = ai_service.generate_meeting_intelligence(meeting["raw_transcript"], template)
        return insights
    except Exception as e:
        print(f"CRITICAL ERROR in /regenerate: {e}") # This will print the exact issue to your terminal
        raise HTTPException(status_code=500, detail=str(e))