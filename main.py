from fastapi import FastAPI
from pydantic import BaseModel
from scraper import scrape_job
from risk_engine import compute_risk

# Initialize FastAPI app
app = FastAPI()

class JobRequest(BaseModel):
    url: str

# API endpoint to analyze a job posting
@app.post("/analyze")
def analyze_job(req: JobRequest):
    # Scrape job details from the provided URL
    job = scrape_job(req.url)

    # Compute risk score based on job details
    score = compute_risk(
        job["description"],
        job["salary"],
        job["email"]
    )

    return {
        "risk_score": score,
        "level": risk_level(score),
        "details": job
    }

# Helper function to determine risk level based on score
def risk_level(score):
    if score < 30:
        return "Safe"
    elif score < 60:
        return "Medium Risk"
    else:
        return "High Risk"