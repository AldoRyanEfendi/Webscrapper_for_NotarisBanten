from selenium import webdriver
from selenium.webdriver.common.by import By
import PySimpleGUI as sg
import time

class WebScrapper:
    def __init__(self):
        self.credentials = {}
        self.details = {}
        self.map = {'Delete': 'delete', 'Login': 'login', 'Detail': 'input', 'Start': 'start', 'OK': 'menu', 'Cancel': 'menu', 'Exit': 'exit'}
        self.result = 'menu'
        self.context = None
        self.driver = None
        self.amount = None

    def find_element(self, finder, element):
        return self.driver.find_element(finder, element)

    def open_ui(self):
        WSM = WebScrapperMenu(self.result)
        self.result, values, self.context = WSM.main(self.map)
        
        if self.context == 'login':
            self.credentials = values.copy()
        elif self.context == 'input':
            self.details = values.copy()
        elif self.context == 'delete':
            self.amount = values['amount']

    def open_webdriver(self):
        self.driver = webdriver.Chrome(executable_path="./chromedriver.exe")
        self.driver.get(self.details['url'])
        self.driver.maximize_window()
        self.driver.implicitly_wait(1200)

    def login(self):
        self.find_element(By.NAME, 'username').send_keys(self.credentials['uname'])
        self.find_element(By.NAME, 'password').send_keys(self.credentials['password'])
        self.find_element(By.CLASS_NAME, 'btn-primary').click()

    def input_data(self):
        for x, y in enumerate(range(int(self.details['mulai']), int(self.details['selesai']))):
            self.driver.get(self.details['url'])
            self.find_element(By.NAME, 'serial').send_keys(x+int(self.details['urut']))
            self.find_element(By.NAME, 'monthly').send_keys(y)
            self.find_element(By.NAME, 'date').send_keys(self.details['tgl'])
            self.find_element(By.NAME, 'type').send_keys(self.details['akta'])
            self.find_element(By.NAME, 'appearer').send_keys(self.details['penghadap'])
            # self.find_element(By.CLASS_NAME, 'btn-primary').click()
            time.sleep(120)
            break

    def main(self):
        try:
            checks = {
                'uname': 'Username', 
                'password': 'Password', 
                'url': 'URL', 
                'mulai': 'Nomor Bulan Mulai', 
                'selesai': 'Nomor Bulan Selesai', 
                'urut': 'Nomor Urut', 
                'tgl': 'Tanggal',
                'akta': 'Jenis Akta',
                'penghadap' : 'Nama Penghadap'
                }
            while True:
                self.open_ui()

                if self.result == 'exit':
                    break

                if self.result == 'start':
                    msg = ''
                    if self.context != 'delete':
                        for key, val in checks.items():
                            if key in ['uname', 'password']:
                                if not self.credentials.get(key, False):
                                    msg = msg + f'{val} Belum Di isi!\n'
                            else:
                                if not self.details.get(key, False):
                                    msg = msg + f'{val} Belum Di isi!\n'
                        
                        if msg:
                            WarningWindow('Warning', f'{msg}')
                            self.result = 'menu'
                            continue

                        break
                    else:
                        if not self.amount:
                            WarningWindow('Warning', f'Jumlah tidak boleh kosong')
                            self.result = 'menu'
                            continue
                        break
                    
            if self.result == 'start':
                self.open_webdriver()
                self.login()
                print(self.context)
                self.input_data()

        except Exception as e:
            WarningWindow('Error', f'An Error Occured :\n{str(e)}')

class WarningWindow:
    def __init__(self, title, msg):
        layout = [[sg.Text(msg)], [sg.Button('OK')]]
        window = sg.Window(title, layout, element_justification='c')
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == 'OK':
                window.close()
                break

class WebScrapperMenu:
    def __init__(self, option):
        # Data
        self.context = option
        print(option)
        if option == 'input':
            self.layout = [
                    [sg.Text("URL")],
                    [sg.In(size=(50, 1), enable_events=True, key="url"),],
                    [sg.Text("Nomor Bulan Mulai")],
                    [sg.In(size=(50, 1), enable_events=True, key="mulai")],
                    [sg.Text("Nomor Bulan Selesai")],
                    [sg.In(size=(50, 1), enable_events=True, key="selesai")],
                    [sg.Text("Nomor urut")],
                    [sg.In(size=(50, 1), enable_events=True, key="urut")],
                    [sg.Text("Tanggal")],
                    [sg.In(size=(50, 1), enable_events=True, key="tgl")],
                    [sg.Text("Jenis Akta")],
                    [sg.In(size=(50, 1), enable_events=True, key="akta")],
                    [sg.Text("Nama Penghadap")],
                    [sg.In(size=(50, 1), enable_events=True, key="penghadap")],
                    [sg.Button('OK'), sg.Button('Cancel')]
                    ]
        elif option == 'menu':
            self.layout = [
                [sg.Button('Login'), sg.Button('Detail'), sg.Button('Start'), sg.Button('Delete'), sg.Button('Exit')]
            ]
        elif option == 'delete':
            self.layout = [
                [[sg.In(size=(50, 1), enable_events=True, key="URL"),], [sg.In(size=(50, 1), enable_events=True, key="amount"),], sg.Button('Start'), sg.Button('Cancel')]
            ]
        else:
            self.layout = [
                    [sg.Text("Username")],
                    [sg.In(size=(50, 1), enable_events=True, key="uname"),],
                    [sg.Text("Password")],
                    [sg.In(size=(50, 1), enable_events=True, key='password', password_char='*')],
                    [sg.Button('OK'), sg.Button('Cancel')]
            ]
        self.layout.insert(0, [sg.Text("Form Bot")])
        self.open_window()

    def open_window(self):
        self.window = sg.Window("Form Bot By Aldo Ryan Efendi", self.layout, element_justification='c')

    def close_windows(self):
        self.window.close()

    def main(self, map):
        # Create an event loop
        while True:
            event, values = self.window.read()
            if map.get(event, False):
                msg = map[event]
                self.close_windows()
                break

            if event == sg.WIN_CLOSED:
                msg = map['Exit']
                self.close_windows()
                break
        
        return msg, values, self.context

WS = WebScrapper()
WS.main()