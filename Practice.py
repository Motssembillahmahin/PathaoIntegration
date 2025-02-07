import pandas as pd
import numpy as np
# file = pd.read_csv('parcels_2025-02-06.csv')
file2 = pd.read_csv('FileterFile.csv')

drop_columns = ['Shipping Street', 'Billing Company', 'Shipping Street']


file2.drop(columns=drop_columns, inplace = True)
file2.to_csv('FileterFile.csv', index = False)
# print(file2['Discount Code'])
# print(file2.columns)
# # print(file2['Shipping'])
#
# print(file2.tail(5))