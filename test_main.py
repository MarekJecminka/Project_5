import pytest
import mysql.connector
from project_5 import (pripojeni_db, vytvoreni_tabulky, pridat_ukol, aktualizovat_ukol, odstranit_ukol)

test_db = "test_database_ukoly"

@pytest.fixture(scope = "function")
def db_setup():
    conn = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "1111"
    )

    cursor = conn.cursor()

    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {test_db}")
    conn.close()

    conn, cursor = pripojeni_db(test_db)
    vytvoreni_tabulky(conn, cursor)

    yield conn, cursor

    cursor.execute("DROP TABLE IF EXISTS ukoly")
    conn.commit()
    cursor.close()
    conn.close()

@pytest.mark.parametrize("nazev, popis, ocekavany_vysledek", [
    ("udělat domácí úkol", "spočítat příklady do matematiky", True),
    ("", "prazdný text", False)
])
def test_pridat_ukol(db_setup, nazev, popis, ocekavany_vysledek):
    conn, cursor = db_setup
    result = pridat_ukol(conn, cursor, nazev, popis)
    assert result == ocekavany_vysledek

    if ocekavany_vysledek:
        cursor.execute("SELECT nazev FROM ukoly WHERE nazev = %s", (nazev,))
        vysledek = cursor.fetchone()
        assert vysledek is not None
        assert vysledek[0] == nazev

@pytest.mark.parametrize("novy_stav, ocekavany_vysledek", [
    (1, True),
    (1, False)
])
def test_aktualizovat_ukol(db_setup, novy_stav, ocekavany_vysledek):
    conn, cursor = db_setup
    pridat_ukol(conn, cursor, "udělat domácí úkol", "spočítat příklady do matematiky")

    if ocekavany_vysledek:
        cursor.execute("SELECT id FROM ukoly WHERE id = 1")
        id = cursor.fetchone()[0]
    else:
        id = 2

    result = aktualizovat_ukol(conn, cursor, id, novy_stav)
    assert result == ocekavany_vysledek

@pytest.mark.parametrize("id, ocekavany_vysledek",[
    (1, True),
    (2, False)
])
def test_odstranit_ukol(db_setup, id, ocekavany_vysledek):
    conn, cursor = db_setup
    pridat_ukol(conn, cursor, "udělat domácí úkol", "spočítat příklady do matematiky")
    result = odstranit_ukol(conn, cursor, id)
    assert result == ocekavany_vysledek
    
    if ocekavany_vysledek:
        cursor.execute("SELECT nazev FROM ukoly WHERE id = 1")
        vysledek = cursor.fetchone()
        assert vysledek is None
