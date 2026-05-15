import pymysql
from datetime import datetime, timedelta
from settings import DB_CONFIG


# ----- Соединение с БД -----

def get_db_connection():
    """Создает и возвращает соединение с MySQL."""
    return pymysql.connect(**DB_CONFIG)
    #return pymysql.connect(cursorclass=pymysql.cursors.DictCursor, **DB_CONFIG)


# ----- USERS -----

def register_user(tg_id: int, tg_login: str) -> None:
    conn = get_db_connection()
    with conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO users (tg_id, tg_login)
                VALUES (%s, %s)
                ON DUPLICATE KEY UPDATE tg_login = VALUES(tg_login)
            """, (tg_id, tg_login))
        conn.commit()

def get_users_for_reminder() -> list[int]:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    print("[REMINDER CHECK]", now)
    conn = get_db_connection()
    with conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT DISTINCT w.tg_id
                FROM history h
                JOIN words w ON w.id = h.word_id
                JOIN users u ON u.tg_id = w.tg_id
                WHERE h.next_date <= %s
                  AND u.notify_enabled = 1
            """, (now,))
            rows = cur.fetchall()
            print("[ROWS FOUND]", rows)
            return [r["tg_id"] for r in rows]

def set_notify(tg_id: int, enabled: bool):
    conn = get_db_connection()
    with conn:
        with conn.cursor() as cur:
            cur.execute("UPDATE users SET notify_enabled = %s WHERE tg_id = %s", (int(enabled), tg_id))
        conn.commit()

def get_notify_status(tg_id: int) -> bool:
    conn = get_db_connection()
    with conn:
        with conn.cursor() as cur:
            cur.execute("SELECT notify_enabled FROM users WHERE tg_id = %s", (tg_id,))
            row = cur.fetchone()
            return bool(row["notify_enabled"]) if row else True


# ----- СЛОВАРИ -----

def create_dictionary(tg_id: int, name: str) -> int:
    conn = get_db_connection()
    with conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO dictionaries (tg_id, name) VALUES (%s, %s)",
                (tg_id, name)
            )
            conn.commit()
            return cur.lastrowid

def get_user_dictionaries(tg_id: int) -> list[dict]:
    conn = get_db_connection()
    with conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, name FROM dictionaries WHERE tg_id = %s ORDER BY created_at ASC",
                (tg_id,)
            )
            rows = cur.fetchall()
    return [{"id": r["id"], "name": r["name"]} for r in rows]

def delete_dictionary(tg_id: int, dict_id: int) -> bool:
    uid = int(tg_id)
    did = int(dict_id)
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id FROM words WHERE dict_id = %s", (did,))
            word_ids = [row["id"] for row in cur.fetchall()]

            if word_ids:
                cur.executemany("DELETE FROM history WHERE word_id = %s", [(wid,) for wid in word_ids])

            cur.execute("DELETE FROM words WHERE dict_id = %s", (did,))
            cur.execute("DELETE FROM dictionaries WHERE id = %s AND tg_id = %s", (did, uid))

        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        print(f"[ERROR] delete_dictionary({uid}, {did}): {e}")
        return False
    finally:
        conn.close()



# ----- СЛОВА -----

async def insert_word(tg_id: int, dict_id: int, word: str, shifting: str, learned: bool = False) -> int:
    conn = get_db_connection()
    with conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO words (tg_id, dict_id, word, shifting, pic, sound, learned)
                VALUES (%s, %s, %s, %s, NULL, NULL, %s)
            """, (tg_id, dict_id, word, shifting, int(learned)))
            word_id = cur.lastrowid
        conn.commit()

    next_date = datetime.now()
    add_history(word_id=word_id, stage=0, next_date=next_date)
    return word_id

def load_words(tg_id: int, dict_id: int | None = None, all_words: bool = False) -> list[dict]:
    #now = datetime.now().replace(second=0, microsecond=0).isoformat(" ", timespec="new_date_time")
    now = datetime.utcnow().replace(second=0, microsecond=0).isoformat(" ", timespec="new_date_time")
    conn = get_db_connection()
    with conn:
        with conn.cursor() as cur:
            query = """
                SELECT w.id, w.word, w.shifting, w.pic, w.sound, w.learned,
                       h.stage, h.next_date
                FROM words w
                LEFT JOIN history h ON h.word_id = w.id
                WHERE w.tg_id = %s
            """
            params = [tg_id]
            if dict_id is not None:
                query += " AND w.dict_id = %s"
                params.append(dict_id)
            if not all_words:
                query += " AND (h.next_date IS NULL OR h.next_date <= %s)"
                params.append(now)

            cur.execute(query, tuple(params))
            rows = cur.fetchall()

    return [
        {
            "id": r["id"],
            "word": r["word"],
            "shifting": r["shifting"],
            "pic": r["pic"],
            "sound": f"/{r['sound']}" if r["sound"] and not str(r["sound"]).startswith("/") else r["sound"],
            "learned": bool(r["learned"]),
            "stage": r["stage"],
            "next_review": r["next_date"],
        }
        for r in rows
    ]



# ----- ИСТОРИЯ -----

def add_history(word_id: int, stage: int, next_date: datetime) -> None:
    nd_str = next_date.replace(second=0, microsecond=0).strftime("%Y-%m-%d %H:%M")
    conn = get_db_connection()
    with conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id FROM history WHERE word_id = %s ORDER BY id DESC LIMIT 1", (word_id,))
            row = cur.fetchone()
            if row:
                cur.execute("""
                    UPDATE history
                    SET stage = %s, next_date = %s, created_at = CURRENT_TIMESTAMP
                    WHERE id = %s
                """, (stage, nd_str, row["id"]))
            else:
                cur.execute("""
                    INSERT INTO history (word_id, stage, next_date)
                    VALUES (%s, %s, %s)
                """, (word_id, stage, nd_str))
        conn.commit()

def update_history_db(tg_id: int, words: list[dict]):
    now = datetime.now()
    conn = get_db_connection()
    with conn:
        with conn.cursor() as cur:
            for w in words:
                word_id = w["id"]
                remembered = w["remembered"]

                cur.execute("SELECT stage FROM history WHERE word_id = %s", (word_id,))
                row = cur.fetchone()
                stage = (row["stage"] or 0)

                if row:
                    stage = row["stage"] or 0
                    new_stage = stage + 1 if remembered else 1
                    step_minutes = [10, 60, 360, 1440, 4320]
                    delta = timedelta(minutes=step_minutes[min(new_stage - 1, len(step_minutes) - 1)])
                    next_date = now + delta
                    cur.execute(
                        "UPDATE history SET stage=%s, next_date=%s WHERE word_id=%s",
                        (new_stage, next_date.strftime("%Y-%m-%d %H:%M"), word_id)
                    )
                else:
                    next_date = now + timedelta(minutes=10)
                    cur.execute(
                        "INSERT INTO history (word_id, stage, next_date) VALUES (%s, %s, %s)",
                        (word_id, 1, next_date.strftime("%Y-%m-%d %H:%M"))
                    )
        conn.commit()

def get_next_repeat_time(tg_id: int) -> str | None:
    conn = get_db_connection()
    with conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT MIN(h.next_date) AS next_date
                FROM history h
                JOIN words w ON w.id = h.word_id
                WHERE w.tg_id = %s
            """, (tg_id,))
            row = cur.fetchone()
    return row["next_date"] if row and row["next_date"] else None
