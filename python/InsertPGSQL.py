import psycopg2

class inserPGSQL(object):
    def __init__(self, *args):
        self.host="localhost"
        self.database="db_name"
        self.user="db_user"
        self.password="db_pass"
        self.port=5432
        self.conn = psycopg2.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password,
        )        
    def inserPGSQL_data(self,*args):
        try:
            for arg in args:
                sql="INSERT INTO test(comment) VALUES ('{}')".format(arg)
                cur = self.conn.cursor()
                cur.execute(sql)
                self.conn.commit()
            cur.close()
        except Exception (psycopg2.DatabaseError) as error:
            print(error)



pg = inserPGSQL()
for msg  in range (0,1000):
    pg.inserPGSQL_data("this is meesage from {}".format(msg))

