from .bruh import Trainer


def get_doneness(file_path, t: Trainer):

    result = t.predict(file_path)
    
    print(result)
    index = 0
    maximum = -1

    for i in range(len(result[0])):
        result[0][i] = "{:.12f}".format(result[0][i])
        print(result[0][i])
        if result[0][i] > maximum:
            index = i
            maximum = result[0][i]

    if index == 0:
        return "Medium"
    elif index == 1:
        return "Rare"
    elif index == 2:
        return "Well done"
