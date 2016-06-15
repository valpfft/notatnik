import psycopg2.extras
import psycopg2
import dj_database_url
db_info = dj_database_url.config(
    default='postgres://nhhfkzrvppmpvl:sT-ng-onnXd_M-ddhBFiSUIOaT@ec2-54-228-219-2.eu-west-1.compute.amazonaws.com:5432/dcg8hogaee5g8i')

conn = psycopg2.connect(
    database=db_info.get('NAME'),
    user=db_info.get('USER'),
    password=db_info.get('PASSWORD'),
    host=db_info.get('HOST'),
    port=db_info.get('PORT'))
c = conn.cursor()
cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
conn.autocommit = True


def create_table():
    c.execute('''CREATE TABLE IF NOT EXISTS memory(
              id SERIAL PRIMARY KEY NOT NULL,
              user_id INT NOT NULL,
              predicate CHAR(512) not null,
              done CHAR(512) not null,
              num integer,
              finished timestamp without time zone not null);''')
    conn.commit()
    return conn, c
create_table()
