import sqlite3

class TriangleDatabase:
    def __init__(self, db_path=":memory:"):
        self.db_path = db_path
        self._conn = sqlite3.connect(db_path, check_same_thread=False)
        self._create_table()

    def _create_table(self):
        self._conn.execute("""
            CREATE TABLE IF NOT EXISTS triangles (
                side1 REAL NOT NULL,
                side2 REAL NOT NULL,
                side3 REAL NOT NULL,
                triangle_type TEXT,
                error_message TEXT,
                PRIMARY KEY (side1, side2, side3)
            )
        """)
        self._conn.commit()

    def add_record(self, side1, side2, side3, triangle_type, error_message):
        self._conn.execute("""
            INSERT OR REPLACE INTO triangles 
            (side1, side2, side3, triangle_type, error_message) 
            VALUES (?, ?, ?, ?, ?)
        """, (float(side1), float(side2), float(side3), triangle_type, error_message))
        self._conn.commit()

    def get_record(self, side1, side2, side3):
        cur = self._conn.execute("""
            SELECT triangle_type, error_message FROM triangles 
            WHERE side1 = ? AND side2 = ? AND side3 = ?
        """, (float(side1), float(side2), float(side3)))
        row = cur.fetchone()
        return {"triangle_type": row[0], "error_message": row[1]} if row else None

    def delete_record(self, side1, side2, side3):
        cur = self._conn.execute("""
            DELETE FROM triangles WHERE side1 = ? AND side2 = ? AND side3 = ?
        """, (float(side1), float(side2), float(side3)))
        self._conn.commit()
        return cur.rowcount > 0

    def close(self):
        self._conn.close()