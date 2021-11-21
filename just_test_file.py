import json
# print(type(b'\r\n'))
# print(b'\n' in b'\r\n')

#
# a = {}
# for p in [11, 12]:
#     a[p] = 1
# print(a)

info = {12 : True,
        13 : False,
        "Temperature sensor" : 50
        }
print(json.dumps(info))

print(json.dumps("Temperature sensor"))

