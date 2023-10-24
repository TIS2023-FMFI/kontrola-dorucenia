from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
import pandas as pd


workbook = pd.read_excel('../example.xls')

def index(request):
    rows = "Column First Name in excel document example.xls contains values : <br>"
    for index,row in workbook.iterrows():
        rows += row['First Name'] + ' <br> '
    return HttpResponse(rows)