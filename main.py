"""
projekt_5.py: pátý projekt do Engeto Online Python Akademie

author: Marek Ječmínka
email: jecminkam@seznam.cz
"""

import mysql.connector

def pripojeni_db(db):
    try:
        conn = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "1111",
            database = db
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

def pridat_ukol(conn, cursor, nazev, popis):

    if not nazev or not popis:
        print("\nNázev i popis nesmí zůstat prázdné!")
        return False

    cursor.execute("INSERT INTO ukoly (nazev, popis, stav, datum_vytvoreni) VALUES (%s, %s, 'Nezahájeno', CURDATE())", (nazev, popis))
    conn.commit()
    print("\nÚkol '" + nazev + "' byl přidán.\n")
    return True

def zobrazit_ukoly(cursor, sql_stav, popis):
    print("\n")
    if sql_stav:
        sql_dotaz = "SELECT * FROM ukoly WHERE stav IN (%s, %s)"
        cursor.execute(sql_dotaz, sql_stav)
        ukoly = cursor.fetchall()
    else:
        sql_dotaz = "SELECT * FROM ukoly"
        cursor.execute(sql_dotaz)
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

def aktualizovat_ukol(conn, cursor, id, novy_stav):
    cursor.execute("SELECT id FROM ukoly WHERE id=%s",(id,))
    if not cursor.fetchone():
        print("Zadali jste neplatné ID.")
        return False

    if novy_stav == 1:
        cursor.execute("UPDATE ukoly SET stav='Probíhá' WHERE id=%s",(id,))
        conn.commit()
        return True

    elif novy_stav == 2:
        cursor.execute("UPDATE ukoly SET stav='Hotovo' WHERE id=%s",(id,))
        conn.commit()
        return True

    else:
        print("Zadali jste špatný vstup.")
        return False

def odstranit_ukol(conn, cursor, id):
    cursor.execute("SELECT id FROM ukoly WHERE id=%s",(id,))
    if not cursor.fetchone():
        print("Zadali jste neplatné ID.")
        return False
    
    cursor.execute("DELETE FROM ukoly WHERE id=%s",(id,))
    conn.commit()
    return True

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
                
                pridat_ukol(db_conn, db_cursor, nazev_ukolu, popis_ukolu)

        elif odpoved == "2":
            stav = ('Nezahájeno', 'Probíhá')
            zobrazit_popis = True
            zobrazit_ukoly(db_cursor, stav, zobrazit_popis)
        
        elif odpoved == "3":
            stav = ('Nezahájeno', 'Probíhá')
            zobrazit_popis = False

            cisla_ukolu = zobrazit_ukoly(db_cursor, stav, zobrazit_popis)

            while True:
                id_ukolu = int(input("\nZadejte číslo ID, u kterého chcete změnit stav: "))
                if id_ukolu in cisla_ukolu:
                    break
                else:
                    print("\nZadali jste neplatné ID úkolu.")

            while True:
                novy_stav_ukolu = int(input("\nPro změnu stavu na 'Probíhá' zmáčkněte číslo 1, pro změnu stavu na 'Hotovo' zmáčkněte číslo 2: "))
                if novy_stav_ukolu in (1,2):
                    break
                else:
                    print("Zadali jste neplatný vstup.")

            aktualizovat_ukol(db_conn, db_cursor, id_ukolu, novy_stav_ukolu)

        elif odpoved == "4":
            stav = None
            zobrazit_popis = False

            cisla_ukolu = zobrazit_ukoly(db_cursor, stav, zobrazit_popis)

            while True:
                    id_ukolu = int(input("\nZadejte číslo ID úkolu, který chcete odstranit: "))
                    if id_ukolu in cisla_ukolu:
                        break
                    else:
                        print("\nZadali jste neplatné ID úkolu.")

            odstranit_ukol(db_conn, db_cursor, id_ukolu)

        elif odpoved == "5":
            print("\nKonec programu.")
            db_cursor.close()
            db_conn.close()
            break

if __name__ == "__main__":
    db_name = "database_ukoly"
    db_conn, db_cursor = pripojeni_db(db_name)
    vytvoreni_tabulky(db_conn, db_cursor)
    hlavni_menu(db_conn, db_cursor)
