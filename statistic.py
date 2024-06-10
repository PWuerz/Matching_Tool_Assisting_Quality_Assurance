import PyQt5.QtCore
#import os
#os.environ["QT_API"] = "pyqt5"
import sys
import math
import numpy as np
#import matplotlib.backends.backend_qt5agg
#import matplotlib
#matplotlib.use("Qt5Agg")
#matplotlib.use('agg')
import matplotlib.pyplot as plt
#plt.switch_backend('Qt5Agg')
import os

my_path = os.getcwd()


def binom(n, k):
    return math.comb(n, k)


def calcLikely(n, k, bin, H):
    return bin * pow(H, k) * pow(1 - H, n - k)


def match_bayes_STATIC_V_NCalc(HC, AC, PH1, ThreshHold, ThreshHoldLeft, ThreshHoldRight):
    # HC = 0.95
    HF = 1 - HC
    # AC = 0.75
    AF = 1 - AC

    H1 = HC * AC + HF * AF
    H2 = 1 - H1
    # PH1 = HC
    PH2 = 1 - PH1

    # n = 100

    # ThreshHold = 0.9
    # ThreshHoldLeft = 0.1
    # ThreshHoldRight = 0.1

    N = 0
    isOverThreshHold = False
    isOverThreshHoldLeft = False
    isOverThreshHoldRight = False

    while (isOverThreshHold != True or isOverThreshHoldLeft != True or isOverThreshHoldRight != True):
        N += 1
        binoms = []
        for i in range(N + 1):
            binoms.append((i, binom(N, i)))

        likelyhoods = []
        for n in binoms:
            likelyhoods.append((n[0], calcLikely(N, n[0], n[1], H1), calcLikely(N, n[0], n[1], H2)))

        posteriors = []
        for l in likelyhoods:
            postH1 = (PH1 * l[1]) / (PH1 * l[1] + PH2 * l[2])
            posteriors.append((l[0], postH1, 1 - postH1, (1 - postH1) / postH1))

        left = 0
        right = 0
        for t in posteriors:
            if t[2] / t[1] <= 0.1:
                right += 1
            if t[2] / t[1] >= 10:
                left += 1

        if (1.0 / (N + 1)) * left > ThreshHoldLeft:
            isOverThreshHoldLeft = True
        else:
            isOverThreshHoldLeft = False
        if (1.0 / (N + 1)) * right > ThreshHoldRight:
            isOverThreshHoldRight = True
        else:
            isOverThreshHoldRight = False
        if (1.0 / (N + 1)) * (left + right) > ThreshHold:
            isOverThreshHold = True
        else:
            isOverThreshHold = False

    print("Current N:", N, "\t left=", left, "\t right=", right, "\t All=", (left + right))
    print("\t left%=", (1.0 / (N + 1)) * left, "\t right%=", (1.0 / (N + 1)) * right, "\t All%=",
          (1.0 / (N + 1)) * (left + right))
    msg = "Current N: " + str(N) + "   left= " + str(left) + "   right= " + str(right) + "   All= " + str(left + right) + "\n" + "left%= " + str((1.0 / (N + 1)) * left) + "   right%= " + str((1.0 / (N + 1)) * right) + "   All%= " + str((1.0 / (N + 1)) * (left + right))
    posteriors_arr = np.array(posteriors)
    return posteriors_arr, msg, N

def Bayes_Modell_Calculation_PRINT(HC, AC, PH1):
    # HC = 0.95
    HF = 1 - HC
    # AC = 0.75
    AF = 1 - AC

    H1 = HC * AC + HF * AF
    H2 = 1 - H1
    # PH1 = HC
    PH2 = 1 - PH1

    N = 0
    ConfidenceIntervalsFulfilled = False

    while not ConfidenceIntervalsFulfilled:
        lowerConfidence = 0.0
        upperConfidence = 0.0
        N = N + 1

        binoms = []
        for i in range(N + 1):
            binoms.append((i, binom(N, i)))

        likelyhoods = []
        for n in binoms:
            likelyhoods.append((n[0], calcLikely(N, n[0], n[1], H1), calcLikely(N, n[0], n[1], H2)))
            #print( "H1 Liklehood: " + str(calcLikely(N, n[0], n[1], H1)))
            #print( "H2 Liklehood: " + str(calcLikely(N, n[0], n[1], H2)))

        posteriors = []
        for l in likelyhoods:
            postH1 = (PH1 * l[1]) / (PH1 * l[1] + PH2 * l[2])
            posteriors.append((l[0], postH1, 1 - postH1, (1 - postH1) / postH1))
            #print( "H1 Posterior: " + str(postH1))
            #print( "H2 Posterior: " + str(1 - postH1))

        lowerbound = 0
        upperbound = 0

        for t in posteriors:
            if (t[1] * PH2) / (t[2] * PH1) <= 0.1:
                lowerbound = t[0]
            if (t[1] * PH2) / (t[2] * PH1) <= 10:
                upperbound = t[0]

        for i in range(lowerbound + 1):
            lowerConfidence += calcLikely(N, i, binom(N, i), H2)

        for i in range(upperbound + 1):
            upperConfidence += calcLikely(N, i, binom(N, i), H1)

        upperConfidence = 1 - upperConfidence

        if upperConfidence >= 0.975 and lowerConfidence >= 0.975:
            ConfidenceIntervalsFulfilled = True

        msg = "LowerConficence: " + str(lowerConfidence) + "     upperConfidence: " + str(upperConfidence)
        posteriors_arr = np.array(posteriors)
        print(posteriors_arr)

    return posteriors_arr, msg, lowerbound ,N

def Bayes_Modell_Calculation(HC, AC, PH1):
    # HC = 0.95
    HF = 1 - HC
    # AC = 0.75
    AF = 1 - AC

    H1 = HC * AC + HF * AF
    H2 = 1 - H1
    # PH1 = HC
    PH2 = 1 - PH1

    N = 0
    ConfidenceIntervalsFulfilled = False

    while not ConfidenceIntervalsFulfilled:
        lowerConfidence = 0.0
        upperConfidence = 0.0
        N = N + 1

        binoms = []
        for i in range(N + 1):
            binoms.append((i, binom(N, i)))

        likelyhoods = []
        for n in binoms:
            likelyhoods.append((n[0], calcLikely(N, n[0], n[1], H1), calcLikely(N, n[0], n[1], H2)))

        posteriors = []
        for l in likelyhoods:
            postH1 = (PH1 * l[1]) / (PH1 * l[1] + PH2 * l[2])
            posteriors.append((l[0], postH1, 1 - postH1, (1 - postH1) / postH1))

        lowerbound = 0
        upperbound = 0

        for t in posteriors:
            if (t[1] * PH2) / (t[2] * PH1) <= 0.1:
                lowerbound = t[0]
            if (t[1] * PH2) / (t[2] * PH1) <= 10:
                upperbound = t[0]

        for i in range(lowerbound + 1):
            lowerConfidence += calcLikely(N, i, binom(N, i), H2)

        for i in range(upperbound + 1):
            upperConfidence += calcLikely(N, i, binom(N, i), H1)

        upperConfidence = 1 - upperConfidence

        if upperConfidence >= 0.975 and lowerConfidence >= 0.975:
            ConfidenceIntervalsFulfilled = True

        msg = "LowerConficence: " + str(lowerConfidence) + "     upperConfidence: " + str(upperConfidence)
        posteriors_arr = np.array(posteriors)

    return posteriors_arr, msg, lowerbound ,N


def buildMatchPoints(preparedMatchValues):
    matches = []
    for round in preparedMatchValues:
        matches.append(round[1])
    return matches


def get_all_indices(lst):
    indices_dict = {}
    for i, x in enumerate(lst):
        if x in indices_dict:
            indices_dict[x].append(i + 1)
        else:
            indices_dict[x] = [i + 1]
    return indices_dict

def graficShowProblems(size, matchPoints):
    notEnougthMatchesNumber = round(size/2)

    for matches in matchPoints:
        if matches < notEnougthMatchesNumber:
            return "/control_task"

    return "/correct_task"


# Übereinstimmungsmatrix muss am Ende natürlich bei einigen Funktionen genutzt werden aber zunächst kann ich die glaub
# nur plotten
def plotKtoPosterios(ID, posteriors, msg, preparedMatchValues, lowerbound):
    size = int(posteriors.size / 3)

    matchPoints = buildMatchPoints(preparedMatchValues)
    msg = msg + "\n" + str(matchPoints)

    n = np.empty((size, 1), dtype=object)
    n = posteriors[-1]

    x_values = np.empty((size, 1), dtype=object)
    y_values = np.empty((size, 2), dtype=object)
    z_values = np.empty((size, 1), dtype=object)

    index = 0
    for posterior in posteriors:
        x_values[index] = [posterior[0]]
        y_values[index] = [posterior[1], posterior[2]]
        z_values[index] = [posterior[3]]
        index = index + 1

    plt.xticks(range(0,index),fontsize=8)
    plt.yticks([0.1, 0.2, 0.3, 0.4, 0.5 , 0.6, 0.7, 0.8, 0.9, 1.0], fontsize=8)
    plt.plot(x_values, y_values, 'o', linestyle="--", label=['Posterior H1', 'Posterior H2'])
    # in diesen Plot den Bayesfactor als Y Linie einzeichnen zwischen 3-10 , und 10 und höher
    #plt.plot(z_values, 'x', linestyle="--")
    # Subplot links x y values rechts z values in  verhätniss zu k
    #print(x_values)
    #print(y_values)
    #print(z_values)

    x_polygon = [lowerbound + 1, lowerbound + 2]

    plt.fill_between(x_polygon, 0, 1, color='gray', alpha=0.5, label='Area of weak Bayes Factor')

    # print(matchPoints)
    result = get_all_indices(matchPoints)
    # print(result)

    ii = 0
    for key, Lvalue in result.items():
        label = ""
        # print(key)
        # print(Lvalue)

        for i in range(index):
            x = x_values[i][0]
            y_h1 = y_values[i][0]
            y_h2 = y_values[i][1]
            if i == key:  # The index starts from 0, so the 17th point has index 16
                if ii % 2 == 0:
                    plt.text(x, y_h1, Lvalue, fontsize=8, ha='left', va='top', color='blue')
                    #plt.text(x, y_h2, f'H2: {y_h2}', fontsize=8, ha='left', va='bottom', color='orange')
                else:
                    plt.text(x, y_h1, Lvalue, fontsize=8, ha='left', va='bottom', color='blue')
                    #plt.text(x, y_h2, f'H2: {y_h2}', fontsize=8, ha='left', va='bottom', color='orange')
            ii = ii + 1

    plt.ylabel('Wahrscheinlichkeiten in %', fontsize=16)
    plt.xlabel('Übereinstimmungen',fontsize=16)

    #plt.axhline(y=0.75, color='r', linestyle='dashed')  #0.75 / 0.25
    #plt.text(n[0], 0.775, 'Substantieller Bayes Faktor', fontsize=8, va='center', ha='right', backgroundcolor='none', color="r")

    #plt.axhline(y=0.9095, color='g', linestyle='dashed') #0.9095 / 0.0905
    #plt.text(n[0], 0.93, 'Starker Bayes Faktor', fontsize=8, va='center', ha='right', backgroundcolor='none', color="g")

    plt.text(n[0], -0.15, msg, fontsize=10, va='center', ha='right', backgroundcolor='none')

    plt.legend(fontsize=16)
    #plt.show()
    #manager = plt.get_current_fig_manager()
    #manager.window.showMaximized()
    figure = plt.gcf()  # get current figure
    figure.set_size_inches(18.5, 10.5)
    figure.set_size_inches(18.5, 10.5, forward=True)

    saveFolder = graficShowProblems(index-1, matchPoints)


    plt.savefig(my_path + saveFolder + "/matplotlib" + str(ID) + ".png", dpi=300, bbox_inches='tight')
    plt.clf()


def prepareMatrixforStatistic(matchMatrix):
    returnList = []
    for answerMatchVector in matchMatrix:
        answerNumber = answerMatchVector[0]
        amountRounds = len(answerMatchVector) - 1
        match = answerMatchVector.count("match")
        noMatch = answerMatchVector.count("no match")
        returnList.append([answerNumber, match, noMatch, amountRounds])

    return returnList

# mit dein Einstellungen 80-n gehen noch gut Grafisch darstellbar
# posteriors = match_bayes_STATIC_V_NCalc(0.95, 0.75, 0.95, 0.975, 0.1, 0.1)
# posteriors, msg = match_bayes_STATIC_V_NCalc(0.95, 0.75, 0.95, 0.9, 0.1, 0.1)
# plotKtoPosterios(posteriors, msg, preparedMatchValues)
