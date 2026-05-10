import sqlite3

# Database connection
conn = sqlite3.connect("ai_predictions.db")

cursor = conn.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS predictions (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    match_id TEXT,
    home_team TEXT,
    away_team TEXT,

    alert_type TEXT,

    probability INTEGER,
    confidence INTEGER,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()


# Save prediction
def save_prediction(
    match_id,
    home_team,
    away_team,
    alert_type,
    probability,
    confidence
):

    cursor.execute("""

    INSERT INTO predictions (

        match_id,
        home_team,
        away_team,
        alert_type,
        probability,
        confidence

    )

    VALUES (?, ?, ?, ?, ?, ?)

    """, (

        match_id,
        home_team,
        away_team,
        alert_type,
        probability,
        confidence

    ))

    conn.commit()

    print("✅ Prediction saved to database")


# Show all predictions
def show_predictions():

    cursor.execute("""

    SELECT *
    FROM predictions
    ORDER BY id DESC

    """)

    rows = cursor.fetchall()

    for row in rows:
        print(row)