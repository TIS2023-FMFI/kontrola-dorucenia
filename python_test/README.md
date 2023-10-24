Porovnávanie knižníc na manipuláciu s excel dokumentom a skúšanie backend-u pomocou Python Flask a Django.\
Python verzia 3.11.6

Testovanie Excel dokumentu  
Požadované knižnice : pandas, xlrd \
Inštalácia knižnice : 
```
pip install <library> 
```
alebo 

```
pip3 install <library>
```


Základne príkazy :

Načíta xls dokument 
```
workbook = pandas.read_excel('file.xls')
```
Načíta hárok v xls dokumente 
```
worksheet = pandas.read_excel('file.xlsx', sheet_name = 'Sheet_name')
```
Vráti riadky daného stĺpca 
```
workbook['column']
```
Vráti n-ty riadok daného stĺpca 
```
workbook['column'].iloc[n]
```

