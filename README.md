# MindGage API Infrastructure

A production-ready FastAPI backend designed to ingest, validate, and synthesize human physiological metrics and cognitive load data using Google's Gemini AI. 

This project demonstrates a complete, containerized machine learning backend built with a focus on enterprise reliability, strict data validation, and automated testing.

## 🏗️ System Architecture

* **Framework:** FastAPI (Asynchronous Python)
* **Intelligence Layer:** Google Gemini 3.6 Flash API 
* **Database:** SQLite with SQLAlchemy ORM
* **Data Validation:** Pydantic
* **MLOps / Deployment:** Docker
* **Testing:** Pytest & HTTPX

## ✨ Key Features

* **AI-Driven Data Synthesis:** Integrates LLMs directly into the backend workflow to analyze the relationship between task complexity and physiological check-ins, forcing strict JSON responses for seamless frontend consumption.
* **Bulletproof Data Validation:** Utilizes Pydantic models to strictly enforce data types and logical constraints (e.g., capping energy levels at 5), automatically throwing `422 Unprocessable Entity` errors for bad payloads.
* **Relational Database Management:** Employs SQLAlchemy to manage normalized tables (`tasks` and `daily_checkins`), demonstrating robust primary/foreign key relationships and transaction rollbacks.
* **Containerized Environment:** Fully packaged using Docker, separating the application runtime from the local OS and securely injecting API credentials at runtime.
* **Automated CI/CD Testing:** Includes a Pytest suite simulating API attacks and database unique-constraint validations to guarantee system stability before deployment.

## 🚀 Quick Start (Docker)

The easiest way to run this API is via Docker, which guarantees an identical environment on any machine.

**1. Clone the repository and navigate to the project folder:**
```bash
git clone [https://github.com/BARAAABID/MindGage-Infrastructure.git](https://github.com/BARAAABID/MindGage-Infrastructure.git)
cd MindGage-Infrastructure/backend
```

**2. Configure your environment variables:**
Create a `.env` file in the root directory and add your Gemini API key:
```env
GEMINI_API_KEY=your_actual_api_key_here
```

**3. Build and run the container:**
```bash
docker build -t mindgage-api .
docker run -d --name mindgage-server -p 8000:8000 --env-file .env mindgage-api
```

**4. Access the API Documentation:**
Open your browser and navigate to `http://localhost:8000/docs` to view the interactive Swagger UI.

## 🧪 Running Automated Tests

To verify the structural integrity of the API and database constraints, run the Pytest suite locally:

```bash
pip install -r requirements.txt
pytest
```

## 👤 Author
**Baraa Abid**  
Computer Engineering Graduate | Backend & AI Engineering
