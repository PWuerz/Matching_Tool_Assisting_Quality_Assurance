import json
import random


with open("questions_test.json", "r") as file:
    json_data = file.read()

data_variable = json.loads(json_data)

#data_json_task = data_variable["tasks"]

data_json_task = data_variable["tasks"]
#data_json_task_variants = data_variable["tasks"][0]["Variants"]
data_json_task_variants_two = data_variable["tasks"][0]["Variants"][1]
data_json_task_variants_fanswers = data_variable["tasks"][0]["Variants"][1]["falseAnswers"]
data_json_task_variants_fanswers_one = data_variable["tasks"][0]["Variants"][1]["falseAnswers"][0]
data_json_task_variants_fanswers_one_value = data_variable["tasks"][0]["Variants"][1]["falseAnswers"][0]["answer"]
#data_json_allVariant = data_variable["tasks"][0]["allVariant"]



stringPattern = "The following question is asked by me according to the following pattern: Example, question, and 1/2/3/4 answer alternatives. Answer me this question in the following \"how to answer Pattern\": \n\nhow to answer pattern: Answer in detail the following question in the following pattern:\nA. give the correct answer in the form 1,2,3 or 4\nB. give reasons why you think this answer is correct.\nC. give reasons why the other three answers are wrong.\n\n"
stringContext = ""
stringQuestion = ""
stringAnswers = ["1."]


#print(stringPattern + stringContext + stringQuestion + stringAnswers[0])
#print(data_variable)
#print(data_json_task_variants_fanswers_one_value)

#for answer in data_json_task_variants_fanswers:
#    print(answer["answer"])



for tasks in data_json_task:
    #print(tasks)
    stringTaskName = tasks["taskname"]

    stringAllVariant= tasks["allVariant"]
    stringTaskID = tasks["taskID"]
    stringAdditionalText = stringAllVariant[0]["additionalText"]
    stringCode = stringAllVariant[0]["code"]
    stringTask = stringAllVariant[0]["task"]
    ListTrueA = stringAllVariant[0]["trueAnswers"]
    ListFalseA = stringAllVariant[0]["falseAnswers"]

    print("->>>>>>> " + str(stringTaskID))
    print("AllVARIANT: \n")
    print("Taskname:\n" + stringTaskName)
    print("---")
    print("AdditionalText:\n" + stringAdditionalText)
    print("---")
    print("Code:\n" + stringCode)
    print("---")
    print("Task:\n" + stringTask)
    print("---")

    ListAllAnswers = []
    print("Answers:")
    for tanswer in ListTrueA:
        print(tanswer["answer"] +"\n----")
        ListAllAnswers.append(tanswer["answer"])
    for fanswer in ListFalseA:
        print(fanswer["answer"]+"\n----")
        ListAllAnswers.append(fanswer["answer"])
    random.shuffle(ListAllAnswers)

    #print(ListAllAnswers)
    ListAllAnswers = []






    print("\n-----||-----")
    print("VARIANTS Answers: \n")
    ListVariantAnswers = []

    data_json_task_variants = tasks["Variants"]


    for variant in data_json_task_variants:

        TrueV = variant["trueAnswer"]
        print(TrueV+"\n----")

        ListVariantAnswers.append(TrueV)


        ListFalseV = variant["falseAnswers"]
        for FalseV in ListFalseV:
            print(FalseV["answer"]+"\n----")
            ListVariantAnswers.append(FalseV["answer"])



        random.shuffle(ListVariantAnswers)
        #print(ListVariantAnswers)
        print("------|-----")
        ListVariantAnswers = []


    print("-----|||----\n\n\n")

