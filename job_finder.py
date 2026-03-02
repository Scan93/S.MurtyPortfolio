"""
Job Finder for S. Dean Murty
- Searches Adzuna + Arbeitnow for jobs near Chandler, AZ
- Scores each job against your resume using Claude AI
- Emails you a daily digest of matches scoring 8/10 or higher

SETUP INSTRUCTIONS (one-time):
1. Install dependencies:
   pip install requests anthropic python-dotenv

2. Create a free Adzuna account at: https://developer.adzuna.com/
   - Get your App ID and App Key

3. Create a free Anthropic account at: https://console.anthropic.com/
   - Get your API key (pay-per-use, very cheap — pennies per day)

4. Create a Gmail App Password:
   - Go to myaccount.google.com > Security > 2-Step Verification > App Passwords
   - Generate a password for "Mail"

5. Create a file called .env in the same folder as this script with:
   ADZUNA_APP_ID=your_app_id_here
   ADZUNA_APP_KEY=your_app_key_here
   ANTHROPIC_API_KEY=your_anthropic_key_here
   GMAIL_APP_PASSWORD=your_gmail_app_password_here

6. Run the script:
   python job_finder.py

TO RUN AUTOMATICALLY EVERY DAY (Windows):
- Open Task Scheduler
- Create a Basic Task
- Set trigger to Daily at your preferred time
- Set action to run: python path\to\job_finder.py
"""

import os
import smtplib
import requests
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
import anthropic

load_dotenv()

# ── Configuration ──────────────────────────────────────────────────────────────

RESUME = """
Name: S. Dean Murty
Location: Chandler, AZ

PROFILE:
Data Analyst with 2+ years of experience in aerospace production at General Dynamics Mission Systems.
Built an automated inventory system that improved tracking accuracy and reduced manual effort.
Proficient in SQL, Tableau, and advanced Excel, with a focus on supporting data-driven decision-making
across cross-functional teams.

EDUCATION:
- A.A.S in Data Analytics, Mesa Community College (Expected Fall 2026) | 3.9 GPA | Dean's List
- Planned transfer for B.S. in Data Science
- Google Data Analyst Certification (Completed Aug 2024)

SKILLS:
SQL, Excel (Advanced), Tableau, Production Planning, Data Integrity, Microsoft Office

EXPERIENCE:
- Senior Production Operator II | General Dynamics Mission Systems | Apr 2023 – Feb 2026
  * Maintained 99.8% quality compliance across life-critical space hardware
  * Created automated material inventory system: +25% accuracy, saved 4 hrs/week
  * Assisted mechanical engineering with design schematics, reduced rework by 15%

- Inbound Associate | Target | Aug 2022 – Mar 2023
  * Maintained 98% inventory accuracy

- Supervisor | Hertz 76 | Feb 2014 – Sep 2021
  * Trained 20+ new hires
  * Managed inventory, parts sourcing, equipment maintenance (reduced downtime 20%)
  * Increased average weekly transaction value by 15%
"""

EXCLUDED_COMPANIES = ["general dynamics", "general dynamics mission systems", "gdms"]

YOUR_EMAIL = os.getenv("YOUR_EMAIL")
FROM_EMAIL = os.getenv("YOUR_EMAIL")

# Chandler, AZ coordinates
LATITUDE = 33.3062
LONGITUDE = -111.8413
RADIUS_MILES = 25
RESULTS_PER_PAGE = 50
MIN_SCORE = 8  # Only include jobs scoring 8/10 or higher

# ── Fetch Jobs from Adzuna ─────────────────────────────────────────────────────

def fetch_adzuna_jobs():
    app_id = os.getenv("ADZUNA_APP_ID")
    app_key = os.getenv("ADZUNA_APP_KEY")

    search_terms = [
        "data analyst",
        "data analyst SQL",
        "business analyst",
        "operations analyst",
        "inventory analyst",
        "reporting analyst",
        "AI analyst",
        "data coordinator",
    ]

    all_jobs = {}

    for term in search_terms:
        url = (
            f"https://api.adzuna.com/v1/api/jobs/us/search/1"
            f"?app_id={app_id}&app_key={app_key}"
            f"&results_per_page={RESULTS_PER_PAGE}"
            f"&what={requests.utils.quote(term)}"
            f"&where=Chandler%2C+AZ"
            f"&distance={RADIUS_MILES}"
            f"&sort_by=date"
            f"&content-type=application/json"
        )

        try:
            response = requests.get(url, timeout=10)
            data = response.json()
            for job in data.get("results", []):
                job_id = job.get("id")
                company = job.get("company", {}).get("display_name", "")
                if any(exc in company.lower() for exc in EXCLUDED_COMPANIES):
                    continue
                if job_id and job_id not in all_jobs:
                    all_jobs[job_id] = {
                        "id": job_id,
                        "title": job.get("title", "N/A"),
                        "company": company,
                        "location": job.get("location", {}).get("display_name", "N/A"),
                        "description": job.get("description", ""),
                        "url": job.get("redirect_url", "#"),
                        "salary_min": job.get("salary_min"),
                        "salary_max": job.get("salary_max"),
                        "source": "Adzuna",
                    }
        except Exception as e:
            print(f"   Adzuna error for '{term}': {e}")

    return list(all_jobs.values())

# ── Fetch Jobs from Arbeitnow (no API key needed) ─────────────────────────────

def fetch_arbeitnow_jobs():
    """
    Arbeitnow is a free job board API with no API key or account required.
    Pulls remote and US-based tech/data jobs.
    """
    search_terms = [
        "data analyst",
        "business analyst",
        "data coordinator",
        "AI specialist",
        "operations analyst",
    ]

    all_jobs = {}

    for term in search_terms:
        url = f"https://www.arbeitnow.com/api/job-board-api?search={requests.utils.quote(term)}"
        try:
            response = requests.get(url, timeout=10)
            data = response.json()
            for job in data.get("data", []):
                job_id = job.get("slug", "")
                company = job.get("company_name", "")
                if any(exc in company.lower() for exc in EXCLUDED_COMPANIES):
                    continue
                remote = job.get("remote", False)
                location = job.get("location", "")
                # Include remote jobs or US-based jobs only
                if not remote and "united states" not in location.lower() and "us" not in location.lower():
                    continue
                if job_id and f"arbeitnow_{job_id}" not in all_jobs:
                    all_jobs[f"arbeitnow_{job_id}"] = {
                        "id": f"arbeitnow_{job_id}",
                        "title": job.get("title", "N/A"),
                        "company": company,
                        "location": "Remote" if remote else location,
                        "description": job.get("description", "")[:1500],
                        "url": job.get("url", "#"),
                        "salary_min": None,
                        "salary_max": None,
                        "source": "Arbeitnow",
                    }
        except Exception as e:
            print(f"   Arbeitnow error for '{term}': {e}")

    return list(all_jobs.values())

# ── Score Jobs with Claude AI ──────────────────────────────────────────────────

def score_job(client, job):
    title = job.get("title", "N/A")
    company = job.get("company", "N/A")
    description = job.get("description", "No description available.")[:1500]
    location = job.get("location", "N/A")
    salary_min = job.get("salary_min")
    salary_max = job.get("salary_max")

    salary_str = ""
    if salary_min and salary_max:
        salary_str = f"${salary_min:,.0f} – ${salary_max:,.0f}/year"
    elif salary_min:
        salary_str = f"From ${salary_min:,.0f}/year"

    prompt = f"""You are a career advisor. Score how well this job matches the candidate's resume on a scale of 1-10.
Only return a JSON object with these fields: score (integer 1-10), reason (1-2 sentences explaining the match).

RESUME:
{RESUME}

JOB:
Title: {title}
Company: {company}
Location: {location}
Salary: {salary_str}
Description: {description}

Respond with only valid JSON, example: {{"score": 7, "reason": "Strong SQL and data skills match the requirements."}}"""

    try:
        message = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=150,
            messages=[{"role": "user", "content": prompt}]
        )
        import json
        raw = message.content[0].text.strip()
        print(f"      AI response: {raw[:150]}")
        raw = raw.replace("```json", "").replace("```", "").strip()
        result = json.loads(raw)
        return result.get("score", 0), result.get("reason", "")
    except Exception as e:
        print(f"   Scoring error for '{title}': {e}")
        return 0, ""

# ── Build Email HTML ───────────────────────────────────────────────────────────

def build_email(scored_jobs):
    if not scored_jobs:
        return "<p>No strong job matches found today (score 8+). Check back tomorrow!</p>"

    html = """
    <html><body style="font-family: Arial, sans-serif; max-width: 700px; margin: auto; color: #333;">
    <h2 style="color: #2c5282;">📊 Your Daily Job Matches</h2>
    <p style="color: #666;">Jobs near Chandler, AZ (+ remote) scored 8/10 or higher against your resume.</p>
    <hr>
    """

    for job, score, reason in scored_jobs:
        title = job.get("title", "N/A")
        company = job.get("company", "N/A")
        location = job.get("location", "N/A")
        url = job.get("url", "#")
        source = job.get("source", "")
        salary_min = job.get("salary_min")
        salary_max = job.get("salary_max")

        salary_str = ""
        if salary_min and salary_max:
            salary_str = f"<span style='color:#276749;'>💰 ${salary_min:,.0f} – ${salary_max:,.0f}/yr</span><br>"
        elif salary_min:
            salary_str = f"<span style='color:#276749;'>💰 From ${salary_min:,.0f}/yr</span><br>"

        score_color = "#276749" if score >= 9 else "#2b6cb0"

        html += f"""
        <div style="border:1px solid #e2e8f0; border-radius:8px; padding:16px; margin-bottom:16px;">
            <h3 style="margin:0 0 4px 0;">{title}</h3>
            <p style="margin:0; color:#555;">🏢 {company} &nbsp;|&nbsp; 📍 {location}
               &nbsp;|&nbsp; <span style="font-size:11px; color:#888;">via {source}</span></p>
            <p style="margin:4px 0;">{salary_str}</p>
            <p style="margin:4px 0;">
                <strong>Match Score: <span style="color:{score_color};">{score}/10</span></strong><br>
                <em style="color:#555;">{reason}</em>
            </p>
            <a href="{url}" style="display:inline-block; margin-top:8px; padding:8px 16px;
               background:#3182ce; color:white; text-decoration:none; border-radius:4px;">
               View Job →
            </a>
        </div>
        """

    html += "<p style='color:#999; font-size:12px;'>Powered by Adzuna + Arbeitnow + Claude AI</p></body></html>"
    return html

# ── Send Email ─────────────────────────────────────────────────────────────────

def send_email(html_content, job_count):
    password = os.getenv("GMAIL_APP_PASSWORD")

    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"🔍 {job_count} Top Job Matches Today (8/10+) – Chandler, AZ"
    msg["From"] = FROM_EMAIL
    msg["To"] = YOUR_EMAIL
    msg.attach(MIMEText(html_content, "html"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(FROM_EMAIL, password)
            server.sendmail(FROM_EMAIL, YOUR_EMAIL, msg.as_string())
        print(f"✅ Email sent with {job_count} top job matches!")
    except Exception as e:
        print(f"❌ Email failed: {e}")

# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    all_jobs = {}

    print("🔍 Fetching jobs from Adzuna...")
    adzuna_jobs = fetch_adzuna_jobs()
    for job in adzuna_jobs:
        all_jobs[job["id"]] = job
    print(f"   Found {len(adzuna_jobs)} jobs from Adzuna")

    print("🔍 Fetching jobs from Arbeitnow (remote/US)...")
    arbeitnow_jobs = fetch_arbeitnow_jobs()
    for job in arbeitnow_jobs:
        all_jobs[job["id"]] = job
    print(f"   Found {len(arbeitnow_jobs)} jobs from Arbeitnow")

    jobs = list(all_jobs.values())
    print(f"\n📋 Total unique jobs to score: {len(jobs)}")

    print("\n🤖 Scoring jobs with Claude AI (showing 8+ only)...")
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    scored = []
    for i, job in enumerate(jobs):
        print(f"   Scoring {i+1}/{len(jobs)}: {job.get('title', 'N/A')} @ {job.get('company', 'N/A')}", end=" ")
        score, reason = score_job(client, job)
        print(f"→ {score}/10")
        if score >= MIN_SCORE:
            scored.append((job, score, reason))

    scored.sort(key=lambda x: x[1], reverse=True)

    print(f"\n✅ {len(scored)} jobs scored {MIN_SCORE}+/10")
    print("📧 Building and sending email digest...")

    html = build_email(scored)
    send_email(html, len(scored))

if __name__ == "__main__":
    main()
