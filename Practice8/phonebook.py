from connect import connect


def add(name, phone):
    conn = connect()
    cur = conn.cursor()

    cur.execute("CALL upsert_user(%s, %s)", (name, phone))
    conn.commit()

    conn.close()



def search(pattern):
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM search_phonebook(%s)", (pattern,))
    rows = cur.fetchall()

    for r in rows:
        print(r)

    conn.close()



def show(limit, offset):
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM get_phonebook(%s, %s)", (limit, offset))
    rows = cur.fetchall()

    for r in rows:
        print(r)

    conn.close()


def delete(val):
    conn = connect()
    cur = conn.cursor()

    cur.execute("CALL delete_user(%s)", (val,))
    conn.commit()

    conn.close()



def insert_many(names, phones):
    conn = connect()
    cur = conn.cursor()

    cur.execute("CALL insert_many(%s, %s)", (names, phones))
    conn.commit()

    conn.close()


if __name__ == "__main__":
    add("Anna", "12345")
    add("Noone", "67890")

    print("SEARCH:")
    search("Ann")

    print("ALL:")
    show(10, 0)

    print("INSERT MANY:")
    insert_many(["Adema", "Abay"], ["111", "abc"])  # abc покажет ошибку

    print("DELETE:")
    delete("Anna")

    print("FINAL:")
    show(10, 0)