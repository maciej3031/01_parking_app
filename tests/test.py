# -*- coding: utf-8 -*-
import unittest
from unittest.mock import patch
from parking_app import *
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class ParkingTest(unittest.TestCase):
    """Parking testing class"""

    def setUp(self):
        @patch('builtins.input', return_value='10')
        def stake_setup(m_input):
            init()
            Stakes.change_stakes()

        stake_setup()

    def tearDown(self):
        c.execute("DROP TABLE park_table")
        c.execute("DROP TABLE price_table")
        con.commit()

    def test_db_init(self):
        if not hasattr(sys.stdout, "getvalue"):
            self.fail("need to run in buffered mode")
        output = sys.stdout.getvalue().strip()
        self.assertIn("Inicjalizacja udana. Bazy danych zostaly otworzone", output)

    @patch('builtins.input', return_value='')
    def test_change_stakes_invalid_data(self, m_input):
        Stakes.change_stakes()
        output = sys.stdout.getvalue().strip()
        self.assertIn("Blad wprowadzania danych! Stawka nie zostala zmieniona!", output)

    @patch('builtins.input', return_value='10')
    def test_change_stakes(self, m_input):
        Stakes.change_stakes()
        c.execute("SELECT * FROM price_table LIMIT 1")
        data = [i for i in c.fetchone()]
        self.assertTrue(data == [10.0, 10, 10.0, 10])

    @patch('builtins.input', return_value='w')
    def test_n_input_menu_W(self, m_input):
        response = Menu.menu()
        self.assertTrue(response == 'W')

    @patch('builtins.input', return_value='e')
    def test_n_input_menu_E(self, m_input):
        response = Menu.menu()
        self.assertTrue(response == 'E')

    @patch('builtins.input', return_value='p')
    def test_n_input_menu_P(self, m_input):
        response = Menu.menu()
        self.assertTrue(response == 'P')

    @patch('builtins.input', return_value='s')
    def test_n_input_menu_S(self, m_input):
        response = Menu.menu()
        self.assertTrue(response == 'S')

    @patch('builtins.input', return_value='a')
    def test_n_input_menu_A(self, m_input):
        response = Menu.menu()
        self.assertTrue(response == 'A')

    @patch('builtins.input', return_value='k')
    def test_n_input_menu_K(self, m_input):
        response = Menu.menu()
        self.assertTrue(response == 'K')

    @patch('builtins.input', return_value='1')
    def test_n_input_menu_unknown(self, m_input):
        response = Menu.menu()
        self.assertTrue(response is None)
        output = sys.stdout.getvalue().strip()
        self.assertIn("Nieznane polecenie", output)

    @patch('builtins.input', return_value='wx123')
    def test_entrance_no_abonament(self, m_input):
        Parking.entrance()
        output = sys.stdout.getvalue().strip()
        self.assertIn("Wprowadzono", output)
        c.execute("SELECT reg FROM park_table WHERE reg = ?", ('WX123',))
        data = c.fetchone()
        self.assertTrue(data)

    @patch('builtins.input', return_value='')
    def test_entrance_no_reg(self, m_input):
        Parking.entrance()
        output = sys.stdout.getvalue().strip()
        self.assertIn("Nieznane polecenie", output)
        c.execute("SELECT reg FROM park_table WHERE reg = ?", ('',))
        data = c.fetchone()
        self.assertFalse(data)

    @patch('builtins.input', return_value='ww123')
    def test_invalid_entrance_car_already_parked(self, m_input):
        Parking.entrance()
        Parking.entrance()
        output = sys.stdout.getvalue().strip()
        self.assertIn("Blad! Taki pojazd juz jest na parkingu!", output)

    @patch('builtins.input', return_value='ww123')
    def test_leaving_no_abonament(self, m_input):
        time = strftime("%H:%M (%Y-%m-%d)", localtime(mktime(localtime()) - 77 * 60))
        DataBase.insert_record_to_db('WW123', time, expdate=None)
        Parking.leaving()
        output = sys.stdout.getvalue().strip()
        self.assertIn("Godzina wjazdu:  {}".format(time), output)
        self.assertIn("Do zaplaty: 80.00 zl", output)

    @patch('builtins.input', return_value='ww123')
    def test_leaving_with_abonament(self, m_input):
        time1 = strftime("%H:%M (%Y-%m-%d)", localtime(mktime(localtime()) - 75 * 60))
        time2 = strftime("%H:%M (%Y-%m-%d)", localtime(mktime(localtime()) + 24 * 60 * 60))
        DataBase.insert_record_to_db('WW123', time1, time2)
        Parking.leaving()
        output = sys.stdout.getvalue().strip()
        self.assertIn("Godzina wjazdu:  {}".format(time1), output)
        self.assertTrue("Do zaplaty: 80.0 zl" not in output)

    @patch('builtins.input', return_value='ww123')
    def test_leaving_invalid_no_car_parked(self, m_input):
        Parking.entrance()
        Parking.leaving()
        Parking.leaving()
        output = sys.stdout.getvalue().strip()
        self.assertIn("Blad!: Takiego pojazdu nie ma na parkingu!", output)

    @patch('builtins.input', return_value='ww123')
    def test_show_parked_vehicles(self, m_input):
        Parking.entrance()
        Parking.vehicles()
        output = sys.stdout.getvalue().strip()
        self.assertIn("Lista pojazdow na parkingu", output)
        self.assertIn("Lista pojazdow niezaparkowanych z abonamentem", output)
        self.assertIn("WW123", output)

    @patch('builtins.input', return_value='')
    def test_subscription_no_input_reg(self, m_input):
        try:
            Subscription.from_input()
        except ValueError:
            pass
        finally:
            output = sys.stdout.getvalue().strip()
            self.assertIn("Nie podano numeru rejestracyjnego", output)

    @patch('builtins.input', return_value='wa123')
    def test_subscription_input_reg_and_status_not_parked(self, m_input):
        response = Subscription.from_input()
        self.assertTrue("not_parked" == response.status)
        self.assertTrue("WA123" == response.reg)

    @patch('builtins.input', return_value='wa123')
    def test_subscription_input_reg_and_status_not_parked_with_sub(self, m_input):
        time = strftime("%H:%M (%Y-%m-%d)", localtime(mktime(localtime()) + 24 * 60 * 60))
        c.execute("INSERT INTO park_table (reg, entrdate, expdate) VALUES (? ,?, ?)", ('WA123', None, time))
        con.commit()
        response = Subscription.from_input()
        self.assertTrue("not_parked_with_sub" == response.status)
        self.assertTrue("WA123" == response.reg)

    @patch('builtins.input', return_value='wa123')
    def test_subscription_input_reg_and_status_not_parked_with_exp_sub(self, m_input):
        time = strftime("%H:%M (%Y-%m-%d)", localtime(mktime(localtime()) - 24 * 60 * 60))
        c.execute("INSERT INTO park_table (reg, entrdate, expdate) VALUES (? ,?, ?)", ('WA123', None, time))
        con.commit()
        response = Subscription.from_input()
        self.assertTrue("not_parked_with_exp_sub" == response.status)
        self.assertTrue("WA123" == response.reg)

    @patch('builtins.input', return_value='wa123')
    def test_subscription_input_reg_and_status_parked(self, m_input):
        time = strftime("%H:%M (%Y-%m-%d)", localtime(mktime(localtime()) - 24 * 60 * 60))
        c.execute("INSERT INTO park_table (reg, entrdate, expdate) VALUES (? ,?, ?)", ('WA123', time, None))
        con.commit()
        response = Subscription.from_input()
        self.assertTrue("parked" == response.status)
        self.assertTrue("WA123" == response.reg)

    @patch('builtins.input', return_value='wa123')
    def test_subscription_input_reg_and_status_parked_with_sub(self, m_input):
        time1 = strftime("%H:%M (%Y-%m-%d)", localtime(mktime(localtime()) - 24 * 60 * 60))
        time2 = strftime("%H:%M (%Y-%m-%d)", localtime(mktime(localtime()) + 24 * 60 * 60))
        c.execute("INSERT INTO park_table (reg, entrdate, expdate) VALUES (? ,?, ?)", ('WA123', time1, time2))
        con.commit()
        response = Subscription.from_input()
        self.assertTrue("parked_with_sub" == response.status)
        self.assertTrue("WA123" == response.reg)

    def test_subscription_front_sub_no_status(self):
        sub = Subscription('')
        sub.status = ''
        response = sub.front_sub(sub.status)
        output = sys.stdout.getvalue().strip()
        self.assertIn('Wystąpil blad, niepoprawny rekord w bazie danych', output)
        self.assertTrue(response)

    def test_subscription_front_sub_status_parked(self):
        sub = Subscription('')
        sub.status = 'parked'
        sub.front_sub(sub.status)
        output = sys.stdout.getvalue().strip()
        self.assertIn('Uzytkownik nie posiada abonamentu lub ten sie skonczyl.\n Samochod znajduje sie na parkingu. Czy chcesz wykupic abonament? [Y/N]', output)

    def test_subscription_front_sub_status_not_parked(self):
        sub = Subscription('WA123')
        sub.front_sub(sub.status)
        output = sys.stdout.getvalue().strip()
        self.assertIn('Uzytkownik nie posiada abonamentu lub ten sie skonczyl.\n Samochodu nie ma na parkingu. Czy chcesz wykupic abonament? [Y/N]', output)

    def test_subscription_front_sub_status_parked_with_sub(self):
        time1 = strftime("%H:%M (%Y-%m-%d)", localtime(mktime(localtime()) - 24 * 60 * 60))
        time2 = strftime("%H:%M (%Y-%m-%d)", localtime(mktime(localtime()) + 24 * 60 * 60))
        c.execute("INSERT INTO park_table (reg, entrdate, expdate) VALUES (? ,?, ?)", ('WA123', time1, time2))
        con.commit()
        sub = Subscription('WA123')
        sub.front_sub(sub.status)
        output = sys.stdout.getvalue().strip()
        self.assertIn('Uzytkownik posiada abonament do', output)
        self.assertIn('Samochod znajduje sie na parkingu. Czy chcesz go przedluzyc? [Y/N]', output)

    def test_subscription_front_sub_status_not_parked_with_sub(self):
        time = strftime("%H:%M (%Y-%m-%d)", localtime(mktime(localtime()) + 24 * 60 * 60))
        c.execute("INSERT INTO park_table (reg, entrdate, expdate) VALUES (? ,?, ?)", ('WA123', None, time))
        con.commit()
        sub = Subscription('WA123')
        sub.front_sub(sub.status)
        output = sys.stdout.getvalue().strip()
        self.assertIn('Uzytkownik posiada abonament do', output)
        self.assertIn('Samochodu nie ma na parkingu. Czy chcesz go przedluzyc? [Y/N]', output)

    @patch('builtins.input', return_value='')
    def test_subscription_decision_no_input(self, m_input):
        sub = Subscription('WA123')
        sub.decision()
        output = sys.stdout.getvalue().strip()
        self.assertIn('Nie wykupiono abonamentu', output)

    @patch('builtins.input', return_value='n')
    def test_subscription_decision_N(self, m_input):
        sub = Subscription('WA123')
        response = sub.decision()
        output = sys.stdout.getvalue().strip()
        self.assertIn('Nie wykupiono abonamentu', output)
        self.assertFalse(response)

    @patch('builtins.input', return_value='y')
    def test_subscription_decision_Y(self, m_input):
        sub = Subscription('WA123')
        response = sub.decision()
        self.assertTrue(response)

    @patch('builtins.input', return_value='')
    def test_subscription_days_input_no_input(self, m_input):
        sub = Subscription('')
        response = sub.days_input()
        output = sys.stdout.getvalue().strip()
        self.assertIn('Nie podano liczby dni!', output)
        self.assertFalse(response)

    @patch('builtins.input', return_value='12')
    def test_subscription_days_input_to_little_number_of_days(self, m_input):
        sub = Subscription('')
        response = sub.days_input()
        output = sys.stdout.getvalue().strip()
        self.assertIn('Za mala liczba dni!', output)
        self.assertFalse(response)

    @patch('builtins.input', return_value='31')
    def test_subscription_days_input(self, m_input):
        sub = Subscription('')
        response = sub.days_input()
        output = sys.stdout.getvalue().strip()
        self.assertIn('Koszt to: ', output)
        self.assertTrue(response == 31)

    def test_subscription_db_insert_status_parked_with_sub(self):
        time1 = strftime("%H:%M (%Y-%m-%d)", localtime(mktime(localtime()) - 24 * 60 * 60))
        time2 = strftime("%H:%M (%Y-%m-%d)", localtime(mktime(localtime()) + 24 * 60 * 60))
        c.execute("INSERT INTO park_table (reg, entrdate, expdate) VALUES (? ,?, ?)", ('WX123', time1, time2))
        con.commit()
        sub = Subscription('WX123')
        sub.days = 30
        sub.subscription_db_insert()
        c.execute("SELECT expdate FROM park_table WHERE reg = ? LIMIT 1", ('WX123',))
        data = [i for i in c.fetchone()]
        time3 = strftime("%H:%M (%Y-%m-%d)", localtime(mktime(localtime()) + 31 * 24 * 60 * 60))
        self.assertTrue(data == [time3])

    def test_subscription_db_insert_status_not_parked_with_sub(self):
        time2 = strftime("%H:%M (%Y-%m-%d)", localtime(mktime(localtime()) + 24 * 60 * 60))
        c.execute("INSERT INTO park_table (reg, entrdate, expdate) VALUES (? ,?, ?)", ('WX123', None, time2))
        con.commit()
        sub = Subscription('WX123')
        sub.days = 30
        sub.subscription_db_insert()
        c.execute("SELECT expdate FROM park_table WHERE reg = ? LIMIT 1", ('WX123',))
        data = [i for i in c.fetchone()]
        time3 = strftime("%H:%M (%Y-%m-%d)", localtime(mktime(localtime()) + 31 * 24 * 60 * 60))
        self.assertTrue(data == [time3])

    def test_subscription_db_insert_status_parked(self):
        time1 = strftime("%H:%M (%Y-%m-%d)", localtime(mktime(localtime()) - 24 * 60 * 60))
        c.execute("INSERT INTO park_table (reg, entrdate, expdate) VALUES (? ,?, ?)", ('WX123', time1, None))
        con.commit()
        sub = Subscription('WX123')
        sub.days = 30
        sub.subscription_db_insert()
        c.execute("SELECT expdate FROM park_table WHERE reg = ? LIMIT 1", ('WX123',))
        data = [i for i in c.fetchone()]
        time3 = strftime("%H:%M (%Y-%m-%d)", localtime(mktime(localtime()) + 29 * 24 * 60 * 60))
        self.assertTrue(data == [time3])

    def test_subscription_db_insert_status_not_parked_with_exp_sub(self):
        time1 = strftime("%H:%M (%Y-%m-%d)", localtime(mktime(localtime()) - 15 * 24 * 60 * 60))
        c.execute("INSERT INTO park_table (reg, entrdate, expdate) VALUES (? ,?, ?)", ('WX123', None, time1))
        con.commit()
        sub = Subscription('WX123')
        sub.days = 30
        sub.subscription_db_insert()
        c.execute("SELECT expdate FROM park_table WHERE reg = ? LIMIT 1", ('WX123',))
        data = [i for i in c.fetchone()]
        time3 = strftime("%H:%M (%Y-%m-%d)", localtime(mktime(localtime()) + 30 * 24 * 60 * 60))
        self.assertTrue(data == [time3])

    def test_subscription_db_insert_status_not_parked(self):
        sub = Subscription('WX123')
        sub.days = 35
        sub.subscription_db_insert()
        c.execute("SELECT expdate FROM park_table WHERE reg = ? LIMIT 1", ('WX123',))
        data = [i for i in c.fetchone()]
        time3 = strftime("%H:%M (%Y-%m-%d)", localtime(mktime(localtime()) + 35 * 24 * 60 * 60))
        self.assertTrue(data == [time3])


if __name__ == '__main__':
    unittest.main(module=__name__, buffer=True, exit=False)
    os.chdir(basedir)
    c.close()
    con.close()
    os.remove('base.db')

