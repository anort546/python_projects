from connect import connect
import csv


def create_table():
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS contacts (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100),
        phone VARCHAR(20)
    );
    """)

    conn.commit()
    cur.close()
    conn.close()



def add_contact(name, phone):
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO contacts (name, phone) VALUES (%s, %s)",
        (name, phone)
    )

    conn.commit()
    cur.close()
    conn.close()


def show_contacts():
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM contacts")
    rows = cur.fetchall()

    for row in rows:
        print(row)

    cur.close()
    conn.close()


def update_contact(name, phone):
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "UPDATE contacts SET phone=%s WHERE name=%s",
        (phone, name)
    )

    conn.commit()
    cur.close()
    conn.close()



def delete_contact(name):
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM contacts WHERE name=%s",
        (name,)
    )

    conn.commit()
    cur.close()
    conn.close()



def find_contact(name):
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM contacts WHERE name=%s",
        (name,)
    )

    print(cur.fetchall())

    cur.close()
    conn.close()


def import_csv():
    conn = connect()
    cur = conn.cursor()

    with open("D:\pp2\Practice7\contacts.csv", "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            cur.execute(
                "INSERT INTO contacts (name, phone) VALUES (%s, %s)",
                (row["name"], row["phone"])
            )

    conn.commit()
    cur.close()
    conn.close()



def menu():
    while True:
        print("\n1. Добавить")
        print("2. Показать")
        print("3. Обновить")
        print("4. Удалить")
        print("5. Найти")
        print("6. Импорт CSV")
        print("0. Выход")

        choice = input("Выбор: ")

        if choice == "1":
            name = input("Имя: ")
            phone = input("Телефон: ")
            add_contact(name, phone)

        elif choice == "2":
            show_contacts()

        elif choice == "3":
            name = input("Имя: ")
            phone = input("Новый телефон: ")
            update_contact(name, phone)

        elif choice == "4":
            name = input("Имя: ")
            delete_contact(name)

        elif choice == "5":
            name = input("Имя: ")
            find_contact(name)

        elif choice == "6":
            import_csv()

        elif choice == "0":
            break


create_table()
menu()