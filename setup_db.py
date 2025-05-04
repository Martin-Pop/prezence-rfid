#!/usr/bin/env python3
import sqlite3;
import os;
from dotenv import load_dotenv;

load_dotenv()

DATABASE_NAME = os.environ.get("DATABASE_NAME", "test.db");

def create_tables():
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    
    c.execute('''create table if not exists karta(
                id integer primary key autoincrement,
                uid integer unique not null check(typeof(uid) = 'integer'),
                jmeno text unique not null,
                valid boolean not null
              );''')
    
    c.execute('''create table if not exists pruchod(
                id integer primary key autoincrement,
                datum datetime not null,
                vchod boolean not null,
                karta_id integer not null,
                foreign key(karta_id) references karta(id)
              );''')
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tables()
    print("Tables created successfully.")
