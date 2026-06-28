import psycopg2
url = 'postgresql://postgres.jdwzlteweneieskdqndc:07agro11guard@aws-1-ap-southeast-1.pooler.supabase.com:5432/postgres'
conn = psycopg2.connect(url)
conn.autocommit = True
cur = conn.cursor()
cur.execute("""
    DROP SCHEMA public CASCADE;
    CREATE SCHEMA public;
    GRANT ALL ON SCHEMA public TO postgres;
    GRANT ALL ON SCHEMA public TO public;
""")
print('Database wiped successfully!')
