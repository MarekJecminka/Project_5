"""
projekt_5.py: pátý projekt do Engeto Online Python Akademie

author: Marek Ječmínka
email: jecminkam@seznam.cz
"""

import mysql.connector
import pytest

def pripojeni_db():
    try:
        conn = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "1111",
            database = "database_ukoly"
        )
        print("Připojení k databázi bylo úspěšné.")
    except mysql.connector.Error as err:
        print(f"Chyba při připojování: {err}")

    cursor = conn.cursor()
    return conn, cursor

def vytvoreni_tabulky(conn, cursor):
    cursor.execute("""CREATE TABLE IF NOT EXISTS ukoly(
        id INT AUTO_INCREMENT PRIMARY KEY,
        nazev VARCHAR(50),
        popis VARCHAR(500),
        stav VARCHAR(20),
        datum_vytvoreni DATE
        )""")
    conn.commit()

def pridat_ukol(conn, cursor):
    while True:
        nazev_ukolu = input("\nZadejte název úkolu: ")
        if nazev_ukolu == "":
            print("\nZadali jste prázdný vstup. Zadejte znovu název úkolu.")
        else:
            break

    while True:
        popis_ukolu = input("Zadejte popis úkolu: ")
        if popis_ukolu == "":
            print("\nZadali jste prázdný vstup. Zadejte znovu popis úkolu.")
        else:
            break

    cursor.execute("""INSERT INTO ukoly (nazev, popis, stav, datum_vytvoreni) VALUES (%s, %s, 'nezahájeno', CURDATE())""", (nazev_ukolu, popis_ukolu))
    conn.commit()

    print("\nÚkol '" + nazev_ukolu + "' byl přidán.\n")

def zobrazit_ukoly(cursor, sql_stav, popis):
    print("\n")
    cursor.execute(f"SELECT * FROM ukoly {sql_stav}")
    ukoly = cursor.fetchall()

    cisla_ukolu = []
    if not ukoly:
        print("Seznam úkolů je prázdný.")
    else:
        for ukol in ukoly:
            if popis:
                print(
                    f"- ID úkolu: {ukol[0]}",
                    f"- Název: {ukol[1]}",
                    f"- Popis: {ukol[2]}",
                    f"- Stav: {ukol[3]}\n",
                    sep = "\n")
            else:
                print(
                    f"- ID úkolu: {ukol[0]}",
                    f"- Název: {ukol[1]}",
                    f"- Stav: {ukol[3]}\n",
                    sep = "\n")
            cisla_ukolu.append(int(ukol[0]))

    return cisla_ukolu

def aktualizovat_ukol(conn, cursor, sql_stav, popis):
    cisla_ukolu = zobrazit_ukoly(cursor, sql_stav, popis)

    while True:
        id = int(input("\nZadejte číslo ID, u kterého chcete změnit stav: "))
        if id in cisla_ukolu:
            break
        else:
            print("\nZadali jste neplatné ID úkolu.")

    while True:
        novy_stav = int(input("\nPro změnu stavu na 'Probíhá' zmáčkněte číslo 1, pro změnu stavu na 'Hotovo' zmáčkněte číslo 2: "))
        if novy_stav in (1,2):
            break
        else:
            print("Zadali jste neplatný vstup.")

    if novy_stav == 1:
        cursor.execute(f"UPDATE ukoly SET stav='Probíhá' WHERE id={id}")
        conn.commit()

    elif novy_stav == 2:
        cursor.execute(f"UPDATE ukoly SET stav='Hotovo' WHERE id={id}")
        conn.commit()

def odstranit_ukol(conn, cursor, sql_stav, popis):
    cisla_ukolu = zobrazit_ukoly(cursor, sql_stav, popis)
    
    while True:
        id = int(input("\nZadejte číslo ID úkolu, který chcete odstranit: "))
        if id in cisla_ukolu:
            break
        else:
            print("\nZadali jste neplatné ID úkolu.")

    cursor.execute(f"DELETE FROM ukoly WHERE id={id}")
    conn.commit()

def hlavni_menu(db_conn, db_cursor):
    while True:
        print(
            "",
            "Správce úkolů - Hlavní menu:",
            "1. Přidat úkol",
            "2. Zobrazit úkoly",
            "3. Aktualizovat úkol",
            "4. Odstranit úkol",
            "5. Ukončit program",
            sep = "\n")

        odpoved = input("\nVyberte možnost (1-5): ")

        if int(odpoved) not in range(1,6):
            print("\nNeplatný vstup. Zadej číslo od 1 do 5.")
        elif odpoved == "1":
            pridat_ukol(db_conn, db_cursor)
        elif odpoved == "2":
            stav = "WHERE stav = 'nezahájeno' OR stav = 'probíhá'"
            zobrazit_popis = True
            zobrazit_ukoly(db_cursor, stav, zobrazit_popis)
        elif odpoved == "3":
            stav = "WHERE stav = 'nezahájeno' OR stav = 'probíhá'"
            zobrazit_popis = False
            aktualizovat_ukol(db_conn, db_cursor, stav, zobrazit_popis)
        elif odpoved == "4":
            stav = ""
            zobrazit_popis = False
            odstranit_ukol(db_conn, db_cursor, stav, zobrazit_popis)
        elif odpoved == "5":
            print("\nKonec programu.")
            db_cursor.close()
            db_conn.close()
            break

if __name__ == "__main__":
    db_conn, db_cursor = pripojeni_db()
    vytvoreni_tabulky(db_conn, db_cursor)
    hlavni_menu(db_conn, db_cursor)
