from mimesis.builtins import RussiaSpecProvider
from faker import Faker
import pandas as pd
import random
from datetime import datetime, timedelta, time
import pytz

# Functions that are being used in creating dataset

# Function that generates time, when person come to doctor
def generate_datetime_first_meet():
    start_date=datetime(2020, 1, 1)
    end_date=datetime(2024, 12, 30)
    working_hours=(8, 18)
    timezone='Europe/Moscow'
    
    delta_days = (end_date - start_date).days
    random_days = random.randint(0, delta_days)
    random_date = start_date + timedelta(days=random_days)
    
    start_hour, end_hour = working_hours
    random_time = time(random.randint(start_hour, end_hour - 1), random.randint(0, 59))

    while random_date.weekday() >= 5:  # 5 и 6 — it's saturday and sunday
        random_days = random.randint(0, delta_days)
        random_date = start_date + timedelta(days=random_days)

    random_datetime = datetime.combine(random_date, random_time)

    tz = pytz.timezone(timezone)
    random_datetime = tz.localize(random_datetime)

    return random_datetime.isoformat()

# Function that generates time, when person come for analyses
def generate_datetime_second_meet(initial_datetime_str):
    working_hours=(8, 18)
    timezone='Europe/Moscow'
    max_hours_delta = 72
    
    # Преобразуем строку обратно в объект datetime
    initial_datetime = datetime.fromisoformat(initial_datetime_str)  # tzinfo уже установлено
    
    while True:
        # Генерация случайного числа часов в диапазоне от 24 до 72
        random_hours = random.randint(24, 72)
        new_datetime = initial_datetime + timedelta(hours=random_hours)

        # Приведение времени к рабочим часам
        start_hour, end_hour = working_hours

        # Если сгенерированное время выходит за пределы рабочего времени, то корректируем его
        if new_datetime.hour < start_hour:
            new_datetime = new_datetime.replace(hour=start_hour, minute=0, second=0)
        elif new_datetime.hour >= end_hour:
            new_datetime = new_datetime + timedelta(days=1)
            new_datetime = new_datetime.replace(hour=start_hour, minute=0, second=0)

        # Проверка, чтобы дата попадала на рабочий день
        while new_datetime.weekday() >= 5:  # Если это суббота (5) или воскресенье (6)
            new_datetime += timedelta(days=1)
            new_datetime = new_datetime.replace(hour=start_hour, minute=0, second=0)

        # Проверка, что время между встречами не превышает 72 часов
        delta_hours = (new_datetime - initial_datetime).total_seconds() / 3600
        if delta_hours <= max_hours_delta:
            break

    return new_datetime.isoformat()

# Function that generates list of passports using mimesis
def generate_passport(amount):
    # Создаем паспорт с помощью библиотеки mimesis
    ru_spec = RussiaSpecProvider() 
    passport = ru_spec.series_and_number()
    set_of_passports = set()
    
    while len(set_of_passports) < amount: # создание необходимого кол-ва паспортов
        passport = ru_spec.series_and_number()
        set_of_passports.add(passport)
        
    list_of_passports = list(set_of_passports)
    return list_of_passports

# Function that generates list of names using faker
def generate_names(amount):
    # Создаем имена с помощью библиотеки mimesis
    fake = Faker("ru_RU")
    fullnames = set()
    
    while len(fullnames) < amount: # создание необходимого кол-ва имен
        name = fake.name()
        fullnames.add(name)
        
    fullnames = list(fullnames)
    
    #data = pd.DataFrame({'Имена': fullnames})

    #data.to_csv('names.csv')
    
    return fullnames

# Function that generates one card number
def generate_card_number(bin_code):
    unique_part = ''.join([str(random.randint(0, 9)) for _ in range(9)]) # Сгенерировать 9 случайных цифр для уникальной части номера карты
    
    partial_card_number = bin_code + unique_part # Объединяем БИН и уникальную часть номера карты
    
    last_digit = random.randint(0,9) # Генерируем случайную последнюю цифру
    
    full_card_number = int(partial_card_number + str(last_digit)) # Полный номер карты
    return full_card_number

# Function that generates list of card numbers, including probabilities for banks
def generate_payment_data(amount, bank_weights=None, payment_system_weights=None):
    
    # Определение данных по банкам и платёжным системам
    bank_data = {
        'Сбербанк': {
            'Visa': '427612',  
            'MasterCard': '546915',  
            'Mir': '220035'  
        },
        'Альфа-Банк': {
            'Visa': '412345',  
            'MasterCard': '532156',  
            'Mir': '220054'  
        },
        'Газпромбанк': {
            'Visa': '410012',  
            'MasterCard': '530114',  
            'Mir': '220011'  
        },
        'Тинькофф': {
            'Visa': '437772',  
            'MasterCard': '521324',  
            'Mir': '220071'  
        },
        'ВТБ': {
            'Visa': '421345',  
            'MasterCard': '548712',  
            'Mir': '220041'  
        }
    }

    # Если не заданы вероятности, по умолчанию выбираем все равновероятно
    if bank_weights is None:
        bank_weights = [1] * len(bank_data)
    
    # Задаем вероятности для платёжных систем (если не заданы)
    if payment_system_weights is None:
        payment_system_weights = [1, 1, 1]  # По умолчанию Visa, MasterCard, Mir равновероятны

    card_number_list = list()
    
    for _ in range(amount):
        # Случайный выбор банка с учётом вероятностей
        bank = random.choices(list(bank_data.keys()), weights=bank_weights, k=1)[0]
        
        # Случайный выбор платежной системы с учётом вероятностей
        payment_system = random.choices(list(bank_data[bank].keys()), weights=payment_system_weights, k=1)[0]
        
        # Получаем БИН/IIN для банка и платежной системы
        bin_code = bank_data[bank][payment_system]
        
        # Генерируем номер карты
        card_number = generate_card_number(bin_code)
        
        card_number_list.append(card_number)

    return card_number_list

# Function that generates one snils
def generate_snils():
    
    snils_format = '{Num1}-{Num2}-{Num3} {Num4}'
    
    # Generate random nums for snils
    argz = {
        'Num1': str(random.randint(0, 999)).zfill(3), 
        'Num2': str(random.randint(0, 999)).zfill(3), 
        'Num3': str(random.randint(0, 999)).zfill(3), 
        'Num4': str(random.randint(0, 99)).zfill(2)    
    }
    
    return snils_format.format(**argz)

def select_symptoms(symptom_dict, n, doctors, doctor):
    matched_symptoms = [symptom for symptom, doctors in symptom_dict.items() if doctor in doctors]

    if len(matched_symptoms) < n:
        return matched_symptoms  # Возвращаем врача и все найденные симптомы
    
    selected_symptoms = random.sample(matched_symptoms, n)
    
    return selected_symptoms

def generate_analyzes(dict, n):
    result = {}
    
    while len(result) != n:
        # Randomly pick amount of analyses from 1 to 5
        num_tests = random.randint(1, 5)
        
        # Randomly pick analyses from dictionary
        selected_tests = random.sample(list(dict.items()), num_tests)
        
        # Create key from chosen analyses
        test_names = ', '.join(test for test, _ in selected_tests)
        
        # Calculate total cost
        total_cost = sum(price for _, price in selected_tests)
        
        # Fill final dictionary
        result[test_names] = total_cost
        
    return result

# Functions that are used to make result file looke better

def format_symptoms(symptom_str):
    # Удаляем квадратные скобки и лишние пробелы, а затем разделяем по запятой
    return symptom_str.strip("[]").replace("'", "").replace('"', '').strip()

def format_number(number):
    number_str = str(number)  # Преобразуем число в строку
    return f"{number_str[:3]}-{number_str[3:6]}-{number_str[6:9]} {number_str[9:]}"  # Форматируем строку

def format_passport(number):
    # Убираем пробелы из строки и преобразуем число в строку
    number_str = str(number).replace(' ', '')
    
    # Проверяем, что длина строки соответствует нужному формату
    if len(number_str) == 10:  # Учитываем длину без пробелов (XX XX XXXXXX)
        return f"{number_str[:4]} {number_str[4:]}"  # Форматируем в XXXX XXXXXX
    else:
        return number

# Main function that generates final file
def generate_dataset(amount, bank_weights=None, payment_system_weights=None):
    # Code 
    df = pd.read_csv('generetion_dataset/csv_files/doctors_and_symptoms.csv', delimiter=';')
    docs = df['docs'].tolist()
    symps = df['symps'].tolist()

    dict = {}
    for i in range(len(symps)):
        dict[symps[i]] = docs[i].split(", ")

    docs = set(doctor for docs in dict.values() for doctor in docs)
    
    card_numbers = generate_payment_data(amount, bank_weights, payment_system_weights)
    
    fullnames = generate_names(amount)
    arrayofpassport = generate_passport(amount)

    doctors = list(docs)

    list_of_doctors = list()
    list_of_analyzes = list()
    list_of_symptoms = list()
    list_of_prices = list()
    list_of_datetime_first_meet = list()
    list_of_datetime_second_meet = list()
    
    df = pd.read_csv('generetion_dataset/csv_files/analyzes_and_cost.csv', delimiter=',')
    analyzes = df['Анализы'].tolist()
    cost = df['Стоимость'].tolist()

    dict_2 = {}
    for i in range(len(symps)):
        dict_2[analyzes[i]] = cost[i]
    
    dict_of_analyzes_and_costs = generate_analyzes(dict_2, amount)
    list_of_analyzes = list(dict_of_analyzes_and_costs.keys())
    list_of_prices = list(dict_of_analyzes_and_costs.values())
    
    used_snils = []
    arrayofsnils = []
    
    for i in range(amount):
        snils = generate_snils()
        while snils in used_snils:
            snils = generate_snils()
        used_snils.append(snils)
        
        arrayofsnils.append(snils)
        
        list_of_doctors.append(doctors[random.randint(0, 49)])
        n = random.randint(1, 10)
        selected_symptoms = select_symptoms(dict, n, docs, list_of_doctors[i])
               
        list_of_symptoms.append(selected_symptoms)
        list_of_datetime_first_meet.append(generate_datetime_first_meet())
        list_of_datetime_second_meet.append(generate_datetime_second_meet(list_of_datetime_first_meet[i]))
        
    data = pd.DataFrame({'Name': fullnames,
                        'Passport': arrayofpassport,
                        'Snils': arrayofsnils,
                        'Symptoms':list_of_symptoms,
                        'Doctor':list_of_doctors,
                        'Date of meeting doctor': list_of_datetime_first_meet,
                        'Analyzes': list_of_analyzes,
                        'Date of getting analyzes': list_of_datetime_second_meet,
                        'Price of analyzes': list_of_prices,
                        'Card number': card_numbers
                        })
    
    data.to_csv('./teams.csv')
    
    df = pd.read_csv('./teams.csv')

    # Функция для преобразования строки


    # Применяем функцию к столбцу 'symptoms'
    df['Symptoms'] = df['Symptoms'].apply(format_symptoms)
    #df['Snils'] = df['Snils'].apply(format_number)
    df['Passport'] = df['Passport'].apply(format_passport)
    
    # Удаление первого столбца (по индексу 0)
    df = df.drop(df.columns[0], axis=1)
    # Если нужно, сохранить изменения в новый Excel файл
    df.to_csv('./teams.csv', index=False)


if __name__ == "__main__":

    bank_weights = list() # Вероятности для банков
    payment_system_weights = list() # Вероятности для платёжных систем
    
    # Const lists for probabilities
    bank_weights = [0.5, 0.2, 0.1, 0.1, 0.1]  
    payment_system_weights = [0.7, 0.2, 0.1] 
    """
    print("Введите вероятности для банков соответственно: ")
    print("Сбербанк, Альфа-Банк, Газпромбанк, Т-Банк, ВТБ")
    print("чтобы в сумме получилась 1")
    
    while len(bank_weights) != 5:
        try:
            a = float(input())
            bank_weights.append(a)
            print("Сейчас сумма равна:", sum(bank_weights))
            if len(bank_weights) == 5 and sum(bank_weights) != 1:
                print("Сумма не равна единице")
                print("Попробуйте заново")
                bank_weights.clear()
                continue
        except ValueError:
                print("Вам нужно ввести цифру.")
        
    
    print("Введите вероятности для платежных систем соответственно: ")
    print("Visa, Mastercard, MIR")
    print("чтобы в сумме получилась 1")
    
    while len(payment_system_weights) != 3:
        try:
            a = float(input())
            payment_system_weights.append(a)
            print("Сейчас сумма равна:", sum(payment_system_weights))
            if len(payment_system_weights) == 3 and sum(payment_system_weights) != 1:
                print("Сумма не равна единице")
                print("Попробуйте заново")
                payment_system_weights.clear()
                continue
        except ValueError:
                print("Вам нужно ввести цифру.")
   """
    print("Теперь введите желаемое количество строк в датасете")
    try:
        amount = int(input())
    except ValueError:
        print("Вам нужно ввести цифру.")
        
    print("Спасибо, ожидайте!")
    # Main function
    generate_dataset(amount, bank_weights, payment_system_weights) 
    
    print("Генерация завершена!")