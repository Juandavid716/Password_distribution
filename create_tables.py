
def create_table(name_table, cur):
    query = """
     CREATE TABLE IF NOT EXISTS {} (
        dimension VARCHAR(30) NOT NULL,
        probability VARCHAR(30) NOT NULL)""".format(name_table)

    cur.execute(query)