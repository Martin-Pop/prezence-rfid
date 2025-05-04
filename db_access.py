#!/usr/bin/env python3
import sqlite3
from setup_db import DATABASE_NAME;
from datetime import datetime

class DatabaseAccess():
    
    def IsKartaValid(uid):
        conn = sqlite3.connect(DATABASE_NAME)
        try:
            c = conn.cursor()
            c.execute('''select valid from karta where uid = ?''', (uid,))
            row = c.fetchone()
            if row is None:
                return False
            return row[0] == 1
        except sqlite3.Error as e:
            print(f"Nastala chyba: {e}")
            return False
        finally:
            conn.close()
    
    def AddPruchod(uid):
        conn = sqlite3.connect(DATABASE_NAME)
        try:
            c = conn.cursor()
            c.execute('''select vchod from pruchod where karta_id = (select id from karta where uid = ?) order by datum desc limit 1''', (uid,))
            last_pruchod = c.fetchone()
            vchod = 0 if last_pruchod and last_pruchod[0] == 1 else 1
            current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            c.execute('''insert into pruchod(datum, karta_id, vchod) values(?, (select id from karta where uid = ?), ?)''', (current_datetime, uid, vchod))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Nastala chyba: {e}")
            return False
        finally:
            conn.close()
   
    def AddKarta(jmeno, UID):
        conn = sqlite3.connect(DATABASE_NAME)
        try:
            c = conn.cursor()
            c.execute('''insert into karta(jmeno, UID, valid) values(?,?,?)''', (jmeno, UID, True))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Nastala chyba: {e}")
            return False 
        finally:
            conn.close()

    def UpdateKarta(jmeno, uid, valid,old_uid):
        conn = sqlite3.connect(DATABASE_NAME)
        try:
            c = conn.cursor()
            c.execute('''update karta set jmeno = ?, valid = ?, uid = ? where uid = ?''', (jmeno, valid, uid, old_uid))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Nastala chyba: {e}")
            return False
        finally:
            conn.close()

    def GetKarty(howmany,page):
        conn = sqlite3.connect(DATABASE_NAME)
        try:
            c = conn.cursor()
            c.execute('''select jmeno, uid, valid from karta limit ? offset ?''', (howmany, (page-1)*howmany))
            rows = c.fetchall()
            return rows
        except sqlite3.Error as e:
            print(f"Nastala chyba: {e}")
        finally:
            conn.close()
    
    def GetPruchody(howmany, page, sort_order, start_date, end_date, specific_user):
        conn = sqlite3.connect(DATABASE_NAME)
        try:
            c = conn.cursor()
            query = '''select jmeno, datum, uid, vchod from pruchod join karta on karta.id = pruchod.karta_id'''
            params = []
            
            conditions = []

            if start_date:
                conditions.append('datum >= ?')
                params.append(start_date)
            if end_date:
                conditions.append('datum <= ?')
                params.append(end_date)
            if specific_user:
                conditions.append('karta.jmeno = ?')
                params.append(specific_user)

            if conditions:
                query += ' where ' + ' and '.join(conditions)

            query += ' order by datum {} limit ? offset ?'.format(sort_order)
            params.extend([howmany, (page-1)*howmany])

            c.execute(query, params)
            rows = c.fetchall()
            return rows
        except sqlite3.Error as e:
            print(f"Nastala chyba: {e}")
        finally:
            conn.close()
    
    def GetKartyUvnitr(howmany, page):
        conn = sqlite3.connect(DATABASE_NAME)
        try:
            c = conn.cursor()
            c.execute('''
                        select k.jmeno, p.datum, k.uid, p.vchod
                        from pruchod p
                        join karta k on p.karta_id = k.id
                        inner join (
                            select karta_id, MAX(datum) as max_datum
                            from pruchod
                            where DATE(datum) = DATE('now')
                            group by karta_id
                        ) latest on p.karta_id = latest.karta_id and p.datum = latest.max_datum
                        where p.vchod = 1 and DATE(p.datum) = DATE('now') and not exists (
                            select 1
                            from pruchod p2
                            where p2.karta_id = p.karta_id and p2.datum > p.datum
                        )
                        limit ? offset ?''', (howmany, (page-1)*howmany))
            rows = c.fetchall()
            return rows
        except sqlite3.Error as e:
            print(f"Nastala chyba: {e}")
        finally:
            conn.close()

