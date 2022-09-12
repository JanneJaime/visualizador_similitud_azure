import xlrd
import os
path = os.path.dirname(__file__)+'\\data\\'

"""
    - Leer excel de palabras permitidas
"""
def words():
    wb = xlrd.open_workbook(path+'palabras_permitidas.xlsx')
    sheet = wb.sheet_by_name('Hoja1')
    topics = []
    for i in range(1,sheet.nrows):
        topics.append(sheet.cell_value(i,1))
    
    return topics