import datetime

example1 = datetime.datetime.now()
print("Year: ", example1.year)
print("Month: ", example1.month)
print("Day: ", example1.day)
print("Hour: ", example1.hour)
print("Minute: ", example1.minute)
print("Second: ", example1.second)
print("Micro Second: ", example1.microsecond)

future = example1 + datetime.timedelta(days=100)
past = example1 - datetime.timedelta(days=100)
print(future)
print(past)

specificDT = datetime.datetime(2023, 9, 1, 4, 0, 0)

with open("formattedDates.txt", 'w') as f:
    f.write(specificDT.strftime("%Y-%m-%d"))