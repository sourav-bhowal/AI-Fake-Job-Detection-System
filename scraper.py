import requests
from bs4 import BeautifulSoup
import re

# Scrape job details from a given URL
def scrape_job(url: str):
    # Make a GET request to the URL
    res = requests.get(url, timeout=10)
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(res.text, "html.parser")

    # Extract the text content from the page
    text = soup.get_text(separator=" ")

    # Return a dictionary with the job description, salary, and email
    return {
        "description": text[:5000],  # truncate
        "salary": extract_salary(text),
        "email": extract_email(text)
    }

# Helper function to extract salary from text
def extract_salary(text):
    """Extract salary information from text, supporting various formats."""
    # Try to find salary ranges like $55,000-$100,000 or $55000-$100000
    range_match = re.search(r'[\$\u20b9]?\s*(\d{1,3}(?:,\d{3})*|\d+)\s*[-\u2013]\s*[\$\u20b9]?\s*(\d{1,3}(?:,\d{3})*|\d+)', text)
    if range_match:
        return f"₹{range_match.group(1)}-₹{range_match.group(2)}"
    
    # Try to find single salary values
    single_match = re.search(r'[\$\u20b9]\s*(\d{1,3}(?:,\d{3})*|\d{4,})', text)
    if single_match:
        return single_match.group(0)
    
    # Try "per week/month/year" patterns
    period_match = re.search(r'(\d{1,3}(?:,\d{3})*|\d+)\s*(?:per|/)\s*(?:week|month|year|hr|hour)', text, re.IGNORECASE)
    if period_match:
        return period_match.group(0)
    
    return None

# Helper function to extract email from text
def extract_email(text):
    """Extract email address from text."""
    # More robust email pattern
    match = re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)
    return match.group() if match else None