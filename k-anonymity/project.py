import pandas as pd

def add_or_update_k_anonymity_column(df, quasi_identifiers):
    # Группируем по квазиидентификаторам и считаем количество строк в каждой группе
    grouped = df.groupby(quasi_identifiers).size().reset_index(name='k-anonymity')

    # Объединяем исходный DataFrame с группированным, чтобы добавить или обновить столбец 'k-anonymity'
    if 'k-anonymity' in df.columns:
        # Обновляем существующий столбец 'k-anonymity'
        df = df.drop(columns=['k-anonymity']).merge(grouped, on=quasi_identifiers, how='left')
    else:
        # Добавляем новый столбец 'k-anonymity'
        df = df.merge(grouped, on=quasi_identifiers, how='left')

    return df.sort_values(by='k-anonymity')

def remove_worst_k_anonymity_rows(df, max_percent=0.05):
    """
    Функция для удаления строк с самым низким показателем k-anonymity,
    но не более max_percent от общего количества строк.
    Возваращет отсортированный по возрастанию датасет
    
    :param df: DataFrame с добавленным столбцом 'k-anonymity'
    :param max_percent: Максимальный процент строк для удаления (по умолчанию 5%)
    :return: DataFrame с удалёнными строками
    """
    # Определяем количество строк, которые нужно удалить (максимум 5%)
    n_rows_to_remove = int(len(df) * max_percent)
    
    # Сортируем DataFrame по столбцу 'k-anonymity' в порядке возрастания
    df_sorted = df.sort_values(by='k-anonymity')

    # Удаляем первые n строк с самым низким k-anonymity
    df_trimmed = df_sorted.iloc[n_rows_to_remove:]
    
    return df_trimmed

# Функция прповерки k-anonymity
def k_anonymity_checker(df, quasi_identifiers = [
        'Name', 'Passport', 'Snils', 'Symptoms', 'Doctor', 
        'Date of meeting doctor', 'Analyzes', 'Date of getting analyzes',
        'Price of analyzes', 'Card number']):
    
    # Шаг 1: Чтение .xlsx файла с прошлой лабораторной
    #df = pd.read_excel('generetion_dataset/teams.xlsx')

    # Шаг 3: Группировка по квази-идентификаторам и подсчет размеров групп
    grouped = df.groupby(quasi_identifiers).size()

    # Шаг 4: Нахождение минимального размера группы
    k_anonymity = grouped.min()

    print(f'k-anonymity: {k_anonymity}')

def find_low_k_anonymity_rows(df, quasi_identifiers, n):
    # Группируем данные по указанным столбцам и считаем частоты
    group_counts = df.groupby(quasi_identifiers).size().reset_index(name='count')
    
    # Фильтруем группы, у которых частота меньше n (k-anonymity < n)
    low_k_anonymity_groups = group_counts[group_counts['count'] < n]
    
    # Объединяем исходный DataFrame с группами, чтобы найти исходные строки
    df_with_k_anonymity = df.merge(low_k_anonymity_groups, on=quasi_identifiers, how='inner')
    
    # Убираем временный столбец 'count', возвращаем строки с низким k-anonymity
    return df_with_k_anonymity.drop(columns=['count'])

def remove_low_k_anonymity_rows(df, quasi_identifiers, n, max_remove_percentage=5):
    # Находим строки с k-anonymity меньше n
    low_k_rows = find_low_k_anonymity_rows(df, quasi_identifiers, n)
    #print("LOW_K_ROWS: ",low_k_rows)
    # Вычисляем количество строк с низким k-anonymity
    low_k_count = low_k_rows.shape[0]
    
    # Общее количество строк в DataFrame
    total_rows = df.shape[0]
    
    # Рассчитываем процент строк с низким k-anonymity
    low_k_percentage = (low_k_count / total_rows) * 100
    
    # Если процент строк меньше или равен max_remove_percentage, удаляем строки
    if low_k_percentage <= max_remove_percentage:
        df_cleaned = df.drop(low_k_rows.index)
        print(f"Удалено {low_k_count} строк ({low_k_percentage:.2f}%)")
        return df_cleaned
    else:
        print(f"Невозможно удалить строки: процент удаляемых данных ({low_k_percentage:.2f}%) превышает допустимый лимит {max_remove_percentage}%.")
        return df

# Функция для маскировки СНИЛСа, используем агрегацию
def mask_snils(snils):
    return "XXX-XXX-XXX" + " X" + str(snils)[-1:]
    #return snils[:2] + 'X-XXX-XXX XX'  # Оставляем первые 2 цифры

# Функция для маскировки номера карты, используем маскеризацию
def mask_card_number(card_number):
    # Преобразуем int в str
    card_str = str(card_number)
    
    # Оставляем первые 6 символов, остальные заменяем на "X"
    if len(card_str) > 6:
        return card_str[:1] + 'X' * (len(card_str) - 1)

def categorize_price(price):
    if price < 20000:
        return f"< 20000"
    elif 20000 <= price <= 50000:
        return f"< 50000"
    else:
        return f"< 70000"

# Функция для локального подавления и перемешивания паспортов
def suppress_and_shuffle_passport(passport):
    # Локальное подавление: оставляем только серию (первые 2 цифры)
    return passport[:2] + ' XXXX XXXXX'  # подавляем оставшуюся часть

specialty_groups = {
    'Аллерголог': 'Терапевтические врачи',
    'Пульмонолог': 'Терапевтические врачи',
    'Терапевт': 'Терапевтические врачи',
    'Ортопед': 'Хирургические врачи',
    'Стоматолог':'Хирургические врачи',
    'Уролог':'Терапевтические врачи',
    'Эндокринолог': 'Терапевтические врачи',
    'Инфекционист': 'Лабораторные специалисты',
    'Нефролог': 'Терапевтические врачи',
    'Психотерапевт':'Терапевтические врачи',
    'Диетолог': 'Терапевтические врачи',
    'Невролог': 'Терапевтические врачи',
    'Кардиолог': 'Терапевтические врачи',
    'Гепатолог': 'Терапевтические врачи',
    'Офтальмолог': 'Терапевтические врачи',
    'Трансплантолог': 'Хирургические врачи',
    'Онколог': 'Хирургические врачи',
    'ЛОР': 'Хирургические врачи',
    'Гастроэнтеролог': 'Терапевтические врачи',
    'Дерматолог': 'Терапевтические врачи',
    'Логопед': 'Терапевтические врачи',
    'Травматолог': 'Хирургические врачи',
    'Ревматолог': 'Терапевтические врачи',
    'Кинезитерапевт': 'Терапевтические врачи',
    'Вестибулолог': 'Терапевтические врачи',
    'Венеролог': 'Терапевтические врачи',
    'Бактериолог': 'Лабораторные специалисты',
    'Психиатр': 'Терапевтические врачи',
    'Хирург': 'Хирургические врачи',
    'Гигиенист': 'Лабораторные специалисты',
    'Нарколог':'Терапевтические врачи',
    'Генетик': 'Лабораторные специалисты',
    'Гематолог': 'Лабораторные специалисты',
    'Реаниматолог':'Терапевтические врачи',
    'Массажист': 'Терапевтические врачи',
    'Эпидемиолог': 'Лабораторные специалисты',
    'Андролог': 'Терапевтические врачи',
    'Нейрофизиолог': 'Терапевтические врачи',
    'Сомнолог': 'Терапевтические врачи',
    'Гомеопат': 'Терапевтические врачи',
    'Миколог': 'Лабораторные специалисты',
    'Пародонтолог': 'Терапевтические врачи',
    'Профпатолог': 'Лабораторные специалисты',
    'Вертебролог': 'Хирургические врачи',
    'Колопроктолог': 'Хирургические врачи',
    'Гинеколог': 'Хирургические врачи',
    'Эндоскопист': 'Хирургические врачи',
    'Фониатр': 'Терапевтические врачи',
    'Флеболог': 'Хирургические врачи'
}

def replace_with_symptom_count(symptom_str):
    # Разделяем строку на отдельные симптомы по запятой
    symptoms = symptom_str.split(',')
    
    # Считаем количество симптомов
    symptom_count = len(symptoms)
    if (symptom_count < 5):
        return "1 - 4"
    elif (symptom_count >= 4 and symptom_count < 8):
        return "4 - 7"
    elif (symptom_count >= 8):
        return "8 - 10"
    
def replace_with_analyze_count(analyze_str):
    # Разделяем строку на отдельные симптомы по запятой
    analyzes = analyze_str.split(',')
    
    # Считаем количество симптомов
    analyze_count = len(analyzes)
    if (analyze_count < 4):
        return "1 - 3"
    elif (analyze_count > 3):
        return "4 - 5"

def determine_gender(full_name):
    # Разделяем ФИО на части
    parts = full_name.split()
    
    if len(parts) < 3:
        return None  # Если ФИО некорректное, возвращаем None
    
    # Получаем отчество
    patronymic = parts[2]
    
    # Определяем пол по отчеству
    if patronymic.endswith('а'): # or patronymic.endswith('ович'):
        return 'Женский'
    else: #patronymic.endswith('евна') or patronymic.endswith('на') or patronymic.endswith('овна'):
        return 'Мужской'
    
       # return None  # Если не удалось определить пол

def aggregate_time(timestamp):
    #return timestamp[:7]
    return timestamp[:5] + "XX" + "-" + "X" * 5 + ":" + "XX" + "+" + "XX" + ":" + "XX"

def calculate_low_k_anonymity_percentage(df, quasi_identifiers, n):
    # Находим строки с k-anonymity меньше n
    low_k_rows = find_low_k_anonymity_rows(df, quasi_identifiers, n)
    
    # Вычисляем количество строк с низким k-anonymity
    low_k_count = low_k_rows.shape[0]
    
    # Общее количество строк в DataFrame
    total_rows = df.shape[0]
    
    # Рассчитываем процентное соотношение
    low_k_percentage = (low_k_count / total_rows) * 100
    
    return low_k_count, low_k_percentage

def main_func(df, selected_quasi_identifiers, exit_file):
    #df = pd.read_csv('teams.csv')
    
    df['Name'] = df['Name'].apply(determine_gender)
    df['Passport'] = 'Паспорт РФ'
    df['Snils'] = df['Snils'].apply(mask_snils)
    df['Symptoms'] = df['Symptoms'].apply(replace_with_symptom_count)
    df['Doctor'] = df['Doctor'].map(specialty_groups)
    df['Date of meeting doctor'] = df['Date of meeting doctor'].apply(aggregate_time)
    df['Analyzes'] = df['Analyzes'].apply(replace_with_analyze_count)
    df['Price of analyzes'] = df['Price of analyzes'].apply(categorize_price)
    df['Date of getting analyzes'] = df['Date of getting analyzes'].apply(aggregate_time)
    df['Card number'] = df['Card number'].apply(mask_card_number)



    #print(low_k_rows)
    
    df = add_or_update_k_anonymity_column(df, selected_quasi_identifiers)
    df = remove_worst_k_anonymity_rows(df, max_percent=0.05)
    
    #df =  add_or_update_k_anonymity_column(df)
    #print(df.head())
    
    df.to_csv(f'{exit_file}.csv', index=False)
    
    #k_anonymity_checker(df, quasi_identifiers=['Name', 'Snils', 'Passport', 'Date of meeting doctor', 'Date of getting analyzes', 'Card number'])
    """
    low_k_rows = find_low_k_anonymity_rows(df, [], 10)
    
    
    #print(low_k_rows)
    low_k = 10
    
    low_k_count, low_k_percentage = calculate_low_k_anonymity_percentage(df, 
    ['Name', 'Passport','Snils', 'Symptoms', 'Doctor',
                                                'Date of meeting doctor',  'Analyzes', 
                                                 'Date of getting analyzes','Price of analyzes', 
                                                'Card number'], low_k)
    
    print(f"Количество строк с k-anonymity меньше {low_k}: {low_k_count}")
    print(f"Процентное соотношение: {low_k_percentage:.2f}%")
    """
    head_df = df.head(5)
    
    k_anonymity_values = df['k-anonymity'].values
    first_k_anonymity_value = k_anonymity_values[0]
    #print("k-anonymity:",first_k_anonymity_value)
    
    min_k_anonymity = df['k-anonymity'].min()

    # Подсчитываем количество строк с минимальным значением 'k-anonymity'
    min_k_anonymity_count = (df['k-anonymity'] == min_k_anonymity).sum()
    print(f"Значение k-anonymity: {min_k_anonymity}")
    print(f"Количество строк с минимальным k-anonymity: {min_k_anonymity_count}")
    
    total_rows = len(df)

    # Считаем процент строк с минимальным 'k-anonymity'
    percentage_min_k_anonymity = (min_k_anonymity_count / total_rows) * 100
    print(f"Процент строк с минимальным k-anonymity: {percentage_min_k_anonymity:.2f}%")
    #print("Топ плохих k-anonymity: ", head_df)

#Для ввода
def select_quasi_identifiers():
    quasi_identifiers_options = ['Name', 'Passport', 'Snils', 'Date of meeting doctor', 
                                 'Analyzes', 'Date of getting analyzes', 'Price of analyzes', 
                                 'Card number']
    
    while True:
        print("\nВыберите квази идентификаторы для анализа k-anonymity:")
        print("Введите номера через запятую, пробел или введите 'все', чтобы выбрать все сразу.")
        print("Доступные столбцы:")
        
        # Печатаем доступные столбцы с номерами
        for i, column in enumerate(quasi_identifiers_options, 1):
            print(f"{i}. {column}")
        
        # Получаем от пользователя ввод
        user_input = input("\nВаш выбор (например, 1, 2, 3 или 'все'): ").strip().lower()
        
        try:
            if user_input == 'все' or user_input == 'all':  # Обработка выбора всех квази-идентификаторов
                print("\nВы выбрали все квази-идентификаторы.")
                return quasi_identifiers_options
            
            # Преобразуем ввод в список чисел, удаляя лишние пробелы
            selected_numbers = [int(x.strip()) for x in user_input.replace(',', ' ').split() if x.strip().isdigit()]
            
            # Проверяем, что выбранные номера находятся в допустимом диапазоне
            if not selected_numbers:
                raise ValueError("Пожалуйста, введите хотя бы один номер или 'все'.")
            
            for num in selected_numbers:
                if num < 1 or num > len(quasi_identifiers_options):
                    raise ValueError(f"Неверный номер: {num}. Пожалуйста, выберите из предложенного диапазона.")

            # Преобразуем выбранные номера в названия столбцов
            selected_columns = [quasi_identifiers_options[i-1] for i in selected_numbers]

            print(f"\nВы выбрали: {', '.join(selected_columns)}")
            return selected_columns
        
        except ValueError as e:
            print(f"\nОшибка ввода: {e}. Попробуйте снова.\n")

        except Exception as e:
            print(f"\nПроизошла непредвиденная ошибка: {e}. Попробуйте снова.\n")


if __name__ == "__main__":
    
   # Запрос имени файла у пользователя
    #exit_file = input("Введите имя выходного файла: ")
    file_name = input("Введите имя файла (с расширением, например, 'data.xlsx'): ")
    exit_file = "anonymous_dataset"
    try:
        # Загружаем файл в DataFrame
        if file_name.endswith('.xlsx'):
            df = pd.read_excel(file_name)
        elif file_name.endswith('.csv'):
            df = pd.read_csv(file_name)
        else:
            raise ValueError("Поддерживаются только файлы .xlsx и .csv")

        print("Файл успешно загружен!")
        selected_quasi_identifiers = select_quasi_identifiers()
        print(f"Квази идентификаторы для анализа: {selected_quasi_identifiers}")
        main_func(df, selected_quasi_identifiers, exit_file)
        #print(df.head())  # Печать первых 5 строк DataFrame

    except FileNotFoundError:
        print("Ошибка: Файл не найден. Проверьте имя файла и путь к нему.")
    except ValueError as ve:
        print(ve)
    except Exception as e:
        print("Произошла ошибка:", e)

