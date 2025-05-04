import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.getcwd()), '.env'))

class Database:
    def __init__(self):
        self.dsn = {
            "dbname": os.getenv("DATABASE_NAME"),
            "user": os.getenv("DATABASE_USER"),
            "password": os.getenv("DATAPASE_PASSWORD"),
            "host": os.getenv("DATABASE_HOST"),
            "port": os.getenv("DATAPASE_PORT")
        }

    def __enter__(self):
        """with 문에서 실행될 때 자동으로 DB 연결"""
        self.conn = psycopg2.connect(**self.dsn)
        self.cur = self.conn.cursor(cursor_factory=RealDictCursor)
        return self

    def execute(self, query, params=None, commit=False):
        """쿼리 실행 함수"""
        try:
            self.cur.execute(query, params)
            if commit:
                self.conn.commit()
            return self.cur
        except Exception as e:
            self.conn.rollback()  # 에러 발생 시 롤백
            raise e

    def __exit__(self, exc_type, exc_value, traceback):
        """with 문이 끝나면 자동으로 DB 연결 해제"""
        self.cur.close()
        self.conn.close()

if __name__ == "__main__":
    with Database() as db:
          result = db.execute("SELECT * FROM users WHERE user_type = %s", ("company",))
          for row in result.fetchall():
              print(row)