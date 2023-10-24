from flask import Flask
import pandas as pd


app = Flask(__name__)


@app.route('/')
def test():
    workbook = pd.read_excel('../example.xls')
    rows = "Column First Name in excel document example.xls contains values : <br>"
    for index,row in workbook.iterrows():
        rows += row['First Name'] + ' <br> '
    return rows

if __name__ == '__main__':
    app.run(debug=True)
