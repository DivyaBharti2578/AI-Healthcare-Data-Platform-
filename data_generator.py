import psycopg2
import random
from faker import Faker
from datetime import datetime, timedelta

fake = Faker()

conn = psycopg2.connect(
    dbname="healthcare",
    user="postgres",
    password="yourpassword",
    host="127.0.0.1",
    port="5432"
)

cursor = conn.cursor()

# Generate Members
print("Generating members...")
for _ in range(10000):
    cursor.execute(
        """
        INSERT INTO dim_member (first_name, last_name, dob, gender, state)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (
            fake.first_name(),
            fake.last_name(),
            fake.date_of_birth(minimum_age=18, maximum_age=90),
            random.choice(["Male", "Female"]),
            fake.state_abbr()
        )
    )

# Generate Providers
print("Generating providers...")
for _ in range(1000):
    cursor.execute(
        """
        INSERT INTO dim_provider (provider_name, specialty, state)
        VALUES (%s, %s, %s)
        """,
        (
            "Dr. " + fake.last_name(),
            random.choice(["Cardiology", "Dermatology", "Orthopedics", "General Practice"]),
            fake.state_abbr()
        )
    )

conn.commit()

# Get max IDs
cursor.execute("SELECT MAX(member_id) FROM dim_member;")
max_member_id = cursor.fetchone()[0]

cursor.execute("SELECT MAX(provider_id) FROM dim_provider;")
max_provider_id = cursor.fetchone()[0]

# Generate Claims
print("Generating claims...")
for _ in range(50000):
    cursor.execute(
        """
        INSERT INTO fact_claims (member_id, provider_id, diagnosis_code, claim_amount, claim_date)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (
            random.randint(1, max_member_id),
            random.randint(1, max_provider_id),
            random.choice(["I10", "E11", "J45", "M54"]),
            round(random.uniform(100, 5000), 2),
            fake.date_between(start_date="-2y", end_date="today")
        )
    )

conn.commit()
conn.close()

print("Data generation complete.")