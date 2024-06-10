from einlesenAufgabe import *
from APIChatGPT import *
from statistic import *
import re
import csv


def parseAllAnswers(listAllVariantAnswer):
    listAllVariantAnswer_T = listAllVariantAnswer.copy()
    random.shuffle(listAllVariantAnswer_T)
    n = 1
    originalShuffelNumberTuple = []
    stringAnswers = ""
    for answer in listAllVariantAnswer_T:
        stringAnswers = stringAnswers + str(n) + ".)" + "\n" + answer + "\n"

        ind = listAllVariantAnswer.index(answer)
        originalShuffelNumberTuple.append((ind + 1, n))
        n = n + 1

    return stringAnswers, sorted(originalShuffelNumberTuple)


def parseAIResponse(AIResponse):
    returnList = []
    expression = r'\d+\.\)\s*'
    # expression = r'\d+\.\s*'
    # print(AIResponse)
    while True:
        match = re.search(expression, AIResponse)
        if match:
            number = int(match.group(0).strip('.)\t\n '))
            returnList.append(number)
            AIResponse = AIResponse[:match.start()] + AIResponse[match.end():]

        else:
            break

    if len(returnList) == 0:  ## falls die Liste leer ist gabs einen parse Fehler
        expression = r'\d+\.\s*'  ## ein bekannter Fehler war bisher das die anzeige der Werte bei 1. , 2. .. statt 1.) 2.) war
        ## sehe Probleme bei dieser Workaround Lösung falls im Code irgendwas mit 1. steht.
        while True:
            match = re.search(expression, AIResponse)
            if match:
                number = int(match.group(0).strip('.)\t\n '))
                returnList.append(number)
                AIResponse = AIResponse[:match.start()] + AIResponse[match.end():]

            else:
                break

    # print(returnList)
    # print("----------------------------")
    return returnList


def controllAIResponse(controllTuple, listAllVariantTRUE, aiAnswers, csvData_dir, round):
    nTrue = len(listAllVariantTRUE)
    n = len(controllTuple)
    TRTuple = []
    FRTuple = []
    matchVectorRound = []
    csvData_Round = [["Number of Answer", "Postition in this Round", "Matches?"]]

    for tuple in controllTuple:  # tuple mit trueAnswer und tuple mit falseAnswer
        if tuple[0] <= nTrue:
            TRTuple.append(tuple)
        else:
            FRTuple.append(tuple)

    # print(TRTuple)
    # print(FRTuple)

    # testanswer01 = [1, 10, 2, 12, 9, 5]
    # ALLE AUS DEM CONTROLLTUPLE ZIEHEN DIE DIE AI ALS RICHTIG SIEHT:

    # HIER WERDEN DIE RAUSGEZOGEN DIE TRUE SIND UND DIE DIE KI ALS RICHTIG SIEHT
    print("-----------------------TRUE/KIDENKTRICHTIG")
    for answer in aiAnswers:
        for tuple in list(TRTuple):
            if answer == tuple[1]:
                print(tuple)  # HIER MUSS WAS PASSIEREN WEGEN MATRIX
                matchVectorRound.append((tuple[0], "match"))
                csvData_Round.append([tuple[0], tuple[1], 1])

                controllTuple.remove(tuple)
                TRTuple.remove(tuple)

    # print(controllTuple)
    # print(matchVectorRound)

    print("-----------------------FALSE/KIDENKTRICHTIG")
    # HIER WERDEN DIE RAUSGEZOGEN DIE FALSE SIND ABER DIE KI ALS RICHTIG SIEHT
    for answer in aiAnswers:
        for tuple in list(FRTuple):
            if answer == tuple[1]:
                print(tuple)  # HIER MUSS WAS PASSIEREN WEGEN MATRIX
                matchVectorRound.append((tuple[0], "no match"))
                csvData_Round.append([tuple[0], tuple[1], 0])

                controllTuple.remove(tuple)
                FRTuple.remove(tuple)

    # print(controllTuple)

    TFTuple = []
    FFTuple = []
    for tuple in controllTuple:
        if tuple[0] <= nTrue:
            TFTuple.append(tuple)
        else:
            FFTuple.append(tuple)

    print("-----------------------TRUE/KIDENKTFALSCH")
    for answer in aiAnswers:
        for tuple in list(TFTuple):
            if answer != tuple[1]:
                print(tuple)  # HIER MUSS WAS PASSIEREN WEGEN MATRIX
                matchVectorRound.append((tuple[0], "no match"))
                csvData_Round.append([tuple[0], tuple[1], 0])

                controllTuple.remove(tuple)
                TFTuple.remove(tuple)

    # print(controllTuple)

    print("-----------------------FALSE/KIDENKTFALSCH")
    for answer in aiAnswers:
        for tuple in list(FFTuple):
            if answer != tuple[1]:
                print(tuple)  # HIER MUSS WAS PASSIEREN WEGEN MATRIX
                matchVectorRound.append((tuple[0], "match"))
                csvData_Round.append([tuple[0], tuple[1], 1])

                controllTuple.remove(tuple)
                FFTuple.remove(tuple)

    csv_completeRound = [("Round " + str(round), csvData_Round)]

    print(csvData_Round)
    print(csv_completeRound)

    with open(csvData_dir, "a", newline="") as csv_file:
        # Create a CSV writer object
        csv_writer = csv.writer(csv_file)

        # Write each round's title and sorted data with titles as separate rows in the CSV file
        for round_title, round_data in csv_completeRound:
            sorted_round_data = [round_data[0]]  # Include the titles in the sorted output
            sorted_round_data.extend(sorted(round_data[1:], key=lambda x: int(x[0])))  # Sort data by Position
            csv_writer.writerow([round_title])  # Write round title as a separate row
            csv_writer.writerows(sorted_round_data)
            csv_writer.writerow([])  # Add an empty row between rounds

    # print(sorted(matchVectorRound))
    print("---")
    print("Auswertung beendet")
    print("---")

    return sorted(matchVectorRound)


def buildMatchMatrix(matchVectorRound, matrix, listAllVariantAnswer):
    n = len(listAllVariantAnswer)

    for i in range(0, n):
        matrix[i].append(matchVectorRound[i][1])


def doPermutations(n, stringAdditionalText, stringCode, stringAllVariantTask, listAllVariantAnswer, listAllVariantTRUE,
                   matrix, csvdata_dir):  # Beispiel wäre n=3 weil drei Testdaten
    for i in range(0, n):
        stringAnswers, originalShuffelNumberTuple = parseAllAnswers(listAllVariantAnswer)

        ResponseAIAnswer = ""
        ResponseAIAnswer = ChatGPT_allVariants(stringAdditionalText, stringCode, stringAllVariantTask, stringAnswers, listAllVariantTRUE)

        print(ResponseAIAnswer)
        print("\n---------Ende ChatGPT Runde " + str(i + 1) + "->-> Start der Auswertung-------------------")

        AIAnswerVector = parseAIResponse(
            ResponseAIAnswer)  # hier muss die Funktion die die AI Response parst aufgerufen werden matchvectorround bekommt dann [1,2,3,4,5]
        matchVectorRound = controllAIResponse(originalShuffelNumberTuple, listAllVariantTRUE, AIAnswerVector,
                                              csvdata_dir, i + 1)
        buildMatchMatrix(matchVectorRound, matrix, listAllVariantAnswer)


def buildMatchPoints(preparedMatchValues):
    matches = []
    for round in preparedMatchValues:
        matches.append(round[1])
    return matches


# bisher wird ausnahmelos die Schätzwahrscheinlichkeit des AI-Systems angepasst
def statisticBackpropagation(N, matches, HumanEstimateProbabilityForCorrect, AIEstimateProbabilityForCorrect):
    HumanEstimateProbabilityForWrong = 1 - HumanEstimateProbabilityForCorrect
    AIEstimateProbabilityForCorrect = AIEstimateProbabilityForCorrect * 100
    print(HumanEstimateProbabilityForWrong)
    print(AIEstimateProbabilityForCorrect)

    # Funktion berechnet gerade nur aufbasis der matches eine neie KI-Warscheinlichkeit
    # Eigentlich müsste gefragt werden Aufgabe Korrekt oder nicht Korrekt
    # Und falls der Prüfer sagt nicht korrekt müsste dieser die nicht korrekte antwortmöglichkeit angeben
    # diese müsste dann gedreht werden z.B wenn 7 Übereinstimmungen nicht korrekt sind werden diese zu N-7 Übereinstimmungen in der Rechnung

    allMatches = 0
    amountAnswers = len(matches)
    for match in matches:
        allMatches = allMatches + match
    allMatchesAverage = allMatches / amountAnswers
    MeasuredProbabilityOnMatches = (100 / N) * allMatchesAverage
    NewAIEstimateProbabilityForCorrect = (HumanEstimateProbabilityForCorrect * AIEstimateProbabilityForCorrect) + (
            HumanEstimateProbabilityForWrong * MeasuredProbabilityOnMatches)

    print("Durchgänge N= " + str(N))
    print("Antwortmöglichkeiten amountAnswers= " + str(amountAnswers))
    print("Alle Matches addiert allMatches= " + str(allMatches))
    print("Durchschnittliche Matches pro Antwort= " + str(allMatchesAverage))
    print("Daraus resultierende Wahrscheinlichkeit basierend Trefferquote MeasuredProbabilityOnMatches= " + str(
        MeasuredProbabilityOnMatches))
    print("Daraus neue resultuerende KI-Wahrscheinlichkeit: " + str(NewAIEstimateProbabilityForCorrect))

    return NewAIEstimateProbabilityForCorrect / 100


def apiCommunicationOneTask_sB(n):
    fullTask = readOneTask(n)
    stringTaskID = fullTask[0]
    stringTaskName = fullTask[1]
    stringAdditionalText = fullTask[2]
    stringCode = fullTask[3]
    stringAllVariantTask = fullTask[4]
    listAllVariantTRUE = fullTask[5]
    listAllVariantAnswer = fullTask[6]
    stringVariantsTask = fullTask[7]
    listVariants = fullTask[8]

    AIEstimateProbabilityForCorrect = 0.75
    HumanEstimateProbabilityForCorrect = 0.90

    n = len(listAllVariantAnswer)
    program = True

    matrix = []
    for i in range(1, n + 1):
        roundList = [str(i)]
        matrix.append(roundList)

    posteriors, msg, N = match_bayes_STATIC_V_NCalc(HumanEstimateProbabilityForCorrect, AIEstimateProbabilityForCorrect,
                                                    0.9, 0.9, 0.1, 0.1)
    doPermutations(N, stringAdditionalText, stringCode, stringAllVariantTask, listAllVariantAnswer, listAllVariantTRUE,
                   matrix)

    preparedMatchValues = prepareMatrixforStatistic(matrix)
    plotKtoPosterios(stringTaskID, posteriors, msg, preparedMatchValues)

    while program:
        answerUser = input("Should the answer get a next pass with new calculated probabilities? Answer yes or no.\n")
        if answerUser == "yes":
            matrix = []
            for i in range(1, n + 1):
                roundList = [str(i)]
                matrix.append(roundList)

            matches = buildMatchPoints(preparedMatchValues)
            AIEstimateProbabilityForCorrect = statisticBackpropagation(N, matches, HumanEstimateProbabilityForCorrect,
                                                                       AIEstimateProbabilityForCorrect)
            print(AIEstimateProbabilityForCorrect)
            # wiederholung des durchgangs
            posteriors, msg, N = match_bayes_STATIC_V_NCalc(HumanEstimateProbabilityForCorrect,
                                                            AIEstimateProbabilityForCorrect, 0.95, 0.9, 0.1, 0.1)
            doPermutations(N, stringAdditionalText, stringCode, stringAllVariantTask, listAllVariantAnswer,
                           listAllVariantTRUE, matrix)

            preparedMatchValues = prepareMatrixforStatistic(matrix)
            plotKtoPosterios(stringTaskID, posteriors, msg, preparedMatchValues)
            # wiederholung des durchgangs vorbei
            program = True
        elif answerUser == "no":
            program = False
        else:
            print("Wrong Answer")


def apiCommunicationOneTask_sBack(n):
    fullTask = readOneTask(n)
    stringTaskID = fullTask[0]
    stringTaskName = fullTask[1]
    stringAdditionalText = fullTask[2]
    stringCode = fullTask[3]
    stringAllVariantTask = fullTask[4]
    listAllVariantTRUE = fullTask[5]
    listAllVariantAnswer = fullTask[6]
    stringVariantsTask = fullTask[7]
    listVariants = fullTask[8]

    AIEstimateProbabilityForCorrect = 0.75
    HumanEstimateProbabilityForCorrect = 0.95

    n = len(listAllVariantAnswer)
    program = True

    matrix = []
    for i in range(1, n + 1):
        roundList = [str(i)]
        matrix.append(roundList)

    posteriors, msg, N = match_bayes_STATIC_V_NCalc(HumanEstimateProbabilityForCorrect, AIEstimateProbabilityForCorrect,
                                                    0.95, 0.9, 0.1, 0.1)
    doPermutations(N, stringAdditionalText, stringCode, stringAllVariantTask, listAllVariantAnswer, listAllVariantTRUE,
                   matrix)

    preparedMatchValues = prepareMatrixforStatistic(matrix)
    # preparedMatchValues = [['1', 12, 8, 20], ['2', 11, 9, 20], ['3', 19, 1, 20], ['4', 18, 2, 20], ['5', 12, 8, 20], ['6', 18, 2, 20], ['7', 18, 2, 20], ['8', 20, 0, 20], ['9', 19, 1, 20], ['10', 16, 4, 20], ['11', 11, 9, 20], ['12', 20, 0, 20], ['13', 7, 13, 20], ['14', 19, 1, 20]]
    plotKtoPosterios(stringTaskID, posteriors, msg, preparedMatchValues)

    while program:
        answerUser = input(
            "Based on the matches, did the AI system answer any answer alternatives incorrectly?? Answer yes or no.\n")
        if answerUser == "yes":
            answerUser01 = input(
                "Which answer alternatives did the AI system answer incorrectly, based on matches? Answer with the numbers of the answer choices\n")

            matrix = []
            for i in range(1, n + 1):
                roundList = [str(i)]
                matrix.append(roundList)

            numbers = re.findall(r'\d+', answerUser01)
            numbers = [int(numb) for numb in numbers]
            AIFoundValues = []
            for i in numbers:
                if i not in AIFoundValues:
                    AIFoundValues.append(i)

            newPreparedMatchValues = []
            # preparedMatchValues ([answerNumber, match, noMatch, amountRounds], ....)
            for preparedMatchValue in preparedMatchValues:
                if int(preparedMatchValue[0]) in AIFoundValues:
                    newPreparedMatchValues.append(
                        [preparedMatchValue[0], preparedMatchValue[2], preparedMatchValue[1], preparedMatchValue[3]])
                else:
                    newPreparedMatchValues.append(
                        [preparedMatchValue[0], preparedMatchValue[1], preparedMatchValue[2], preparedMatchValue[3]])

            matches = buildMatchPoints(newPreparedMatchValues)
            AIEstimateProbabilityForCorrect = statisticBackpropagation(N, matches, HumanEstimateProbabilityForCorrect,
                                                                       AIEstimateProbabilityForCorrect)
            print(AIEstimateProbabilityForCorrect)
            # wiederholung des durchgangs
            posteriors, msg, N = match_bayes_STATIC_V_NCalc(HumanEstimateProbabilityForCorrect,
                                                            AIEstimateProbabilityForCorrect, 0.95, 0.9, 0.1, 0.1)
            doPermutations(N, stringAdditionalText, stringCode, stringAllVariantTask, listAllVariantAnswer,
                           listAllVariantTRUE, matrix)

            preparedMatchValues = prepareMatrixforStatistic(matrix)
            plotKtoPosterios(stringTaskID, posteriors, msg, preparedMatchValues)
            # wiederholung des durchgangs vorbei

            program = True
        elif answerUser == "no":
            program = False
        else:
            print("Wrong Answer")


def apiCommunicationOneTask(n):
    dir = my_path + "/csvfromValues"
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))

    csv_data_dir = my_path + "/csvfromValues/data_" + str(n) + ".csv"
    with open(csv_data_dir, "w"):
        pass

    fullTask = readOneTask(n)
    stringTaskID = fullTask[0]
    stringTaskName = fullTask[1]
    stringAdditionalText = fullTask[2]
    stringCode = fullTask[3]
    stringAllVariantTask = fullTask[4]
    listAllVariantTRUE = fullTask[5]
    listAllVariantAnswer = fullTask[6]
    stringVariantsTask = fullTask[7]
    listVariants = fullTask[8]

    n = len(listAllVariantAnswer)

    matrix = []
    for i in range(1, n + 1):
        roundList = [str(i)]
        matrix.append(roundList)

    # doPermutations macht die Übereinstimmungsmatrix ... matrix erstmal als festen Wert
    posteriors, msg, N = match_bayes_STATIC_V_NCalc(0.90, 0.75, 0.90, 0.9, 0.1,  # 0.95, 0.75, 0.9, 0.6, 0.1 für 5
                                                    0.1)  # Statistik wird für Werte berechnet später durch Rückkopplung angepasst, N Werte werden berechnet für Permutation
    doPermutations(N, stringAdditionalText, stringCode, stringAllVariantTask, listAllVariantAnswer, listAllVariantTRUE,
                   matrix, csv_data_dir)  # zwei um für N-Aufgaben test wenig permutation zu haben
    # matrix = [['1', 'keine übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'keine übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'keine übereinstimmung', 'übereinstimmung'], ['2', 'keine übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'keine übereinstimmung', 'keine übereinstimmung', 'übereinstimmung', 'keine übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'keine übereinstimmung', 'übereinstimmung', 'keine übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'keine übereinstimmung', 'übereinstimmung', 'keine übereinstimmung'], ['3', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'keine übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'keine übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'keine übereinstimmung', 'keine übereinstimmung', 'keine übereinstimmung', 'keine übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'keine übereinstimmung', 'keine übereinstimmung'], ['4', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'keine übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'keine übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung'], ['5', 'übereinstimmung', 'übereinstimmung', 'keine übereinstimmung', 'keine übereinstimmung', 'keine übereinstimmung', 'keine übereinstimmung', 'übereinstimmung', 'keine übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'keine übereinstimmung', 'keine übereinstimmung', 'übereinstimmung', 'übereinstimmung'], ['6', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'keine übereinstimmung', 'übereinstimmung', 'keine übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'keine übereinstimmung', 'keine übereinstimmung'], ['7', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'keine übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'keine übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'keine übereinstimmung', 'keine übereinstimmung', 'übereinstimmung'], ['8', 'keine übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'keine übereinstimmung', 'keine übereinstimmung'], ['9', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung'], ['10', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'keine übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'keine übereinstimmung', 'übereinstimmung', 'keine übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'keine übereinstimmung', 'keine übereinstimmung'], ['11', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'keine übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'keine übereinstimmung', 'übereinstimmung', 'keine übereinstimmung', 'keine übereinstimmung', 'übereinstimmung', 'keine übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung'], ['12', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung'], ['13', 'keine übereinstimmung', 'übereinstimmung', 'keine übereinstimmung', 'keine übereinstimmung', 'keine übereinstimmung', 'keine übereinstimmung', 'keine übereinstimmung', 'keine übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'keine übereinstimmung', 'keine übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'keine übereinstimmung', 'keine übereinstimmung', 'übereinstimmung', 'keine übereinstimmung'], ['14', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'keine übereinstimmung', 'übereinstimmung', 'keine übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'keine übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung', 'übereinstimmung']]
    # Ab hier läuft die Statistik
    print(matrix)
    preparedMatchValues = prepareMatrixforStatistic(matrix)
    plotKtoPosterios(stringTaskID, posteriors, msg, preparedMatchValues)


def apiCommunicationALLTasks():
    dir = my_path + "/correct_task"
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))

    dir = my_path + "/control_task"
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))

    dir = my_path + "/csvfromValues"
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))

    allTasks = readAllTasks()

    # matrixAllTasks = []

    for task in allTasks:
        stringTaskID = task[0]
        stringTaskName = task[1]
        stringAdditionalText = task[2]
        stringCode = task[3]
        stringAllVariantTask = task[4]
        listAllVariantTRUE = task[5]
        listAllVariantAnswer = task[6]
        stringVariantsTask = task[7]
        listVariants = task[8]
        n = len(listAllVariantAnswer)

        matrixOneTask = []
        for i in range(1, n + 1):
            roundList = [str(i)]
            matrixOneTask.append(roundList)

        csv_data_dir = my_path + "/csvfromValues/data_" + str(stringTaskID) + ".csv"
        with open(csv_data_dir, "w"):
            pass

        posteriors, msg, N = match_bayes_STATIC_V_NCalc(0.90, 0.75, 0.90, 0.9, 0.1,
                                                        0.1)  # Statistik wird für Werte berechnet später durch Rückkopplung angepasst, N Werte werden berechnet für Permutation
        doPermutations(N, stringAdditionalText, stringCode, stringAllVariantTask, listAllVariantAnswer,
                       listAllVariantTRUE, matrixOneTask,
                       csv_data_dir)  # zwei um für N-Aufgaben test wenig permutation zu haben

        print(matrixOneTask)

        preparedMatchValues = prepareMatrixforStatistic(matrixOneTask)
        plotKtoPosterios(stringTaskID, posteriors, msg, preparedMatchValues)

        # matrixAllTasks.append(matrixOneTask)


def apiCommunicationNTasks(firstTaskID, lastTaskID):
    # matrixAllTasks = []

    for n in range(firstTaskID, lastTaskID + 1):
        fullTask = readOneTask(n)
        stringTaskID = fullTask[0]
        stringTaskName = fullTask[1]
        stringAdditionalText = fullTask[2]
        stringCode = fullTask[3]
        stringAllVariantTask = fullTask[4]
        listAllVariantTRUE = fullTask[5]
        listAllVariantAnswer = fullTask[6]
        stringVariantsTask = fullTask[7]
        listVariants = fullTask[8]

        csv_data_dir = my_path + "/csvfromValues/data_" + str(stringTaskID) + ".csv"
        with open(csv_data_dir, "w"):
            pass

        n = len(listAllVariantAnswer)

        matrixOneTask = []
        for i in range(1, n + 1):
            roundList = [str(i)]
            matrixOneTask.append(roundList)

        # posteriors, msg, N = match_bayes_STATIC_V_NCalc(0.90, 0.75, 0.90, 0.9, 0.1, 0.1)
        posteriors, msg, lowerbound, N = Bayes_Modell_Calculation(0.90, 0.75, 0.9)

        doPermutations(N, stringAdditionalText, stringCode, stringAllVariantTask, listAllVariantAnswer,
                       listAllVariantTRUE, matrixOneTask,
                       csv_data_dir)  # zwei um für N-Aufgaben test wenig permutation zu haben

        print(matrixOneTask)

        preparedMatchValues = prepareMatrixforStatistic(matrixOneTask)
        plotKtoPosterios(stringTaskID, posteriors, msg, preparedMatchValues, lowerbound)

        # matrixAllTasks.append(matrixOneTask)
