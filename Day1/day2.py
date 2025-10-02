# # # words = ("spam", "eggs", "ham")
# # # print(words[0])
# # #
# # # # empty_tuple = ()
# #
# # person = ("Rubik", 15, "Finland")
# #
# # name, age, birthday = person
# # print(name, age, birthday)
#
# # my_dictionary = {
# #     "Key1": "value1",
# #     "Key2": "value2",
# #     "Key3": "value3",
# # }
#
# contact_info = {
#     "Rubik": "0442323232",
#     "Ylli": "38923829",
#     "Diell": ""
# }
#
# # rubik_phone = contact_info["Rubik"]
# #
# # print(rubik_phone)
# #
# # contact_info["Ylli"] = "049494949"
# #
# # print(contact_info)
#
# contact_info["Diell"] = "01201201"
#
# print(contact_info)
#
# del contact_info["Rubik"]
#
# print(contact_info)
#
# keys = contact_info.keys()
# print(keys)
#
# items = contact_info.items()
# print(items)

# personal_info = {
#     "Rubik" : ("91029102910291", "15", "Gjakove"),
#     "Yll": ("12810280182", "17", "Vranjevc"),
#     "Diell": ("1290-1902", "16", "Prishtine")
# }
#
# print(personal_info)
#
# del personal_info["Rubik"]
# print(personal_info)

contact_info = {
    "Rubik": {
        "phone_number": "+55 55 55 55",
        "email": "rubik@halla.com",
        "home": "Prishtina",
        "Birthday": "23/02/2022",
    },

    "Yll": {
        "phone_number": "+55 55 55 55",
        "email": "rubik@halla.com",
        "home": "Prishtina",
        "Birthday": "23/02/2022",
    },

    "Diell": {
        "phone_number": "+55 55 55 55",
        "email": "rubik@halla.com",
        "home": "Prishtina",
        "Birthday": "23/02/2022",
    }
}

grades = {
    ("Rubik", "Math"): 5,
    ("Yll", "Math"): 5,
    ("Diell", "Math"): 5,
}

rubik_math = grades[("Rubik", "Math")]
print("Rubik's math grade:", rubik_math)
# print(contact_info)
#
# rubik = contact_info["Rubik"]
# print(rubik)