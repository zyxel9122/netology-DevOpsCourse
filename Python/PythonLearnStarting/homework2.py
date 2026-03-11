HELP = """
help - напечатать справку по программе.
add - добавить задачу в список (название задачи запрашиваем у пользователя).
show - напечатать все добавленные задачи.
exit - выход из программы."""

tasks = {}  # словарь: дата -> список задач

run = True

while run:
    command = input("Введите команду: ")
    if command == "help":
        print(HELP)
    elif command == "show":
        if tasks:
            for date, task_list in tasks.items():
                print(f"{date}: {', '.join(task_list)}")
        else:
            print("Задач пока нет.")
    elif command == "add":
        date = input("Введите дату: ")
        task = input("Введите задачу: ")
        # Если даты нет, создаём новый список и добавляем задачу
        tasks.setdefault(date, []).append(task)
        print("Задача добавлена")
    elif command == "add to date":
        if not tasks:
            print("Нет ни одной даты. Сначала добавьте задачу через 'add'.")
            continue
        print("Доступные даты:", ", ".join(tasks.keys()))
        date = input("Введите дату: ")
        if date in tasks:
            task = input("Введите задачу: ")
            tasks[date].append(task)
            print(f"Задача на {date} добавлена!")
        else:
            print("Такой даты нет.")
    elif command == "exit":
        print("До свидания!")
        break
    else:
        print("Неизвестная команда")

