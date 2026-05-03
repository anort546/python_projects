-- procedure: add a phone number to an existing contact by name
CREATE OR REPLACE PROCEDURE add_phone(
    p_contact_name VARCHAR,
    p_phone        VARCHAR,
    p_type         VARCHAR
)
LANGUAGE plpgsql AS $$
DECLARE
    v_contact_id INTEGER;
BEGIN
    -- find the contact by first_name (case insensitive)
    SELECT id INTO v_contact_id
    FROM contacts
    WHERE LOWER(first_name) = LOWER(p_contact_name)
    LIMIT 1;

    IF v_contact_id IS NULL THEN
        RAISE EXCEPTION 'contact "%" not found', p_contact_name;
    END IF;

    -- insert the new phone number for that contact
    INSERT INTO phones (contact_id, phone, type)
    VALUES (v_contact_id, p_phone, p_type);
END;
$$;


-- procedure: move a contact to a group, create the group if it doesnt exist
CREATE OR REPLACE PROCEDURE move_to_group(
    p_contact_name VARCHAR,
    p_group_name   VARCHAR
)
LANGUAGE plpgsql AS $$
DECLARE
    v_contact_id INTEGER;
    v_group_id   INTEGER;
BEGIN
    -- find or create the group
    SELECT id INTO v_group_id
    FROM groups
    WHERE LOWER(name) = LOWER(p_group_name);

    IF v_group_id IS NULL THEN
        INSERT INTO groups (name) VALUES (p_group_name)
        RETURNING id INTO v_group_id;
    END IF;

    -- find the contact
    SELECT id INTO v_contact_id
    FROM contacts
    WHERE LOWER(first_name) = LOWER(p_contact_name)
    LIMIT 1;

    IF v_contact_id IS NULL THEN
        RAISE EXCEPTION 'contact "%" not found', p_contact_name;
    END IF;

    -- update contact group
    UPDATE contacts SET group_id = v_group_id WHERE id = v_contact_id;
END;
$$;


-- function: search contacts by name, email, or any phone number
-- extends the practice 8 pattern search
CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE (
    id         INTEGER,
    first_name VARCHAR,
    last_name  VARCHAR,
    email      VARCHAR,
    birthday   DATE,
    group_name VARCHAR,
    phones     TEXT
)
LANGUAGE plpgsql AS $$
BEGIN
    RETURN QUERY
    SELECT
        c.id,
        c.first_name,
        c.last_name,
        c.email,
        c.birthday,
        g.name AS group_name,
        -- aggregate all phones for this contact into one string
        STRING_AGG(p.phone || ' (' || COALESCE(p.type, '?') || ')', ', ') AS phones
    FROM contacts c
    LEFT JOIN groups g ON g.id = c.group_id
    LEFT JOIN phones p ON p.contact_id = c.id
    WHERE
        -- match name
        c.first_name ILIKE '%' || p_query || '%'
        OR c.last_name  ILIKE '%' || p_query || '%'
        -- match email
        OR c.email      ILIKE '%' || p_query || '%'
        -- match any phone belonging to this contact
        OR c.id IN (
            SELECT contact_id FROM phones
            WHERE phone ILIKE '%' || p_query || '%'
        )
    GROUP BY c.id, c.first_name, c.last_name, c.email, c.birthday, g.name
    ORDER BY c.first_name;
END;
$$;


-- function: paginated contact list (kept from practice 8, extended with sort)
CREATE OR REPLACE FUNCTION get_contacts_page(
    p_limit  INTEGER,
    p_offset INTEGER,
    p_sort   VARCHAR DEFAULT 'name'   -- 'name', 'birthday', 'date'
)
RETURNS TABLE (
    id         INTEGER,
    first_name VARCHAR,
    last_name  VARCHAR,
    email      VARCHAR,
    birthday   DATE,
    group_name VARCHAR,
    phones     TEXT
)
LANGUAGE plpgsql AS $$
BEGIN
    RETURN QUERY
    SELECT
        c.id,
        c.first_name,
        c.last_name,
        c.email,
        c.birthday,
        g.name AS group_name,
        STRING_AGG(p.phone || ' (' || COALESCE(p.type, '?') || ')', ', ') AS phones
    FROM contacts c
    LEFT JOIN groups g ON g.id = c.group_id
    LEFT JOIN phones p ON p.contact_id = c.id
    GROUP BY c.id, c.first_name, c.last_name, c.email, c.birthday, g.name, c.created_at
    ORDER BY
        CASE WHEN p_sort = 'birthday' THEN c.birthday::TEXT   END ASC NULLS LAST,
        CASE WHEN p_sort = 'date'     THEN c.created_at::TEXT END ASC,
        c.first_name ASC
    LIMIT  p_limit
    OFFSET p_offset;
END;
$$;
