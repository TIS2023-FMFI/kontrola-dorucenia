import pandas as pd

ORDERS_DOCUMENT_PATH = 'C:/kontrola-dorucenia/website/Databaza_2023_project.xlsm'
ORDERS_SHEET_NAME = 'databaza'
CARRIERS_DOCUMENT_PATH = 'C:/kontrola-dorucenia/website/databaza_dopravcov.xlsx'


class Order:

    def __init__(self, order_code):
        workbook = pd.read_excel(ORDERS_DOCUMENT_PATH, sheet_name=ORDERS_SHEET_NAME)
        rows = workbook.loc[workbook['VF'] == order_code]

        if not rows.empty:
            indices = list(rows.index.values)
            first_index = indices[0]
            self.loading_ctr = rows.loc[first_index, 'LOADING CTR']
            self.loading_zip = rows.loc[first_index, 'LOADING ZIP']
            self.loading_city = rows.loc[first_index, 'LOADING CITY']
            self.loading_date = rows.loc[first_index, 'LOADING DATE']
            self.loading_time = rows.loc[first_index, 'LOADING TIME']
            self.delivery_ctr = rows.loc[first_index, 'DELIVERY CTR']
            self.delivery_zip = rows.loc[first_index, 'DELIVERY ZIP']
            self.delivery_city = rows.loc[first_index, 'DELIVERY CITY']
            self.delivery_date = rows.loc[first_index, 'DELIVERY DATE']
            self.delivery_time = rows.loc[first_index, 'DELIVERY TIME']
            self.booking_reference = rows.loc[first_index, 'BOOKING REFERENCE']
            self.truck_plates = rows.loc[first_index, 'TRUCK PLATES']
            self.carrier = rows.loc[first_index, 'CARRIER']
            self.vf = rows.loc[first_index, 'VF']
            self.pic = rows.loc[first_index, 'PIC']

    def exist(self):
        return hasattr(self, 'vf')


class Carrier:

    def __init__(self, carrier_code):
        workbook = pd.read_excel(CARRIERS_DOCUMENT_PATH)
        rows = workbook.loc[workbook['TPOP'] == carrier_code]

        if not rows.empty:
            indices = list(rows.index.values)
            first_index = indices[0]
            self.tpop = rows.loc[first_index, 'TPOP']
            self.carrier = rows.loc[first_index, 'Dopravca']
            self.dispatchers = []
            for i in indices:
                email = rows.loc[i, 'Mail']
                contact = rows.loc[i, 'Kontakt']
                language = rows.loc[i, 'Jazyk']
                self.dispatchers.append(Carrier_Dispatcher(email, contact, language))

    def exist(self):
        return hasattr(self, 'tpop')


class Carrier_Dispatcher:

    def __init__(self, email, contact, language):
        self.email = email
        self.contact = contact
        self.language = language
