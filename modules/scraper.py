import pandas as pd
from modules.job_model import Job


def create_dummy_jobs():

    jobs = [
        Job(
            company="Google",
            role="Data Analyst",
            location="Bangalore",
            experience="0-2 Years",
            source="LinkedIn",
            apply_link="https://linkedin.com/jobs"
        ),

        Job(
            company="Microsoft",
            role="Business Analyst",
            location="Hyderabad",
            experience="1 Year",
            source="LinkedIn",
            apply_link="https://linkedin.com/jobs"
        )
    ]

    df = pd.DataFrame([job.__dict__ for job in jobs])

    df.to_csv("data/jobs.csv", index=False)

    print("✅ Jobs Saved Successfully")