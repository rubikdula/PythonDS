# # # # name = ["Rubik", "Yll", "Rion"]
# # # #
# # # # for name in name:
# # # #     print(name)
# # # #
# # # # test1 = "hello"
# # # # for test1 in test1:
# # # #     print(test1)
# # # #
# # # # test2 = "hello World"
# # # # for character in test2:
# # # #     if character.isalpha():
# # # #         print(character)
# # # #
# # # # for number in range(1, 6):
# # # #     print(number)
# # # #
# # # # numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
# # # #
# # # # maximum = numbers[0]
# # # #
# # # # for number in numbers:
# # # #     number > maximum
# # # #     maximum = number
# # # #     print(maximum)
# # # #
# # # # count = 1
# # # #
# # # # while count < 5:
# # # #     print(count)
# # # #     count += 1
# # #
# # # numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# # # target = 4
# # # for number in numbers:
# # #     print("Number:", number)
# # #     if number == target:
# # #         print("Correct")
# # #         break
# #
# # score = [50, 68, 42, 57, 78, 35, 62, 92]
# # total = 0
# # count = 0
# # for score in score:
# #     if score < 50:
# #         continue
# #         total += score
# #         count += 1
# #
# # average = total / count if count > 0 else 0
# # print("Total score:", total)
# # print("Average score:", average)
#
# while True :
#     user_input = input("Please enter a number: ")
#
#     if user_input.isnumeric():
#         number = int(user_input)
#
#         if number > 0:
#             break
#
#         print("Error")
# print("You entered a positive number")

total = 0

for number in range(1, 21):
    if number % 2 == 0:
        total += number

print("Your total sum of the numbers is", total)