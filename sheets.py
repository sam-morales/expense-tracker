import datetime
from pytz import timezone
import gspread
from oauth2client.service_account import ServiceAccountCredentials

class Sheets:

    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    client = gspread.authorize(creds)

    def add_expense(self, description, amount, category, method, invoice="", receipt_link=""):
        sheet = self.client.open('Budget').sheet1
        row = [str(datetime.date.today()),
                #str(datetime.datetime.now(timezone('US/Eastern')).strftime('%H:%M:%S')),
                description,
                invoice,
                amount,
                category,
                receipt_link,
                method]
        sheet.append_row(row, value_input_option='USER_ENTERED')
