import sqlite3

class ParkDatabase:
    def __init__(self):
        self.conn = sqlite3.connect('parking_system.db')
        self.create_table()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS parking (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                number_plate TEXT NOT NULL,
                slot TEXT NOT NULL,
                time TEXT NOT NULL,
                floor TEXT NOT NULL
            )
        ''')
        self.conn.commit()

    def add_entry(self, number_plate, slot, time, floor):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO parking (number_plate, slot, time, floor) VALUES (?, ?, ?, ?)
        ''', (number_plate, slot, time, floor))
        self.conn.commit()

    def get_all_entries(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM parking')
        return cursor.fetchall()
    
    def get_entries_by_floor(self, floor):
        query = '''
        SELECT number_plate, slot, time FROM parking
        WHERE floor = ?
        '''
        cursor = self.conn.execute(query, (floor,))
        rows = cursor.fetchall()
        entries = [{'number_plate': row[0], 'slot': row[1], 'time': row[2]} for row in rows]
        return entries

    def close(self):
        self.conn.close()
