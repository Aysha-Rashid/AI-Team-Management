from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import datetime

from data_pipeline import EmployeeData
from ai_engine import ProjectRequirement, TeamFormationEngine

app = FastAPI(title="AI Team Formation Assistant")

class EmployeeCreate(BaseModel):
    employee_id: str
    name: str
    current_role: str
    department: str
    skills: List[str]
    experience_years: float
    availability: float
    projects: List[Dict]
    feedback: List[Dict]
    cv_text: str
    personality_traits: Optional[Dict] = None

class ProjectRequirementCreate(BaseModel):
    role: str
    required_skills: List[str]
    experience_level: float
    personality_traits: Optional[List[str]]
    team_size: int
    project_type: str
    budget: Optional[float] = None
    timeline_months: Optional[int] = None
    department_constraints: Optional[Dict[str, int]] = None
    seniority_mix: Optional[Dict[str, int]] = None

class TeamSuggestion(BaseModel):
    team: List[Dict]
    total_cost: float
    skill_coverage: Dict
    team_balance_score: float

class FeedbackSubmit(BaseModel):
    team_suggestion_id: str
    feedback_type: str  # 'accept', 'reject', 'modify'
    comments: str
    modifications: Optional[Dict] = None

class WhatIfScenario(BaseModel):
    original_team_id: str
    modified_params: Dict

# Initialize components
config = {
    'hr_systems': {
        'workday': {'api_key': 'YOUR_KEY'},
        'sap': {'api_key': 'YOUR_KEY'},
        'oracle': {'api_key': 'YOUR_KEY'}
    },
    'novita_ai': {'api_key': 'sk_HLLVkOXU0z_FlKPx9_D2Jt1R0IME_AWz075iMdRtZTM'},
    'milvus': {
        'host': 'localhost',
        'port': 19530
    },
    'project_tools': {
        'jira': {'api_key': 'YOUR_KEY'},
        'asana': {'api_key': 'YOUR_KEY'}
    }
}

team_engine = TeamFormationEngine(config)

@app.post("/employees/", response_model=Dict)
async def create_employee(employee: EmployeeCreate):
    """Add a new employee to the system"""
    try:
        employee_data = EmployeeData(**employee.dict())
        # Process and store employee data
        team_engine.data_pipeline.ingest_employee_data(employee_data)
        return {"status": "success", "message": f"Employee {employee.name} added successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/suggest-team/", response_model=TeamSuggestion)
async def suggest_team(requirement: ProjectRequirementCreate):
    """Get team suggestions based on project requirements"""
    try:
        project_req = ProjectRequirement(**requirement.dict())
        suggestion = team_engine.suggest_team(project_req)
        return suggestion
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/what-if-scenario/", response_model=TeamSuggestion)
async def generate_what_if_scenario(scenario: WhatIfScenario):
    """Generate alternative team composition based on modified parameters"""
    try:
        alternative_team = team_engine.team_composer.generate_what_if_scenario(
            scenario.original_team_id,
            scenario.modified_params
        )
        return alternative_team
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/feedback/", response_model=Dict)
async def submit_feedback(feedback: FeedbackSubmit):
    """Submit feedback on team suggestions"""
    try:
        team_engine.process_feedback(
            feedback.team_suggestion_id,
            feedback.dict()
        )
        return {"status": "success", "message": "Feedback processed successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/employees/{employee_id}/availability")
async def get_employee_availability(employee_id: str):
    """Get employee's current availability"""
    try:
        # TODO: Implement availability check
        return {"employee_id": employee_id, "availability": 0.0}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.put("/employees/{employee_id}/availability")
async def update_employee_availability(employee_id: str, availability: float):
    """Update employee's availability"""
    try:
        # TODO: Implement availability update
        return {"status": "success", "message": f"Availability updated for employee {employee_id}"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/skills/")
async def get_available_skills():
    """Get list of all skills in the system"""
    try:
        # TODO: Implement skill retrieval
        return {"skills": []}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/projects/types/")
async def get_project_types():
    """Get list of available project types"""
    try:
        # TODO: Implement project type retrieval
        return {"project_types": []}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/departments/constraints/")
async def get_department_constraints():
    """Get current department constraints"""
    try:
        # TODO: Implement department constraints retrieval
        return {"constraints": {}}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)