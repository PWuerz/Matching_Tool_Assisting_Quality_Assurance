import json
import random

with open("data/BPPFehler2.json", "r") as file:
    json_data = file.read()

data_variable = json.loads(json_data)
data_json_tasks = data_variable["tasks"]


# Einlesen aller Tasks
def readAllTasks():

    ListReturnAllTasks = []
    ListReturnTask = []

    for task in data_json_tasks:
        #task = data_variable["tasks"][i-1]
        # an dieser Stelle werden alle Daten des Tasks eingelesen
        stringTaskName = task["taskname"]
        stringTaskID = task["taskID"]
        stringAdditionalText = task["additionalText"]
        stringCode = task["code"]
        AllVariant = task["allVariant"]

        ListReturnTask.append(stringTaskID)
        ListReturnTask.append(stringTaskName)
        ListReturnTask.append(stringAdditionalText)
        ListReturnTask.append(stringCode)
        # --------------------------------------------------------
        # einlesen der nested allVariant-Antwortalternativen
        listTrueAllVariantAnswer = AllVariant[0]["trueAnswers"]
        listFalseAllVariantAnswer = AllVariant[0]["falseAnswers"]
        stringAllVariantTask = AllVariant[0]["task"]
        ListReturnTask.append(stringAllVariantTask)

        listAllVariantAnswer_Temp = []
        listAllVariantTRUE = []
        for trueAllVariantAnswer in listTrueAllVariantAnswer:
            listAllVariantAnswer_Temp.append(trueAllVariantAnswer["answer"])
            listAllVariantTRUE.append(trueAllVariantAnswer["answer"])
        for falseAllVariantAnswer in listFalseAllVariantAnswer:
            listAllVariantAnswer_Temp.append(falseAllVariantAnswer["answer"])

        #random.shuffle(listAllVariantAnswer_Temp)
        ListReturnTask.append(listAllVariantTRUE)
        ListReturnTask.append(listAllVariantAnswer_Temp)
        listAllVariantAnswer_Temp = []
        listAllVariantTRUE = []
        # --------------------------------------------------------
        # einlesen der nested Variants-Antwortalternativen
        listVariantAnswers_Temp = []
        data_json_task_variants = task["Variants"]
        stringVariantTask = task["Variants"][0]["task"]
        ListReturnTask.append(stringVariantTask)

        ListAllvariant = []
        for variant in data_json_task_variants:
            variantL = []
            stringAllVariantID = variant["id"]
            trueVariantsAnswer = variant["trueAnswer"]
            listFalseVariantsAnswer = variant["falseAnswers"]

            listVariantAnswers_Temp.append(trueVariantsAnswer)
            for falseVariantsAnswer in listFalseVariantsAnswer:
                listVariantAnswers_Temp.append(falseVariantsAnswer["answer"])

            variantL.append(stringAllVariantID)
            random.shuffle(listVariantAnswers_Temp)
            variantL.append(trueVariantsAnswer)
            variantL.append(listVariantAnswers_Temp)
            ListAllvariant.append(variantL)
            listVariantAnswers_Temp = []
        ListReturnTask.append(ListAllvariant)
        ListReturnAllTasks.append(ListReturnTask)
        ListReturnTask = []

    return ListReturnAllTasks

# Denke diese Funktion wird später für das Qualitätsmanagment System besser zu nutzen!
# TODO Muss sicher gemacht werden wegen outofRange Errors!!! Kleinerster Wert 1 -> MaximalWert Berechnen?????
def readOneTask(i):
    ListReturnTask = []

    task = data_variable["tasks"][i-1]
    # an dieser Stelle werden alle Daten des Tasks eingelesen
    stringTaskName = task["taskname"]
    stringTaskID = task["taskID"]
    stringAdditionalText = task["additionalText"]
    stringCode = task["code"]
    AllVariant = task["allVariant"]

    ListReturnTask.append(stringTaskID)
    ListReturnTask.append(stringTaskName)
    ListReturnTask.append(stringAdditionalText)
    ListReturnTask.append(stringCode)
    # --------------------------------------------------------
    # einlesen der nested allVariant-Antwortalternativen
    listTrueAllVariantAnswer = AllVariant[0]["trueAnswers"]
    listFalseAllVariantAnswer = AllVariant[0]["falseAnswers"]
    stringAllVariantTask = AllVariant[0]["task"]
    ListReturnTask.append(stringAllVariantTask)

    listAllVariantAnswer_Temp = []
    listAllVariantTRUE = []
    for trueAllVariantAnswer in listTrueAllVariantAnswer:
        listAllVariantAnswer_Temp.append(trueAllVariantAnswer["answer"])
        listAllVariantTRUE.append(trueAllVariantAnswer["answer"])
    for falseAllVariantAnswer in listFalseAllVariantAnswer:
        listAllVariantAnswer_Temp.append(falseAllVariantAnswer["answer"])

    #random.shuffle(listAllVariantAnswer_Temp)
    ListReturnTask.append(listAllVariantTRUE)
    ListReturnTask.append(listAllVariantAnswer_Temp)
    listAllVariantAnswer_Temp = []
    listAllVariantTRUE = []
    # --------------------------------------------------------
    # einlesen der nested Variants-Antwortalternativen
    listVariantAnswers_Temp = []
    data_json_task_variants = task["Variants"]
    stringVariantTask = task["Variants"][0]["task"]
    ListReturnTask.append(stringVariantTask)

    ListAllvariant = []
    for variant in data_json_task_variants:
        variantL = []
        stringAllVariantID = variant["id"]
        trueVariantsAnswer = variant["trueAnswer"]
        listFalseVariantsAnswer = variant["falseAnswers"]

        listVariantAnswers_Temp.append(trueVariantsAnswer)
        for falseVariantsAnswer in listFalseVariantsAnswer:
            listVariantAnswers_Temp.append(falseVariantsAnswer["answer"])

        variantL.append(stringAllVariantID)
        random.shuffle(listVariantAnswers_Temp)
        variantL.append(trueVariantsAnswer)
        variantL.append(listVariantAnswers_Temp)
        ListAllvariant.append(variantL)
        listVariantAnswers_Temp = []
    ListReturnTask.append(ListAllvariant)

    return ListReturnTask

# Einlesen aller Tasks mit PRINT
def readAllTasks_print():
    for task in data_json_tasks:
        # an dieser Stelle werden alle Daten des Tasks eingelesen
        stringTaskName = task["taskname"]
        stringTaskID = task["taskID"]
        stringAdditionalText = task["additionalText"]
        stringCode = task["code"]
        AllVariant = task["allVariant"]

        print(stringTaskID)
        print(stringTaskName)
        print(stringAdditionalText)
        print(stringCode)
        # --------------------------------------------------------
        # einlesen der nested allVariant-Antwortalternativen
        listTrueAllVariantAnswer = AllVariant[0]["trueAnswers"]
        listFalseAllVariantAnswer = AllVariant[0]["falseAnswers"]
        stringAllVariantTask = AllVariant[0]["task"]

        listAllVariantAnswer_Temp = []
        for trueAllVariantAnswer in listTrueAllVariantAnswer:
            print(trueAllVariantAnswer["answer"] + "\n----")
            listAllVariantAnswer_Temp.append(trueAllVariantAnswer["answer"])
        for falseAllVariantAnswer in listFalseAllVariantAnswer:
            print(falseAllVariantAnswer["answer"] + "\n----")
            listAllVariantAnswer_Temp.append(falseAllVariantAnswer["answer"])

        random.shuffle(listAllVariantAnswer_Temp)
        print(stringAllVariantTask)
        print(listAllVariantAnswer_Temp)
        listAllVariantAnswer_Temp = []
        # --------------------------------------------------------
        # einlesen der nested Variants-Antwortalternativen
        listVariantAnswers_Temp = []
        data_json_task_variants = task["Variants"]

        for variant in data_json_task_variants:
            stringAllVariantID = variant["id"]
            stringVariantTask = variant["task"]
            trueVariantsAnswer = variant["trueAnswer"]
            listFalseVariantsAnswer = variant["falseAnswers"]

            print(trueVariantsAnswer + "\n----")
            listVariantAnswers_Temp.append(trueVariantsAnswer)
            for falseVariantsAnswer in listFalseVariantsAnswer:
                print(falseVariantsAnswer["answer"] + "\n----")
                listVariantAnswers_Temp.append(falseVariantsAnswer["answer"])

            print(stringAllVariantID)
            print(stringVariantTask)
            random.shuffle(listVariantAnswers_Temp)
            print(listVariantAnswers_Temp)
            listVariantAnswers_Temp = []


def readOneTask_print(i):
    task = data_variable["tasks"][i-1]
    # an dieser Stelle werden alle Daten des Tasks eingelesen
    stringTaskName = task["taskname"]
    stringTaskID = task["taskID"]
    stringAdditionalText = task["additionalText"]
    stringCode = task["code"]
    # -> -> -> hier noch weitere Variablen einlesen
    AllVariant = task["allVariant"]

    print(stringTaskID)
    print(stringTaskName)
    print(stringAdditionalText)
    print(stringCode)
    # --------------------------------------------------------
    # einlesen der nested allVariant-Antwortalternativen
    listTrueAllVariantAnswer = AllVariant[0]["trueAnswers"]
    listFalseAllVariantAnswer = AllVariant[0]["falseAnswers"]
    stringAllVariantTask = AllVariant[0]["task"]

    listAllVariantAnswer_Temp = []
    for trueAllVariantAnswer in listTrueAllVariantAnswer:
        print(trueAllVariantAnswer["answer"] + "\n----")
        listAllVariantAnswer_Temp.append(trueAllVariantAnswer["answer"])
    for falseAllVariantAnswer in listFalseAllVariantAnswer:
        print(falseAllVariantAnswer["answer"] + "\n----")
        listAllVariantAnswer_Temp.append(falseAllVariantAnswer["answer"])

    random.shuffle(listAllVariantAnswer_Temp)
    print(stringAllVariantTask)
    print(listAllVariantAnswer_Temp)
    listAllVariantAnswer_Temp = []
    # --------------------------------------------------------
    # einlesen der nested Variants-Antwortalternativen
    listVariantAnswers_Temp = []
    data_json_task_variants = task["Variants"]

    for variant in data_json_task_variants:
        stringAllVariantID = variant["id"]
        stringVariantTask = variant["task"]
        trueVariantsAnswer = variant["trueAnswer"]
        listFalseVariantsAnswer = variant["falseAnswers"]

        #print(trueVariantsAnswer + "\n----")
        listVariantAnswers_Temp.append(trueVariantsAnswer)
        for falseVariantsAnswer in listFalseVariantsAnswer:
            #print(falseVariantsAnswer["answer"] + "\n----")
            listVariantAnswers_Temp.append(falseVariantsAnswer["answer"])

        #print(stringAllVariantID)
        #print(stringVariantTask)
        random.shuffle(listVariantAnswers_Temp)
        #print(listVariantAnswers_Temp)
        listVariantAnswers_Temp = []
