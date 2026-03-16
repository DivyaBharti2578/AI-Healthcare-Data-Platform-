import requests
import psycopg2
import re
import time
import os


# -------------------------
# ALLOWED TABLES
# -------------------------
ALLOWED_TABLES = {
    "fact_claims": ["claim_id", "member_id", "provider_id", "diagnosis_code", "claim_amount", "claim_date"],
    "dim_member": ["member_id", "first_name", "last_name", "dob", "gender", "state"],
    "dim_provider": ["provider_id", "provider_name", "specialty", "state"]
}


# -------------------------
# DATABASE CONNECTION (RETRY LOGIC)
# -------------------------
def get_connection():
    for i in range(10):  # retry 10 times
        try:
            conn = psycopg2.connect(
                dbname=os.getenv("DB_NAME"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                host=os.getenv("DB_HOST"),
                port=os.getenv("DB_PORT")
            )
            return conn
        except psycopg2.OperationalError:
            print("Waiting for database...")
            time.sleep(3)

    raise Exception("Database connection failed after retries.")


# -------------------------
# GENERATE SQL FROM OLLAMA
# -------------------------
def generate_sql(question):

    prompt = f"""
You are a PostgreSQL SQL generator.

STRICT RULES:
- Return ONLY raw SQL.
- No explanation.
- No markdown.
- Only SELECT statements.
- Use only provided schema.
- If unsure, return: SELECT 1;

Schema:
fact_claims(claim_id, member_id, provider_id, diagnosis_code, claim_amount, claim_date)
dim_member(member_id, first_name, last_name, dob, gender, state)
dim_provider(provider_id, provider_name, specialty, state)

Question: {question}
"""

    response = requests.post(
        "http://host.docker.internal:11434/api/generate",
        json={
            "model": "llama3",
            "prompt": prompt,
            "stream": False
        }
    )

    raw_sql = response.json()["response"]
    return clean_sql_output(raw_sql)


# -------------------------
# CLEAN SQL OUTPUT
# -------------------------
def clean_sql_output(raw_output):
    raw_output = raw_output.replace("```sql", "").replace("```", "")

    if ";" in raw_output:
        raw_output = raw_output.split(";")[0] + ";"

    return raw_output.strip()


# -------------------------
# VALIDATE SQL SAFETY
# -------------------------
def validate_sql(sql):

    if not sql.strip().upper().startswith("SELECT"):
        return False

    blocked = ["DROP", "DELETE", "UPDATE", "INSERT", "ALTER"]
    for word in blocked:
        if word in sql.upper():
            return False

    return True


# -------------------------
# EXECUTE SQL
# -------------------------
def execute_sql(sql):

    conn = get_connection()
    cursor = conn.cursor()

    start = time.time()

    cursor.execute(sql)
    rows = cursor.fetchall()

    end = time.time()
    execution_time = round(end - start, 4)

    cursor.close()
    conn.close()

    return rows, execution_time


# -------------------------
# LOG QUERY
# -------------------------
def log_query(question, sql, execution_time):

    conn = get_connection()
    cursor = conn.cursor()

    insert_query = """
        INSERT INTO query_logs (user_question, generated_sql, execution_time)
        VALUES (%s, %s, %s)
    """

    cursor.execute(insert_query, (question, sql, execution_time))
    conn.commit()

    cursor.close()
    conn.close()