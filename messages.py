# -*- coding: utf-8 -*-
class CommonMessage:
    unknown_cmd = "Nieznane polecenie"
    set_reg_number = "Podaj numer rejestracyjny pojazdu: "


class StakesMessage:
    stakes_changing = "\nZmiana wysokosci oplat\n"
    current_stake = "Biezaca stawka wynosi %.2f zl za %i minut(y)\n"
    current_sub = "Biezace stawki za abonament wynosza %.2f zl za %i dni\n"
    set_new_stake = "Podaj nowa wysokosc oplat: "
    set_new_time = "Podaj nowy czas naliczania w minutach: "
    set_new_sub_stake = "Podaj nowa wysokosc abonamentu: "
    set_new_sub_time = "Podaj nowy czas trwania abonamentu w danich: "
    error_stakes_not_changed = "Blad wprowadzania danych! Stawka nie zostala zmieniona!"
    db_error = "Blad zapisu danych! Stawka nie zostala zmieniona!"


class MenuMessage(CommonMessage):
    parking = "PARKING"
    menu_options = "[W] Wjazd [E] Wyjazd [P} Pojazdy [S] Stawka [A] Przedluz/wykup abonament [K] Koniec"
    menu_letters = 'WEPSKA'


class SubscriptionMessage(CommonMessage):
    db_read_error = "Blad odczytu danych z bazy danych!"
    no_reg_number_given = "Nie podano numeru rejestracyjnego"
    parked_no_sub = "Uzytkownik nie posiada abonamentu lub ten sie skonczyl.\n Samochod znajduje sie na parkingu. Czy chcesz wykupic abonament? [Y/N]\nKoszt: %.2f zl; za %i dni"
    not_parked_no_sub = "Uzytkownik nie posiada abonamentu lub ten sie skonczyl.\n Samochodu nie ma na parkingu. Czy chcesz wykupic abonament? [Y/N]\nKoszt: %.2f zl; za %i dni"
    parked_with_sub = "\nSamochod znajduje sie na parkingu. Czy chcesz go przedluzyc? [Y/N]\nKoszt: %.2f zl; za %i dni"
    not_parked_with_sub = "\nSamochodu nie ma na parkingu. Czy chcesz go przedluzyc? [Y/N]\nKoszt: %.2f zl; za %i dni"
    user_has_sub = "Uzytkownik posiada abonament do "
    db_error = "Wystąpil blad, niepoprawny rekord w bazie danych"
    sub_not_purchased = "Nie wykupiono abonamentu"
    how_long_sub = "Na jak dlugi czas chcesz wykupic abonament? Podaj liczbe dni. Nie mniej niz 30 dni"
    sub_cost = "Koszt to: %.2f zl za %i dni"
    too_few_days_error = "Za mala liczba dni!"
    no_days_given_error = "Nie podano liczby dni!"
    db_save_error = "Blad zapisu do bazy danych!"


class ParkingMessage(CommonMessage):
    # vehicles
    parked_vehicles = "Lista pojazdow na parkingu"
    reg_num = "Nr rej."
    parked_hour = "Godz. parkowania"
    subs_yes_no = " Abonament (Tak/Nie)"
    subs_term = "Termin abonamentu:"
    yes = "TAK"
    no = "NIE"
    not_parked_vehicles_with_sub = "Lista pojazdow niezaparkowanych z abonamentem"

    # leaving
    vehicle_leaving = "Wyjazd pojazdu - godzina"
    entrance_hour = "Godzina wjazdu: "
    to_pay = "\nDo zaplaty: %.2f zl"
    error_no_such_vehicle_parked = "Blad!: Takiego pojazdu nie ma na parkingu!"

    # entrance
    vehicle_entrance = "Wjazd pojazdu - godzina"
    inserted = "Wprowadzono"
    error_vehicle_already_parked = "Blad! Taki pojazd juz jest na parkingu!"


class MainMessage:
    serious_error = "Wystapil powazny blad!"
    db_critical_error = "Blad krytyczny! Baza danych nie zostala otwarta!"
    db_init_success = "Inicjalizacja udana. Bazy danych zostaly otworzone"
