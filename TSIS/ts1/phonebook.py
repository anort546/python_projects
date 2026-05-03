import json
import csv
import os
from connect import get_connection
from config import PAGE_SIZE

#helper: print a row as a readable line
def print_row(row):
    # row columns: id, first_name, last_name, email, birthday, group_name, phones
    print(f"  [{row[0]}] {row[1]} {row[2] or ''} | "
          f"email: {row[3] or '-'} | "
          f"bday: {row[4] or '-'} | "
          f"group: {row[5] or '-'} | "
          f"phones: {row[6] or '-'}")

#1. add a new contact
def add_contact():
    print("\n--- add contact ---")
    first = input("first name: ").strip()
    last  = input("last name (enter to skip): ").strip() or None
    email = input("email (enter to skip): ").strip() or None
    bday  = input("birthday yyyy-mm-dd (enter to skip): ").strip() or None
    group = input("group (Family/Work/Friend/Other): ").strip() or "Other"

    conn = get_connection()
    cur  = conn.cursor()

    # get or create the group
    cur.execute("SELECT id FROM groups WHERE LOWER(name) = LOWER(%s)", (group,))
    row = cur.fetchone()
    if row:
        group_id = row[0]
    else:
        cur.execute("INSERT INTO groups (name) VALUES (%s) RETURNING id", (group,))
        group_id = cur.fetchone()[0]

    # insert the contact
    cur.execute(
        "INSERT INTO contacts (first_name, last_name, email, birthday, group_id) "
        "VALUES (%s, %s, %s, %s, %s) RETURNING id",
        (first, last, email, bday, group_id)
    )
    contact_id = cur.fetchone()[0]

    # add at least one phone
    while True:
        phone = input("phone number (enter to skip): ").strip()
        if not phone:
            break
        ptype = input("type (home/work/mobile): ").strip() or "mobile"
        cur.execute(
            "INSERT INTO phones (contact_id, phone, type) VALUES (%s, %s, %s)",
            (contact_id, phone, ptype)
        )
        more = input("add another phone? (y/n): ").strip().lower()
        if more != "y":
            break

    conn.commit()
    cur.close()
    conn.close()
    print("contact added.")

#2. search contacts (uses db function search_contacts)
def search():
    query = input("\nsearch (name / email / phone): ").strip()
    conn  = get_connection()
    cur   = conn.cursor()
    cur.execute("SELECT * FROM search_contacts(%s)", (query,))
    rows = cur.fetchall()
    cur.close()
    conn.close()

    if not rows:
        print("nothing found.")
        return
    for row in rows:
        print_row(row)

#3. filter by group
def filter_by_group():
    conn = get_connection()
    cur  = conn.cursor()

    # show available groups first
    cur.execute("SELECT name FROM groups ORDER BY name")
    groups = [r[0] for r in cur.fetchall()]
    print("\navailable groups:", ", ".join(groups))

    group = input("enter group name: ").strip()
    cur.execute("""
        SELECT c.id, c.first_name, c.last_name, c.email, c.birthday,
               g.name,
               STRING_AGG(p.phone || ' (' || COALESCE(p.type,'?') || ')', ', ')
        FROM contacts c
        LEFT JOIN groups g ON g.id = c.group_id
        LEFT JOIN phones p ON p.contact_id = c.id
        WHERE LOWER(g.name) = LOWER(%s)
        GROUP BY c.id, c.first_name, c.last_name, c.email, c.birthday, g.name
        ORDER BY c.first_name
    """, (group,))
    rows = cur.fetchall()
    cur.close()
    conn.close()

    if not rows:
        print("no contacts in that group.")
        return
    for row in rows:
        print_row(row)

#4. sort contacts 
def list_sorted():
    print("\nsort by: 1) name  2) birthday  3) date added")
    choice = input("choose: ").strip()
    sort_map = {"1": "name", "2": "birthday", "3": "date"}
    sort = sort_map.get(choice, "name")

    conn = get_connection()
    cur  = conn.cursor()
    cur.execute("SELECT * FROM get_contacts_page(%s, 0, %s)", (1000, sort))
    rows = cur.fetchall()
    cur.close()
    conn.close()

    for row in rows:
        print_row(row)

# 5. paginated navigation
def paginate():
    print("\nsort by: 1) name  2) birthday  3) date added")
    choice = input("choose: ").strip()
    sort_map = {"1": "name", "2": "birthday", "3": "date"}
    sort = sort_map.get(choice, "name")

    page = 0
    while True:
        offset = page * PAGE_SIZE
        conn = get_connection()
        cur  = conn.cursor()
        cur.execute("SELECT * FROM get_contacts_page(%s, %s, %s)",
                    (PAGE_SIZE, offset, sort))
        rows = cur.fetchall()
        cur.close()
        conn.close()

        if not rows and page == 0:
            print("no contacts.")
            break

        print(f"\n--- page {page + 1} ---")
        for row in rows:
            print_row(row)

        # navigation options
        nav = input("next(n) / prev(p) / quit(q): ").strip().lower()
        if nav == "n":
            if len(rows) < PAGE_SIZE:
                print("already on last page.")
            else:
                page += 1
        elif nav == "p":
            if page == 0:
                print("already on first page.")
            else:
                page -= 1
        else:
            break

#6. add phone to existing contact
def add_phone():
    name  = input("\ncontact first name: ").strip()
    phone = input("phone number: ").strip()
    ptype = input("type (home/work/mobile): ").strip() or "mobile"

    conn = get_connection()
    cur  = conn.cursor()
    try:
        cur.execute("CALL add_phone(%s, %s, %s)", (name, phone, ptype))
        conn.commit()
        print("phone added.")
    except Exception as e:
        conn.rollback()
        print(f"error: {e}")
    finally:
        cur.close()
        conn.close()

#7. move contact to group
def move_to_group():
    name  = input("\ncontact first name: ").strip()
    group = input("group name: ").strip()

    conn = get_connection()
    cur  = conn.cursor()
    try:
        cur.execute("CALL move_to_group(%s, %s)", (name, group))
        conn.commit()
        print("contact moved.")
    except Exception as e:
        conn.rollback()
        print(f"error: {e}")
    finally:
        cur.close()
        conn.close()

#8. delete contact
def delete_contact():
    name = input("\nfirst name of contact to delete: ").strip()
    conn = get_connection()
    cur  = conn.cursor()
    cur.execute("DELETE FROM contacts WHERE LOWER(first_name) = LOWER(%s)", (name,))
    deleted = cur.rowcount
    conn.commit()
    cur.close()
    conn.close()
    print(f"{deleted} contact(s) deleted.")

# 9. export all contacts to json
def export_json():
    conn = get_connection()
    cur  = conn.cursor()

    # get all contacts with their phones and group
    cur.execute("""
        SELECT c.id, c.first_name, c.last_name, c.email,
               c.birthday::TEXT, g.name AS group_name
        FROM contacts c
        LEFT JOIN groups g ON g.id = c.group_id
        ORDER BY c.first_name
    """)
    contacts = cur.fetchall()

    result = []
    for row in contacts:
        contact_id = row[0]
        # get all phones for this contact
        cur.execute("SELECT phone, type FROM phones WHERE contact_id = %s", (contact_id,))
        phones = [{"phone": p[0], "type": p[1]} for p in cur.fetchall()]
        result.append({
            "first_name": row[1],
            "last_name":  row[2],
            "email":      row[3],
            "birthday":   row[4],
            "group":      row[5],
            "phones":     phones
        })

    cur.close()
    conn.close()

    filename = "contacts_export.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"exported {len(result)} contacts to {filename}")

#10. import contacts from json
def import_json():
    filename = input("\njson filename (default: contacts_export.json): ").strip()
    if not filename:
        filename = "contacts_export.json"

    if not os.path.exists(filename):
        print("file not found.")
        return

    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)

    conn = get_connection()
    cur  = conn.cursor()
    added = skipped = overwritten = 0

    for item in data:
        first = item.get("first_name", "")
        # check if contact already exists
        cur.execute("SELECT id FROM contacts WHERE LOWER(first_name) = LOWER(%s)", (first,))
        existing = cur.fetchone()

        if existing:
            print(f"duplicate: {first}")
            choice = input("  skip(s) or overwrite(o)? ").strip().lower()
            if choice == "o":
                # delete old contact (phones cascade delete)
                cur.execute("DELETE FROM contacts WHERE id = %s", (existing[0],))
                overwritten += 1
            else:
                skipped += 1
                continue

        # get or create group
        group_name = item.get("group") or "Other"
        cur.execute("SELECT id FROM groups WHERE LOWER(name) = LOWER(%s)", (group_name,))
        g = cur.fetchone()
        if g:
            group_id = g[0]
        else:
            cur.execute("INSERT INTO groups (name) VALUES (%s) RETURNING id", (group_name,))
            group_id = cur.fetchone()[0]

        # insert contact
        cur.execute(
            "INSERT INTO contacts (first_name, last_name, email, birthday, group_id) "
            "VALUES (%s, %s, %s, %s, %s) RETURNING id",
            (first, item.get("last_name"), item.get("email"),
             item.get("birthday"), group_id)
        )
        contact_id = cur.fetchone()[0]

        # insert phones
        for ph in item.get("phones", []):
            cur.execute(
                "INSERT INTO phones (contact_id, phone, type) VALUES (%s, %s, %s)",
                (contact_id, ph.get("phone"), ph.get("type"))
            )
        added += 1

    conn.commit()
    cur.close()
    conn.close()
    print(f"done: {added} added, {overwritten} overwritten, {skipped} skipped.")

#11. import from csv (extended with new fields)
def import_csv():
    filename = input("\ncsv filename (default: contacts.csv): ").strip()
    if not filename:
        filename = "contacts.csv"

    if not os.path.exists(filename):
        print("file not found.")
        return

    conn = get_connection()
    cur  = conn.cursor()
    added = 0

    with open(filename, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            first = row.get("first_name", "").strip()
            if not first:
                continue

            # get or create group
            group_name = row.get("group", "Other").strip() or "Other"
            cur.execute("SELECT id FROM groups WHERE LOWER(name) = LOWER(%s)", (group_name,))
            g = cur.fetchone()
            if g:
                group_id = g[0]
            else:
                cur.execute("INSERT INTO groups (name) VALUES (%s) RETURNING id", (group_name,))
                group_id = cur.fetchone()[0]

            # insert contact, skip if first_name already exists
            cur.execute("SELECT id FROM contacts WHERE LOWER(first_name) = LOWER(%s)", (first,))
            if cur.fetchone():
                print(f"skipping duplicate: {first}")
                continue

            bday  = row.get("birthday", "").strip() or None
            email = row.get("email", "").strip() or None
            cur.execute(
                "INSERT INTO contacts (first_name, last_name, email, birthday, group_id) "
                "VALUES (%s, %s, %s, %s, %s) RETURNING id",
                (first, row.get("last_name", "").strip() or None, email, bday, group_id)
            )
            contact_id = cur.fetchone()[0]

            # insert phone if present
            phone = row.get("phone", "").strip()
            if phone:
                ptype = row.get("phone_type", "mobile").strip() or "mobile"
                cur.execute(
                    "INSERT INTO phones (contact_id, phone, type) VALUES (%s, %s, %s)",
                    (contact_id, phone, ptype)
                )
            added += 1

    conn.commit()
    cur.close()
    conn.close()
    print(f"imported {added} contacts from csv.")

#main menu
def main():
    menu = """
========= phonebook =========
 1  add contact
 2  search (name/email/phone)
 3  filter by group
 4  list sorted
 5  browse pages
 6  add phone to contact
 7  move contact to group
 8  delete contact
 9  export to json
10  import from json
11  import from csv
 0  exit
=============================
"""
    actions = {
        "1":  add_contact,
        "2":  search,
        "3":  filter_by_group,
        "4":  list_sorted,
        "5":  paginate,
        "6":  add_phone,
        "7":  move_to_group,
        "8":  delete_contact,
        "9":  export_json,
        "10": import_json,
        "11": import_csv,
    }

    while True:
        print(menu)
        choice = input("choose: ").strip()
        if choice == "0":
            print("bye.")
            break
        action = actions.get(choice)
        if action:
            action()
        else:
            print("invalid choice.")

if __name__ == "__main__":
    main()
