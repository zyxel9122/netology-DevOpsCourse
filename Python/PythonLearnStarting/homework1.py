#Задание1
""""
today_date = input("Введите дату:")
task_enter = input("Введите задачу:")
print(today_date)
print(task_enter)
"""
#Задание2
""""
count = 0
array_date: str = []
array_task_enter: str = []
while count < 3: 
    user_input = input("Введите дату:")
    array_date.append(user_input)
    user_input = input("Введите задачу:")
    array_task_enter.append(user_input) 
    count += 1
count_print = 0
while count_print < 3: 
    print(array_date[count_print])
    print(array_date[count_print])
    count_print += 1
"""
#Задание2 из нейронки
""""
dates = []
tasks = []
for _ in range(3):
    dates.append(input("Введите дату: "))
    tasks.append(input("Введите задачу: "))

for date, task in zip(dates, tasks):
    print(date)
    print(task)
"""
#Задание3 Словарь
""""
n = int(input("Сколько задач добавить? "))
my_task_dict = {}
for i in range(n):
    key = input(f"Введите {i+1} дату : ")
    value = input(f"Введите задачу на '{key}': ")
    my_task_dict[key] = value
print(my_task_dict)
"""
