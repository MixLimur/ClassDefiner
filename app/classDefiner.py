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

def getParameters(line = ""):

    getter = setter = True
    exception = False

    line = line.strip()
    if line != "":
        value = True
        for ch in line:
            if ch == '-': value = False
            elif ch == '+': value = True
            match ch:
                case 's': setter = value
                case 'g': getter = value
                case 'e': exception = value
                case _: pass
    return {
        "setter": setter,
        "getter": getter,
        "exception": exception
    }

def asDictionaryItem(line):
    line = line.strip()

    if "=" in line:
        main, default = [item.strip() for item in line.split("=")]
    else:
        main = line
        default = None

    if "[" in main and "]" in main: # have brackets
        open_bracket = main.find("[")
        close_bracket = main.find("]")
        name = main[:open_bracket]
        boundaries = main[open_bracket + 1:close_bracket]
        left_boundary, right_boundary = [item if item.strip() != '' else None for item in boundaries.split(":")]
        parameters = getParameters(main[close_bracket + 1:])
    elif (firstPar := min((main.find(i) for i in ["-", "+"] if main.find(i) >= 0), default=-1)) >= 0:  # no brackets but have parameters
        name = main[:firstPar]
        left_boundary = right_boundary = None
        parameters = getParameters(main[firstPar-1:])
    else:
        name = main
        left_boundary = right_boundary = None
        parameters = getParameters()

    fieldDictionary = {
        "boundaries":
            {
                "left": left_boundary,
                "right": right_boundary
            },
        "default": default,
        "parameters": parameters
    }
    return name, fieldDictionary

# Main format:
# field[left_boundary:right_boundary] +s +g -re = default_value, ...
# field - field name
# [left_boundary:right_boundary] (optional) - set value boundaries in setters if needed
# +s +g -e (optional) - default arguments where "-" means False (Remove), and "+" means True (Add)
# s: setters, g:getters, re: raise_exception (if user gives incorrect data, would it raise exception or no)
# = default_value (optional) - set a default value to field via class constructor

def classDefiner(fields = None):
    mainDictionary = dict()

    if fields == None:
        fields = input("Fields: (sep by comma)\n[-:-] after field without space, to choose boundaries\n")
    res = [asDictionaryItem(field) for field in fields.split(',')]
    mainDictionary.update(dict(res))
    print(mainDictionary)


    fieldsList = [field.split('=')[0].strip() for field in fields.split(',')]
    if 'self' in fieldsList:
        fieldsList.remove('self')
    else:
        fields = f"self, {fields}"
    fields = mainDictionary.keys()


    pattern = r"\[.*?\]"

    boundList = boundariesList(fieldsList)
    fieldsList = [re.sub(pattern, '', item) for item in fieldsList]

    #init
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
    # asDictionaryItem('age[0:100] = 20, name = "Ivan"')
    while True:
        classDefiner()