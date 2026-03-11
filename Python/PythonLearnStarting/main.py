#strings = ["Hello", "world"]
numbers = [1, 2, 3, 4, 5]
#data = ["hello", 1]
sum = 0
for i in numbers:
    sum += i
    print(i)

#my_age = input("Enter your age:")
#print("Your age is:" + my_age)
print(True)
""""
print(strings)
print(numbers)
print(data)

summa = numbers + data
print(summa)

numbers.append(6)
print(numbers)

first = strings[0]
second = strings[1]
print(first)
print(second)

strings_length = len(strings)
print(strings_length)

s = sum(numbers)
print(s)
"""

# cat: кошка
# bat: летучая мышь

# ключ : значение

dictionary = {
  "cat": "кошка",
  "bat": "летучая мышь"
}

# print(dictionary)
# cat = dictionary["cat"]
# print(cat)

countries = {
  "Африка": ["Египет", "Конго", "ЮАР"],
  "Азия": ["Китай", "Таиланд", "Индонезия"]
}

africa = countries["Африка"]
print(africa)

africa_key = "Африка"
print(countries[africa_key])

countries["Европа"] = ["Австрия", "Испания", "Италия"]
print(countries)
print(countries["Европа"])
# countries[0] = "Hello"
# print(countries)
africa.append("Эфиопия")
print(africa)
print(countries)
print(len(countries["Африка"]))