import re
def enterNumber(text = "Enter value: "):
    while True:
        try:
            number = input(text)
            return int(number)
        except ValueError:
            print("Enter a valid value!")

#base case (for protected fields)

def printSetter(field, *, l = None, r = None):
    setter_start = (
        f"@{field}.setter\n"
        f"def set_{field}(self, new_{field}):\n"
    )
    if l == r == None:
        logic = ""
    elif l == None: # right boundaries
        logic = (
            f"\tif new_{field} > {r}:\n"
            f"\t\tself._{field} = {r}\n"
            f"\telse:\n\t"
        )
    elif r == None: # left boundaries
        logic = (
            f"\tif new_{field} < {l}:\n"
            f"\t\tself._{field} = {l}\n"
            f"\telse:\n\t"
        )
    else: # left and right boundaries
        logic = (
            f"\tif new_{field} > {r}:\n"
            f"\t\tself._{field} = {r}\n"
            f"\telif new_{field} < {l}\n:"
            f"\t\tself._{field} = {l}\n"
            f"\telse:\n\t"
        )

    print(setter_start + logic + f"\tself._{field} = new_{field}\n")

def boundariesList(fieldsList):
    resultList = list()
    for field in fieldsList:
        if '[' not in field:
            resultList.append([None,None])
        else:
            bracket = field.find("[")
            str = field[bracket+1:-1]
            boundaries = str.split(":")
            boundaries = [None if item == '-' else item for item in boundaries]
            resultList.append(boundaries)
    # print(resultList)
    return resultList

def classDefiner(fields = None):
    if fields == None:
        fields = input("Fields: (sep by comma)\n[-:-] after field without space, to choose boundaries\n")
    fieldsList = [field.split('=')[0].strip() for field in fields.split(',')]
    if 'self' in fieldsList:
        fieldsList.remove('self')
    else:
        fields = f"self, {fields}"

    pattern = r"\[.*?\]"

    boundList = boundariesList(fieldsList)
    fieldsList = [re.sub(pattern, '', item) for item in fieldsList]

    #init
    fields = re.sub(pattern, '', fields)
    print(f"def __init__({fields}):")
    for field in fieldsList:
        print(f"\tself.{field} = {field}")
    print()
    #getters & setters
    for i, field in enumerate(fieldsList):
        print(f"@property\ndef get_{field}(self):\n\treturn self._{field}\n")
        printSetter(field, l = boundList[i][0], r = boundList[i][1])
        # print(f"@{field}.setter\ndef set_{field}(self, new_{field}):\n\tself._{field} = new_{field}\n")

    # printSetter(fieldsList[0], r = None)

# classDefiner("self, name, description, duration, difficulty = 0")

if __name__ == '__main__':
    while True:
        classDefiner()