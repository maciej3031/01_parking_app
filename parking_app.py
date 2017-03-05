# -*- coding: utf-8 -*-
import sys
from time import *
import math
import sqlite3

# polaczenie z baza danych i stworzenie kursora

con = sqlite3.connect("base.db")
con.row_factory = sqlite3.Row
c = con.cursor()


class DataBase():
    """ Klasa skupiajaca funkcje realizujace dzialania na bazie danych  """

    @staticmethod
    def create_table():
        """ tworzy tabele z nr rej samochodow, data zaparkowania, i terminem waznosci abonamentu """
        c.execute('CREATE TABLE IF NOT EXISTS park_table (reg TEXT PRIMARY KEY NOT NULL, entrdate DATETIME, expdate DATETIME)')

    @staticmethod
    def create_price_table():
        """ tworzy tabele cen ze stawka, okresem, kosztem abonamentu i okresem abonamentu
        W TEJ TABELI MUSI BYC ZAWSZE TYLKO JEDEN REKORD!!! """
        c.execute('CREATE TABLE IF NOT EXISTS price_table (stake REAL, term INTEGER, substake REAL, subterm INTEGER)')

    @staticmethod
    def read_record_from_db(reg):
        """ odczytuje wszystkie wartosci dla danego nr rejestracyjnego z tabeli z samochodami
         po podaniu nr rejestracyjnego. Zwraca liste tupli """
        c.execute("SELECT reg, entrdate, expdate FROM park_table WHERE reg = ? LIMIT 1", (reg,))
        data = c.fetchone()
        return data  # zwraca tuple postaci: (reg, entrdate, expdate)

    @staticmethod
    def read_from_db():
        """ odczytuje wszystkie rekordy z tabeli z samochodami
        zwraca liste tupli """
        c.execute("SELECT reg, entrdate, expdate FROM park_table ORDER BY reg ASC")
        data = c.fetchall()
        return data  # zwraca liste tupli

    @staticmethod
    def read_record_from_pricedb():
        """ odczytuje wartosci stawki, okresu, kosztu abonamentu i okresu abonamentu z tabeli cen
        zwraca liste tupli """
        c.execute("SELECT price_table.stake, term, substake, subterm FROM price_table LIMIT 1")
        data = c.fetchone()
        return data  # zwraca tuple postaci: [(stake, term, substake, subterm)]

    @staticmethod
    def insert_record_to_pricedb(stake, term, substake, subterm):
        """ wstawia rekord do tabeli cen - UWAGA UZYWAC TYLKO DO STWORZENIA PIERWSZEGO REKORDU """
        c.execute("INSERT INTO price_table (stake, term, substake, subterm) VALUES (? ,?, ?, ?)",
                  (stake, term, substake, subterm))
        con.commit()

    @staticmethod
    def insert_record_to_db(reg, entrdate, expdate = None):
        """ wstawia nowy rekord do tabeli samochodow """
        c.execute("INSERT INTO park_table (reg, entrdate, expdate) VALUES (? ,?, ?)", (reg, entrdate, expdate))
        con.commit()

    @staticmethod
    def update_entrdate_in_db(reg, entrdate):
        """ update'uje date wjazdu po podaniu nr rejestracyjnego, dla niezaparkowanego samochodu podawac NULL/None """
        c.execute("UPDATE park_table SET entrdate = ? WHERE reg = ? ", (entrdate, reg))
        con.commit()

    @staticmethod
    def update_abondate_in_db(reg, expdate):
        """ update'uje termin waznosci abonamentu, dla braku abonamentu podawac NULL/None """
        c.execute("UPDATE park_table SET expdate = ? WHERE reg = ? ", (expdate, reg))
        con.commit()

    @staticmethod
    def update_record_in_pricedb(stake, term, substake, subterm):
        """ update'uje wartosci stawki, okresu, kosztu abonamentu i okresu abonamentu w tabeli cen """
        c.execute("UPDATE price_table SET stake = ?, term = ?, substake = ?, subterm = ?", (stake, term,
                                                                                            substake, subterm))
        con.commit()

    @staticmethod
    def delete_record_in_db(reg):
        """ kasuje rekord w tabeli samochodow po podaniu nr rejestracyjnego UWAGA NIEODWRACALNE! """
        c.execute("DELETE FROM park_table WHERE reg = ?", (reg,))
        con.commit()


class Stakes():
    """ Klasa przechowujaca metody i dane o stawkach i okresach """

    stake = 1.00
    term = 30
    subterm = 30
    substake = 100.00

    @staticmethod
    def change_stakes():
        """ metoda zmieniajaca stawki """
        print("\nZmiana wysokosci oplat\n")
        print("Biezaca stawka wynosi %.2f zl za %i minut(y)\n" % (Stakes.stake, Stakes.term))
        print("Biezace stawki za abonament wynosza %.2f zl za %i dni\n" % (Stakes.substake, Stakes.subterm))
        try:
            s = float(input("Podaj nowa wysokosc oplat: "))         # wczytanie danych do zmiennych tymczasowych
            o = int(input("Podaj nowy czas naliczania w minutach: "))
            ak = float(input("Podaj nowa wysokosc abonamentu: "))
            ac = int(input("Podaj nowy czas trwania abonamentu w danich: "))
            assert all(i > 0 for i in [s, o, ak, ac])
        except AssertionError and ValueError:
            print("Blad wprowadzania danych! Stawka nie zostala zmieniona!")
            return
        try:
            DataBase.update_record_in_pricedb(s, o, ak, ac)  # zapisujemy w bazie
        except Exception:
            print("Blad zapisu danych! Stawka nie zostala zmieniona!")
        else:
            Stakes.stake = s  # kopiujemy do zmiennych klasy
            Stakes.term = o
            Stakes.subterm = ac
            Stakes.substake = ak
            del s, o, ac, ak


class Menu():
    """ Klasa przechowujaca menu glowne graficzne """

    @staticmethod
    def menu():
        """ metoda menu glownego programu """
        while True:
            print('-' * 85)
            print("PARKING".center(85))
            print('-' * 85)
            print("[W] Wjazd [E] Wyjazd [P} Pojazdy [S] Stawka [A] Przedluz/wykup abonament [K] Koniec".center(85))
            print('-' * 85)
            w = input()
            if not w:
                print("Nieznane polecenie")
            else:
                w = w[0].upper()  # pierwszy znak, duza litera
                if w in 'WEPSKA':  # jezeli podana przez uzytkownika litera jest poprawna to zwroc ja,
                    return w
                else:
                    print("Nieznane polecenie")  # jezeli nie zwroc "nieznane polecenie"
                    return


class Subscription():
    """ Klasa przechowujaca metody odpowiedzialne za zmiane abonamentu"""

    def __init__(self, reg):
        """ metoda inicjujaca """
        try:
            self.db_entry = DataBase.read_record_from_db(reg)   # przechowuje o danym nr rej dane z bazy danych
        except Exception:
            print("Blad odczytu danych z bazy danych!")
        self.status = self.read_status(self.db_entry)       # przechowuje status pojazdu
        self.reg = reg      # przechowuje nr rejestracyjny pojazdu

    def read_status(self, record):
        """ metoda odczytujaca status pojazdu """
        if not record:
            return "not_parked"      # () -> Brak auta na parkingu
        elif not record[1]:
            if mktime(strptime(record[2], "%H:%M (%Y-%m-%d)")) > mktime(localtime()):
                return "not_parked_with_sub"      # (rej,,expdate) -> Brak auta na parkingu, ale jest już wykupiony abonament
            else:
                return "not_parked_with_exp_sub"    # jak wyzej tylko z przeterminowanym abonamentem
        elif not record[2]:
            return "parked"         # (rej, entrdate) -> Zaparkowany bez abonamentu
        elif len(record) == 3:
            return "parked_with_sub"      # (rej, entrdate, expdate) -> zaparkowany z abonamentem

    @classmethod
    def from_input(cls):
        """ metoda pobierajaca nr rejestracyjny """
        reg = input("Podaj nr rejestracyjny pojazdu")[:9].upper()
        if not reg:
            print("Nie podano numeru rejestracyjnego")
            raise ValueError
        else:
            return cls(reg)

    def front_sub(self, status):
        """ metoda wyswietlajaca odpowiedni komunikat dla uzytkownika programu """
        if status == "parked":
            print("Uzytkownik nie posiada abonamentu lub ten sie skonczyl.\n Samochod znajduje sie na parkingu. Czy chcesz wykupic abonament? [Y/N]\nKoszt: %.2f zl; za %i dni" % (
                Stakes.substake, Stakes.subterm))
        elif status in ["not_parked", "not_parked_with_exp_sub"]:
            print("Uzytkownik nie posiada abonamentu lub ten sie skonczyl.\n Samochodu nie ma na parkingu. Czy chcesz wykupic abonament? [Y/N]\nKoszt: %.2f zl; za %i dni" % (
                Stakes.substake, Stakes.subterm))
        elif status == "parked_with_sub":
            print("Uzytkownik posiada abonament do ", self.db_entry[2],
                  "\nSamochod znajduje sie na parkingu. Czy chcesz go przedluzyc? [Y/N]\nKoszt: %.2f zl; za %i dni" % (
                      Stakes.substake, Stakes.subterm))
        elif status == "not_parked_with_sub":
            print("Uzytkownik posiada abonament do ", self.db_entry[2],
                  "\nSamochodu nie ma na parkingu. Czy chcesz go przedluzyc? [Y/N]\nKoszt: %.2f zl; za %i dni" % (
                      Stakes.substake, Stakes.subterm))
        else:
            print("Wystąpil blad, niepoprawny rekord w bazie danych")
            return True

    def decision(self):
        """ metoda realizujaca decyzje uzykownika """
        self.bool1 = input()
        if not self.bool1:
            print("Nie wykupiono abonamentu")
            return False
        if self.bool1[0].upper() == "N":
            print("Nie wykupiono abonamentu")
            return False
        elif self.bool1[0].upper() == "Y":
            return True

    def days_input(self):
        """ metoda rezlizujaca wybor dni przez uzytkownika """
        print("Na jak dlugi czas chcesz wykupic abonament? Podaj liczbe dni. Nie mniej niz 30 dni")
        self.days = input()
        try:
            self.days = int(self.days)
            if self.days >= 30:
                self.price = self.days * (Stakes.substake / Stakes.subterm)
                print("Koszt to: %.2f zl za %i dni" % (self.price, self.days))
                return self.days
            else:
                print("Za mala liczba dni!")
                return False
        except ValueError:
            print("Nie podano liczby dni!")
            return False

    def subscription_db_insert(self):
        try:
            # jezeli auto ma wykupiony, wazny abonament to dodaj wykupiona ilosc dni do obecnego terminu waznosci
            if self.status in ["parked_with_sub", "not_parked_with_sub"]:
                DataBase.update_abondate_in_db(self.reg, strftime("%H:%M (%Y-%m-%d)",
                                localtime(mktime(strptime(self.db_entry[2], "%H:%M (%Y-%m-%d)")) + self.days * 24 * 60 * 60)))
            # jezeli auto jest zaparkowane bez abonamentu to dodaj wykupiona ilosc dni do daty wjazdu
            elif self.status in ["parked"]:
                DataBase.update_abondate_in_db(self.reg, strftime("%H:%M (%Y-%m-%d)",
                                localtime(mktime(strptime(self.db_entry[1], "%H:%M (%Y-%m-%d)")) + self.days * 24 * 60 * 60)))
            # jezeli auto nie jest zaparkowane i ma przeterm. abon. to wykupiona ilosc dni dodaj do obecnego czasu
            elif self.status in ["not_parked_with_exp_sub"]:
                DataBase.update_abondate_in_db(self.reg, strftime("%H:%M (%Y-%m-%d)",
                                                            localtime(mktime(localtime()) + self.days * 24 * 60 * 60)))
            # jezeli auto nie jest zaparkowane to wykupiona ilosc dni dodaj do obecnego czasu. Inaczej niz w/w status bo
            # bo brak rekordu w bazie danych i nalezy uzyc innego zapytania (INSERT zamiast UPDATE)
            elif self.status in ["not_parked"]:
                DataBase.insert_record_to_db(self.reg, None, strftime("%H:%M (%Y-%m-%d)",
                                                            localtime(mktime(localtime()) + self.days * 24 * 60 * 60)))
        except Exception:
            print("Blad zapisu do bazy danych!")

    def subscription(self):
        """ metoda glowna wykupienia/przedluzenia abonamentu """
        if self.front_sub(self.status):     # jezeli metoda front_sub otrzyma status inny niz przewidzane to zakoncz
            return
        if not self.decision():     # jezeli metoda decision otrzyma decyzje "Nie" to zakoncz
            return
        self.days = self.days_input()
        self.subscription_db_insert()


class Parking():
    """ Klasa skupiajaca metody realizujace wjazd, wyjazd i wyswietlanie samochodow na parkingu """

    @staticmethod
    def vehicles():
        """ metoda pokazujaca liste pojazdow na parkingu i z abonamentem """
        print("-" * 85)
        print("Lista pojazdow na parkingu".center(85))
        print("-" * 85)
        print("|", "Nr rej.".center(10), "|", "Godz. parkowania".center(21), "|", " Abonament (Tak/Nie)".center(21),
               "|", "Termin abonamentu:".center(21) + "|")
        print("-" * 85)
        for record in DataBase.read_from_db():  # pobieramy po kolei kazdy rekord z tabeli samochodow
            if record["entrdate"]:
                if record["expdate"]:  # te samochody ktore maja abonament
                    print("|%11s |" % record[0], "%21s" % record[1], "|", "TAK".center(21), "|", "%20s" % record[2], "|")
                else:  # reszta bez abonamentu
                    print("|%11s |" % record[0], "%21s" % record[1], "|", "NIE".center(21), "|")
        print("-" * 85)
        print("Lista pojazdow niezaparkowanych z abonamentem".center(85))
        print("-" * 85)
        print(("|" + "Nr rej.".center(12) + "|" + " Abonament (Tak/Nie)".center(21) + "|" +
              "Termin abonamentu:".center(21) + "|").center(85))
        for record in DataBase.read_from_db():  # pobieramy po kolei kazdy rekord z tabeli samochodow
            if record[2] and not record[1]:  # bierzemy tylko te samochody ktore maja abonament i nie sa na parkingu
                print(("|%11s |" % record[0] + "TAK".center(21) + "|" + "%21s" % record[2] + "|").center(85))

    @staticmethod
    def leaving():
        """ metoda rejestrujaca wyjazd pojazdu z parkingu """
        print("Wyjazd pojazdu - godzina", strftime("%H:%M (%Y-%m-%d)"))
        print("Podaj nr rejestracyjny")
        reg = input()[:9].upper()
        if not reg:
            print("Nieznane polecenie")
        else:
            if DataBase.read_record_from_db(reg):  # sprawdzamy czy taki numer rejestracyjny jest w bazie to znaczy czy byl zaparkowany
                hour = DataBase.read_record_from_db(reg)["entrdate"]
                print("Godzina wjazdu: ", hour)
                hour = mktime(strptime(hour, "%H:%M (%Y-%m-%d)"))   # zamiana ze str na struct_time a potem na sekundy
                if DataBase.read_record_from_db(reg)[2]:  # sprawdzamy czy ma abonament tzn czy wartosc w kolumnie subterm nie jest rowna NULL
                    DataBase.update_entrdate_in_db(reg, None)  # ustawiamy wartosc w kolumnie entrdate na None/NULL
                else:
                    minutes = int(mktime(localtime()) - hour) / 60
                    units = math.ceil(minutes / Stakes.term)  # naliczanie za rozpoczety okres
                    print("\nDo zaplaty: %.2f zl" % (units * Stakes.stake))
                    DataBase.delete_record_in_db(reg)  # usuwamy wpis z bazy danych
            else:
                print("Blad!: Takiego pojazdu nie ma na parkingu!")

    @staticmethod
    def entrance():
        """ metoda rejestrujaca wjazd pojazdu na parking """
        reg = input("Podaj numer rejestracyjny pojazdu: ")[:9].upper()
        hour = strftime("%H:%M (%Y-%m-%d)")     # aby w bazie danych byla normalna data a nie liczba
        print("Wjazd pojazdu - godzina", hour)
        if not reg:
            print("Nieznane polecenie")
        else:
            if not DataBase.read_record_from_db(reg):  # sprawdzamy czy samochod nie jest zaparkowany tzn czy w bazie nie ma rekordu o podanej nazwie numeru rejestracyjnego
                DataBase.insert_record_to_db(reg, hour)
                print("Wprowadzono")
            elif not DataBase.read_record_from_db(reg)["entrdate"]:  # jezeli jest taki rekord w bazie to sprawdzamy czy samochodu nie ma na parkingu, czyli czy wartosc w kolumnie entrdate jest NULL
                DataBase.update_entrdate_in_db(reg, hour)
                print("Wprowadzono")
            else:
                print("Blad! Taki pojazd juz jest na parkingu!")


def choice():
    """ funkcja realizujaca wybor uzytkownika programu """
    while True:
        w = Menu.menu()
        if w == "K":        # jezeli litera zwrocona przez Menu.menu() jest rowna "K" to zakoncz program
            break
        elif w == "S":      # jezeli jest rowna "S" to wywolaj metode zmiany stawki
            Stakes.change_stakes()
        elif w == "P":      # jezeli jest rowna "P" to wywolaj metode pokazujaca stan parkingu
            Parking.vehicles()
        elif w == "E":      # jezeli jest rowna "E" to wywolaj metode realizujaca wyjazd z parkingu
            Parking.leaving()
        elif w == "W":      # jezeli jest rowna "W" to wywolaj metode realizujaca wjazd na parking
            Parking.entrance()
        elif w == "A":      # jezeli jest rowna "A" to wywolaj metode realizujaca zmianę abonamentu
            try:
                Subscription.from_input().subscription()
            except ValueError:      # proba wylapania wyjatku w ktorym nie podano nr rejestracyjnego
                pass


def init():
    """ funkcja inicjalizujaca baze danych """
    try:
        DataBase.create_table()  # otwarcie bazy danych
        DataBase.create_price_table()
    except Exception:
        print("Blad krytyczny! Baza danych nie zostala otwarta!")
        sys.exit(0)  # wyjscie z programu
    print("Inicjalizacja udana. Bazy danych zostaly otworzone")
    if DataBase.read_record_from_pricedb():  # czy juz istnieje rekord ze stawkami w bazie
        (Stakes.stake, Stakes.term, Stakes.substake, Stakes.subterm) = DataBase.read_record_from_pricedb()  # jezeli tak to kopiujemy stawki
    else:
        DataBase.insert_record_to_pricedb(Stakes.stake, Stakes.term, Stakes.substake, Stakes.subterm)
        Stakes.change_stakes()  # jezeli nie - wczytujemy od uzytkownika


# program glowny

if __name__ == "__main__":
    init()  # otwarcie bazy
    try:
        choice()  # interfejs uzytkownika
    except Exception:
         print("Wystapil powazny blad!")
    c.close()
    con.close()  # zamkniecie bazy