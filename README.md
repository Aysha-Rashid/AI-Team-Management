# AI-Driven Team Formation Assistant

An intelligent system that leverages AI to optimize team formation by analyzing employee data, skills, and project requirements.

## Features

- **Data Integration**: Seamless integration with HR systems (Workday, SAP, Oracle HCM)
- **AI-Powered Matching**: Advanced role-fit matching using vector embeddings
- **Smart Team Composition**: Optimized team suggestions considering multiple factors
- **Explainable Recommendations**: Detailed explanations for team member selections
- **Real-time Updates**: Dynamic availability tracking and team adjustments

## Architecture

### Components

1. **Data Pipeline** (`data_pipeline.py`)
   - Ingests employee data from various sources
   - Processes CVs and feedback using Novita.ai
   - Generates and stores vector embeddings in Milvus

2. **AI Engine** (`ai_engine.py`)
   - Handles role-fit matching
   - Optimizes team composition
   - Generates match explanations

3. **API Layer** (`api.py`)
   - FastAPI-based REST API
   - Endpoints for team suggestions and employee management

## Setup

1. **Environment Setup**

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows
venv\Scripts\activate
# Unix/MacOS
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

2. **Configuration**

Create a `.env` file in the project root:

```env
# HR System API Keys
WORKDAY_API_KEY=your_key
SAP_API_KEY=your_key
ORACLE_API_KEY=your_key

# Novita.ai API Key
NOVITA_API_KEY=your_key

# Milvus Configuration
MILVUS_HOST=localhost
MILVUS_PORT=19530
```

3. **Database Setup**

```bash
# Start Milvus (using Docker)
docker-compose up -d
```

## Usage

1. **Start the API Server**

```bash
python api.py
```

2. **API Endpoints**

- `POST /employees/`: Add new employee
- `POST /suggest-team/`: Get team suggestions
- `GET /employees/{employee_id}/availability`: Check employee availability
- `PUT /employees/{employee_id}/availability`: Update availability
- `GET /skills/`: List available skills
- `GET /projects/types/`: List project types

## Example API Usage

```python
# Request team suggestion
import requests

project_requirement = {
    "role": "Lead Developer",
    "required_skills": ["Python", "AI/ML", "Team Leadership"],
    "experience_level": 5.0,
    "personality_traits": ["collaborative", "innovative"],
    "team_size": 5,
    "project_type": "AI Product Development",
    "timeline_months": 6
}

response = requests.post(
    "http://localhost:8000/suggest-team/",
    json=project_requirement
)

team_suggestion = response.json()
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.