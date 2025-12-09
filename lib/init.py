import sqlite3

CONN = sqlite3.connect(':memory:')
CURSOR = CONN.cursor()
