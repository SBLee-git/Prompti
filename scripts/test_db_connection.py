from backend.db.database import engine

def test_connection():
    try:
        with engine.connect() as conn:
            result = conn.execute("SELECT version();")
            print("✅ DB 연결 성공! 🎉")
            print("📦 PostgreSQL 버전:", result.fetchone()[0])
    except Exception as e:
        print("❌ DB 연결 실패:", e)

if __name__ == "__main__":
    test_connection()
