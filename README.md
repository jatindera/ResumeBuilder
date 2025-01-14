# Resume Builder API 🚀

A modern FastAPI-based backend service for creating and managing professional resumes with ease.

## 📋 Features

- Create and manage multiple resumes
- Structured data model for education, experience, and skills
- JSON-based API with automatic validation
- Interactive API documentation
- Easy to extend and customize

## 🛠️ Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git

## 🚀 Quick Start

### 1. Clone the Repository

git clone https://github.com/jatindera/ResumeBuilder.git
cd ResumeBuilder

### 2. Backend Setup

# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# For Windows:
.venv\Scripts\activate
# For Unix/MacOS:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

### 3. Environment Setup

# Copy the environment template
cp .env.template .env

# Edit .env with your configurations
# Required variables:
# - DATABASE_URL
# - SECRET_KEY
# - API_VERSION

### 4. Run the Application

# Make sure you're in the backend directory with activated virtual environment
uvicorn app.main:app --reload --port 8000

## 📚 API Documentation

Once the server is running, access the interactive API documentation:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Key Endpoints

#### Resume Management
- GET /api/v1/ - List all resumes
- POST /api/v1/ - Create a new resume

Example POST request:

{
  "full_name": "John Doe",
  "email": "john@example.com",
  "phone": "+1234567890",
  "summary": "Senior Software Engineer with 5+ years of experience",
  "education": [
    {
      "institution": "University of Technology",
      "degree": "Master's",
      "field_of_study": "Computer Science",
      "start_date": "2018-09",
      "end_date": "2020-05",
      "grade": "3.8 GPA"
    }
  ],
  "experience": [
    {
      "company": "Tech Corp",
      "position": "Senior Developer",
      "start_date": "2020-06",
      "end_date": "Present",
      "description": [
        "Led team of 5 developers",
        "Implemented microservices architecture",
        "Reduced system response time by 40%"
      ]
    }
  ],
  "skills": [
    {
      "category": "Programming",
      "skills": ["Python", "JavaScript", "SQL"]
    },
    {
      "category": "Frameworks",
      "skills": ["FastAPI", "React", "Docker"]
    }
  ]
}

## 📁 Project Structure

backend/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── api/
│   │   ├── endpoints/
│   │   │   ├── resume.py
│   │   │   └── ...
│   ├── core/
│   │   ├── config.py
│   │   └── ...
│   ├── models/
│   └── schemas/
├── tests/
├── .env.template
└── requirements.txt

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (git checkout -b feature/AmazingFeature)
3. Commit your changes (git commit -m 'Add: Amazing Feature')
4. Push to the branch (git push origin feature/AmazingFeature)
5. Open a Pull Request

## 🐛 Bug Reports

If you find a bug, please open an issue with:
- Clear bug description
- Steps to reproduce
- Expected behavior
- Screenshots (if applicable)

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📬 Contact

Project Link: https://github.com/jatindera/ResumeBuilder