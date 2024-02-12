import pandas as pd
from datetime import datetime
import os

ORDERS_ATTACHMENTS_PATH = 'website/attachments'
ORDERS_SHEET_NAME = 'databaza'
CARRIERS_DOCUMENT_PATH = 'website/databaza_dopravcov.xlsx'


class Order:

    def __init__(self, order_code):
        
        for filename in os.listdir(ORDERS_ATTACHMENTS_PATH):
            
            workbook = pd.read_excel(f'{ORDERS_ATTACHMENTS_PATH}/{filename}', sheet_name=None)
            for sheet in workbook.values():
                
                try:
                    rows = sheet.loc[sheet['VF'] == order_code]
                    if not rows.empty:
                        
                        indices = list(rows.index.values)
                        first_index = indices[0]
                        self.client = rows.loc[first_index, 'CLIENT']
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
                        break
                    
                except Exception as e:
                    print(e)

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


RESPONSE_DOCUMENT_PATH = 'Evidencia_nezhod.xlsx'


class Evidencia_nezhod:

    def __init__(self):
        # Load existing data from the Excel file if it exists
        try:
            self.data = pd.read_excel(RESPONSE_DOCUMENT_PATH)
        except FileNotFoundError:
            self.data = pd.DataFrame(columns=[
                'INES carrier file', 'Date of record', 'Responsible´s name',
                'Loading date', 'Loading time', 'Unloading date',
                'Unloading time', 'New date', 'New time',
                'Type of non-conformity', 'Root cause', 'Comment', 'Recorded by'
            ])

    def add_response(self, order_code, order, carrier, date, time, non_conformity, root_cause, comment, dispatcher):
        today = datetime.today().strftime('%Y-%m-%d')
        new_data = {
            'INES carrier file': order_code,
            'Date of record': today,
            'Responsible´s name': carrier,
            'Loading date': str(order.loading_date).split(' ')[0],
            'Loading time': order.loading_time,
            'Unloading date': str(order.delivery_date).split(' ')[0],
            'Unloading time': order.delivery_time,
            'New date': date,
            'New time': time,
            'Type of non-conformity': non_conformity,
            'Root cause': root_cause,
            'Comment': comment,
            'Recorded by': dispatcher
        }
        self.data = pd.concat([self.data, pd.DataFrame([new_data])], ignore_index=True)

    def write_to_excel(self):
        df = self.data
        writer = pd.ExcelWriter(RESPONSE_DOCUMENT_PATH)
        df.to_excel(writer, sheet_name='sheetName', index=False, na_rep='NaN')

        for column in df:
            column_length = max(df[column].astype(str).map(len).max(), len(column))
            col_idx = df.columns.get_loc(column)
            writer.sheets['sheetName'].set_column(col_idx, col_idx, column_length)

        writer.close()


def getLanguage(order_code, carrier_email):
    order = Order(order_code)
    carrier = Carrier(order.carrier)
    for dispatcher in carrier.dispatchers:
        if dispatcher.email == carrier_email:
            return dispatcher.language
