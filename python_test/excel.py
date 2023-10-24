import pandas as pd

# Nacita subor 
workbook = pd.read_excel('example.xls')

# workbook['column']  vrati riadky daneho stlpca
print(workbook['First Name'])

# workbook['column'].iloc[n] vrati n-ty riadok daneho stlpca (riadok zacina od 0)
print(workbook['First Name'].iloc[2])

