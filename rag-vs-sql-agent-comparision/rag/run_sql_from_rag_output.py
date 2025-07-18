import sqlite3
import re

DB_PATH = "../e-commerce-data/olist.sqlite/olist.sqlite"
RAG_OUTPUT_PATH = "rag-output.txt"
RESULTS_PATH = "rag-sql-results.txt"

# Read the SQL query from rag-output.txt
with open(RAG_OUTPUT_PATH, "r", encoding="utf-8") as f:
    content = f.read()

# Extract the SQL query (between ```sql and ```) if present
match = re.search(r"```sql\s*(.*?)```", content, re.DOTALL)
if match:
    sql_query = match.group(1).strip()
else:
    # Fallback: try to find a SELECT statement
    select_match = re.search(r"(SELECT[\s\S]+?;)", content, re.IGNORECASE)
    if select_match:
        sql_query = select_match.group(1).strip()
    else:
        raise ValueError("No SQL query found in rag-output.txt")

print(f"Running SQL query:\n{sql_query}\n")

# Run the query on the SQLite database
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()
cursor.execute(sql_query)
rows = cursor.fetchall()
columns = [desc[0] for desc in cursor.description]
conn.close()

# Write results to rag-sql-results.txt
with open(RESULTS_PATH, "w", encoding="utf-8") as f:
    f.write("\t".join(columns) + "\n")
    for row in rows:
        f.write("\t".join(str(x) for x in row) + "\n")

print(f"Results written to {RESULTS_PATH}") 