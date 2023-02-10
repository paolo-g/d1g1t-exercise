import sys
import psycopg2

# Try to connect to the postgres instance
if __name__ == "__main__":
    connector = f"host={sys.argv[1]} dbname={sys.argv[2]} user={sys.argv[3]} password={sys.argv[4]}"
    try:
        conn = psycopg2.connect(connector)
        conn.close()
    except psycopg2.OperationalError as ex:
        sys.exit(1)

    sys.exit(0)
