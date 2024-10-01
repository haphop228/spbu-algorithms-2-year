import pandas as pd

# Шаг 1: Чтение .xlsx файла
df = pd.read_excel('Generetion DataSet/teams.xlsx')

# Шаг 2: Выбор квази-идентификаторов
quasi_identifiers = ['Name', 'Passport', 'Snils', 'Symptoms', 'Doctor', 'Date of meeting doctor', 'Analyzes', 'Date of getting analyzes', 'Price of analyzes', 'Card number']  # Здесь нужно указать свои квази-идентификаторы

# Шаг 3: Группировка по квази-идентификаторам и подсчет размеров групп
grouped = df.groupby(quasi_identifiers).size()

# Шаг 4: Нахождение минимального размера группы
k_anonymity = grouped.min()

print(f'k-anonymity: {k_anonymity}')
