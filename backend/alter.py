import sqlite3

def run():
    try:
        conn = sqlite3.connect("backend/sql_app.db")
        conn.execute("ALTER TABLE meals ADD COLUMN ai_explanation VARCHAR;")
        conn.commit()
        print("Success")
    except Exception as e:
        print("Error:", e)
    finally:
        conn.close()

if __name__ == '__main__':
    run()
