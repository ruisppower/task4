import pandas as pd
import os
import matplotlib.pyplot as plt

# читаем Excel
df = pd.read_excel(r'C:\Users\Пользователь\Desktop\Книга1.xlsx',
                   engine='openpyxl')

# сохраняем в CSV (правильный формат!)
df.to_csv(r'C:\Users\Пользователь\Desktop\Книга1.csv',
          index=False,
          encoding='utf-8')
df_csv = pd.read_csv(r'C:\Users\Пользователь\Desktop\Книга1.csv',
                     encoding='utf-8')

# Сохраните в переменную na_number серию, в которой для каждой колонки будет указано, сколько пропущенных значений она содержит.
na_number = (df_csv.isna()
             .sum())
#print(na_number)

# Посмотрели типы данных столбцов
df_types = df_csv.dtypes
#print(df_types)

df_csv["age"] = (df_csv["age"]
                 .astype(float))
#print(df_csv.dtypes)

# Удаляем столбцы sex и age
df_delete = df_csv.drop(['sex', 'age'],
                        axis=1)
#print(df_delete)

# Убираем дубликаты по колонке client_id, оставляем только первую строку для каждого значения
df_1 = (df_delete
        .drop_duplicates(subset='client_id',
                         keep='first'))
#print(df_1.head())


# Здесь треним Python
# В списке numbers содержатся числа.
# Добавьте через цикл в список positive_numbers положительные числа из numbers.
# Если вам попался 0, то нужно прекратить этот цикл.
# Например, numbers = [1, -2, 3, 0, -3, 2].
# Тогда positive_numbers должен быть: positive_numbers = [1, 3]

numbers = [1, -2, 4, 10, 5, -3, 16, 0, -8, 9, 11]
postive_numbers = []
for i in numbers:
    if i != 0:
        if i > 0:
            postive_numbers.append(i)
#print(postive_numbers)

# Продолжаю анализ данных по поездкам на такси из Перу
taxi = pd.read_csv(r'C:\Users\Пользователь\Desktop\Аналитик данных 1\[SW.BAND] 2 МОДУЛЬ PYTHON\[SW.BAND] Ноутбуки и датасеты\3_taxi_peru.csv',
                   sep=';',
                   encoding='windows-1251')

taxi['start_at'] = pd.to_datetime(taxi['start_at'])
taxi['end_at'] = pd.to_datetime(taxi['end_at'])
taxi['arrived_at'] = pd.to_datetime(taxi['arrived_at'])
#print(taxi['start_at'].head())

taxi['month'] = taxi['start_at'].dt.month
taxi['weekday'] = taxi['start_at'].dt.day_name()
taxi['year_month'] = taxi['start_at'].dt.to_period('M')

filtered_taxi = taxi[taxi['start_type'].isin(['asap', 'reserved'])]

wait_time = taxi["arrived_at"] - taxi["start_at"]
taxi['wait_time_minutes'] = (wait_time
                             .dt
                             .total_seconds() / 60)
#print(wait_time_minutes)

being_late = (taxi[taxi['start_type'] == 'reserved']
              .copy())
being_late['wait_time_minutes'] = (
    (being_late['arrived_at'] - being_late['start_at'])
    .dt.total_seconds() / 60)

late_drivers = being_late[being_late['wait_time_minutes'] > 0]

#print(late_drivers[['driver_id', 'start_at', 'arrived_at', 'wait_time_minutes']].head(10))

late_counts = (late_drivers.groupby('driver_id')
               .size())
max_late_driver_id = late_counts.idxmax()
#print(max_late_driver_id)


       # Строим график числа заказов по месяцам

# Считаем количество заказов по месяцам
orders_per_month = taxi.groupby('month').size()

# Строим график
plt.figure(figsize=(8,5))
orders_per_month.plot(kind='bar', color='skyblue')
plt.title('Число заказов по месяцам')
plt.xlabel('Месяц')
plt.ylabel('Количество заказов')
plt.xticks(rotation=0)  # чтобы подписи месяцев были горизонтально
plt.show()


       # Теперь строим график по дням недели

orders_per_weekday = taxi.groupby('weekday').size()

# Строим график
plt.figure(figsize=(8,5))
orders_per_weekday.plot(kind='bar', color='skyblue')
plt.title('Число заказов по дням недели')
plt.xlabel('День недели')
plt.ylabel('Количество заказов')
plt.xticks(rotation=0)  # чтобы подписи дней недели были горизонтально
plt.show()

       # Теперь строим график MAU (Monthly Active Users)

# Считаем количество уникальных пользователей по месяцам
mau = taxi.groupby('year_month')['user_id'].nunique()

# Строим график
plt.figure(figsize=(10,5))
mau.plot(kind='line', marker='o', color='teal')
plt.title('Monthly Active Users (MAU)')
plt.xlabel('Месяц')
plt.ylabel('Количество уникальных пользователей')
plt.xticks(rotation=45)
plt.grid(True)
plt.show()

























