
def create_table(name_table, cur):
    query = """
     CREATE TABLE IF NOT EXISTS {} (
        dimension TEXT NOT NULL,
        probability VARCHAR(30) NOT NULL)""".format(name_table)

    cur.execute(query)
    cur.execute("DELETE FROM {}".format(name_table))

def create_table_hash( cur):
    query = """
     CREATE TABLE IF NOT EXISTS {} (
        hash_t VARCHAR(30) NOT NULL)""".format("hash_table")

    cur.execute(query)
    #cur.execute("DELETE FROM {}".format(name_table))