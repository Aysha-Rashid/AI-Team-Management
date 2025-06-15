from typing import Dict, List, Optional
from dataclasses import dataclass
import numpy as np
from datetime import datetime
from team_composer import TeamComposer, TeamConstraints

@dataclass
class ProjectRequirement:
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

class TeamFormationEngine:
    def __init__(self, config: Dict):
        self.config = config
        self.vector_store = None  # Milvus client
        self.llm_client = None    # Novita.ai client
        self.team_composer = TeamComposer(config)

    def generate_role_vector(self, requirement: ProjectRequirement) -> List[float]:
        """Generate vector embedding for ideal candidate based on requirements"""
        role_description = f"""
        Role: {requirement.role}
        Required Skills: {', '.join(requirement.required_skills)}
        Experience Level: {requirement.experience_level} years
        Personality Traits: {', '.join(requirement.personality_traits or [])}
        Project Type: {requirement.project_type}
        """
        # TODO: Use Novita.ai to generate embedding
        return []

    def search_candidates(self, role_vector: List[float], requirement: ProjectRequirement) -> List[Dict]:
        """Search for matching candidates in Milvus with constraints"""
        # Initial vector similarity search
        search_params = {
            'vector': role_vector,
            'filters': {
                'availability': {'$gte': 0.5},  # At least 50% available
                'experience_years': {'$gte': requirement.experience_level}
            }
        }
        
        # Get initial candidates from vector store
        candidates = []  # TODO: Implement Milvus search
        
        # Apply team composition constraints
        constraints = TeamConstraints(
            max_per_department=requirement.department_constraints or {},
            min_experience_years=requirement.experience_level * 0.8,  # Allow some flexibility
            max_experience_years=requirement.experience_level * 1.5,
            required_seniority_mix=requirement.seniority_mix or {},
            max_workload=0.8  # Maximum 80% workload per person
        )
        
        filtered_candidates = self.team_composer.apply_constraints(candidates, constraints)
        return filtered_candidates

    def generate_match_explanation(self, candidate: Dict, requirement: ProjectRequirement) -> str:
        """Generate natural language explanation for the match using Novita.ai"""
        prompt = f"""
        Analyze the fit between the candidate and the role requirements:
        
        Role Requirements:
        - Position: {requirement.role}
        - Required Skills: {', '.join(requirement.required_skills)}
        - Experience Level: {requirement.experience_level} years
        - Desired Traits: {', '.join(requirement.personality_traits or [])}
        
        Candidate Profile:
        - Current Role: {candidate['current_role']}
        - Skills: {', '.join(candidate['skills'])}
        - Experience: {candidate['experience_years']} years
        - Project History: {candidate['projects']}
        - Feedback Highlights: {candidate['feedback']}
        
        Provide a detailed analysis of:
        1. Why this person is a good fit
        2. Any potential gaps or areas for development
        3. Specific examples from their experience that match the requirements
        4. Team collaboration potential
        5. Workload and availability considerations
        """
        # TODO: Use Novita.ai to generate explanation
        return ""

    def suggest_team(self, requirement: ProjectRequirement) -> Dict:
        """Main method to suggest a team based on project requirements"""
        # Generate vector for ideal candidate
        role_vector = self.generate_role_vector(requirement)
        
        # Search for matching candidates with constraints
        candidates = self.search_candidates(role_vector, requirement)
        
        # Optimize team composition
        optimized_team = self.team_composer.optimize_seniority_mix(
            candidates, 
            requirement.seniority_mix or {}
        )
        
        # Generate explanations for each team member
        team_with_explanations = [
            {
                **candidate,
                'explanation': self.generate_match_explanation(candidate, requirement),
                'role_fit_score': self._calculate_role_fit(candidate, requirement)
            }
            for candidate in optimized_team
        ]
        
        # Create project tasks and notify team members
        if requirement.budget and requirement.timeline_months:
            project_details = {
                'name': f"{requirement.role} Team - {requirement.project_type}",
                'start_date': datetime.now().strftime('%Y-%m-%d'),
                'budget': requirement.budget,
                'duration_months': requirement.timeline_months
            }
            self.team_composer.create_project_tasks(team_with_explanations, project_details)
            self.team_composer.notify_team_members(team_with_explanations, project_details)
        
        return {
            'team': team_with_explanations,
            'total_cost': self._calculate_team_cost(team_with_explanations),
            'skill_coverage': self._analyze_skill_coverage(team_with_explanations, requirement),
            'team_balance_score': self._calculate_team_balance(team_with_explanations)
        }

    def _calculate_role_fit(self, candidate: Dict, requirement: ProjectRequirement) -> float:
        """Calculate how well a candidate fits the role requirements"""
        # TODO: Implement role fit calculation
        return 0.0

    def _calculate_team_cost(self, team: List[Dict]) -> float:
        """Calculate the total cost of the team"""
        # TODO: Implement cost calculation logic
        return 0.0

    def _analyze_skill_coverage(self, team: List[Dict], requirement: ProjectRequirement) -> Dict:
        """Analyze how well the team covers required skills"""
        # TODO: Implement skill coverage analysis
        return {}

    def _calculate_team_balance(self, team: List[Dict]) -> float:
        """Calculate team balance score based on experience and skills distribution"""
        # TODO: Implement team balance calculation
        return 0.0

    def process_feedback(self, team_suggestion: Dict, feedback: Dict):
        """Process feedback for continuous improvement"""
        self.team_composer.store_feedback(team_suggestion['team'], feedback)
        # TODO: Implement feedback-based model refinement