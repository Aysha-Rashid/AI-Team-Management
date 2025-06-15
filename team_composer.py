from typing import Dict, List, Optional
from dataclasses import dataclass
import json

@dataclass
class TeamConstraints:
    max_per_department: Dict[str, int]
    min_experience_years: float
    max_experience_years: float
    required_seniority_mix: Dict[str, int]  # e.g., {"senior": 2, "mid": 2, "junior": 1}
    max_workload: float  # maximum allowed workload percentage per person

class TeamComposer:
    def __init__(self, config: Dict):
        self.config = config
        self.project_tools = {}
        self.feedback_store = []

    def initialize_project_tools(self):
        """Initialize connections to project management tools"""
        # TODO: Implement connections to Jira, Asana, etc.
        pass

    def apply_constraints(self, candidates: List[Dict], constraints: TeamConstraints) -> List[Dict]:
        """Apply team composition constraints to candidate list"""
        filtered_candidates = []
        department_counts = {}

        for candidate in candidates:
            # Check department constraints
            dept = candidate['department']
            if dept in constraints.max_per_department:
                if department_counts.get(dept, 0) >= constraints.max_per_department[dept]:
                    continue
                department_counts[dept] = department_counts.get(dept, 0) + 1

            # Check experience constraints
            if not (constraints.min_experience_years <= candidate['experience_years'] <= 
                   constraints.max_experience_years):
                continue

            # Check workload
            if candidate['availability'] > constraints.max_workload:
                continue

            filtered_candidates.append(candidate)

        return filtered_candidates

    def optimize_seniority_mix(self, candidates: List[Dict], 
                             required_mix: Dict[str, int]) -> List[Dict]:
        """Optimize team composition based on seniority requirements"""
        # TODO: Implement seniority-based team optimization
        return candidates

    def generate_what_if_scenario(self, base_team: List[Dict], 
                                modified_params: Dict) -> List[Dict]:
        """Generate alternative team compositions based on modified parameters"""
        # Create new constraints with modified parameters
        new_constraints = TeamConstraints(**modified_params)
        
        # Apply new constraints to generate alternative team
        alternative_team = self.apply_constraints(base_team, new_constraints)
        return alternative_team

    def store_feedback(self, team_suggestion: List[Dict], feedback: Dict):
        """Store feedback for future model refinement"""
        feedback_entry = {
            'timestamp': str(datetime.now()),
            'team_suggestion': team_suggestion,
            'feedback': feedback
        }
        self.feedback_store.append(feedback_entry)
        # TODO: Implement feedback processing for model refinement

    def create_project_tasks(self, team: List[Dict], project_details: Dict):
        """Create tasks in project management tools"""
        for tool_name, tool_client in self.project_tools.items():
            if tool_name == 'jira':
                self._create_jira_tasks(team, project_details)
            elif tool_name == 'asana':
                self._create_asana_tasks(team, project_details)

    def _create_jira_tasks(self, team: List[Dict], project_details: Dict):
        """Create tasks in Jira"""
        # TODO: Implement Jira task creation
        pass

    def _create_asana_tasks(self, team: List[Dict], project_details: Dict):
        """Create tasks in Asana"""
        # TODO: Implement Asana task creation
        pass

    def notify_team_members(self, team: List[Dict], project_details: Dict):
        """Send notifications to selected team members"""
        for member in team:
            notification = self._generate_notification(member, project_details)
            self._send_notification(member['email'], notification)

    def _generate_notification(self, member: Dict, project_details: Dict) -> str:
        """Generate personalized notification message"""
        return f"""Hi {member['name']},

You have been selected for the project: {project_details['name']}
Role: {member['assigned_role']}
Start Date: {project_details['start_date']}

Please review the project details in your project management dashboard.
"""

    def _send_notification(self, email: str, message: str):
        """Send notification to team member"""
        # TODO: Implement notification sending logic
        pass