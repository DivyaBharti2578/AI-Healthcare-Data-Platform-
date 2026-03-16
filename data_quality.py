import psycopg2

conn = psycopg2.connect(
    dbname="healthcare",
    user="postgres",
    password="yourpassword",
    host="127.0.0.1",
    port="5432"
)

cursor = conn.cursor()

def run_check(check_name, query_fail, query_total):
    cursor.execute(query_fail)
    failed = cursor.fetchone()[0]

    cursor.execute(query_total)
    total = cursor.fetchone()[0]

    failure_percentage = (failed / total) * 100 if total > 0 else 0

    cursor.execute("""
        INSERT INTO data_quality_checks 
        (check_name, failed_records, total_records, failure_percentage)
        VALUES (%s, %s, %s, %s)
    """, (check_name, failed, total, failure_percentage))

    conn.commit()

# 1️⃣ Null Diagnosis Code Check
run_check(
    "Null Diagnosis Code",
    "SELECT COUNT(*) FROM fact_claims WHERE diagnosis_code IS NULL;",
    "SELECT COUNT(*) FROM fact_claims;"
)

# 2️⃣ Negative Claim Amount Check
run_check(
    "Negative Claim Amount",
    "SELECT COUNT(*) FROM fact_claims WHERE claim_amount < 0;",
    "SELECT COUNT(*) FROM fact_claims;"
)

# 3️⃣ Future Claim Date Check
run_check(
    "Future Claim Date",
    "SELECT COUNT(*) FROM fact_claims WHERE claim_date > CURRENT_DATE;",
    "SELECT COUNT(*) FROM fact_claims;"
)

conn.close()

print("Data quality checks completed.")