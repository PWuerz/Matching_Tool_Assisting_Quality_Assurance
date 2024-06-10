import openai
import random
from timeout_decorator import timeout, TimeoutError

# DIESE FILE MÜSSEN AM ENDE VIELE FUNKTIONEN IN ANDERE FILES GEZOGEN WERDEN !!!! meiste in apiCommunication
openai.api_key = ""


def restartable_timeout(timeout_duration):
    def decorator(func):
        def wrapper(*args, **kwargs):
            while True:
                try:
                    return timeout(timeout_duration)(func)(*args, **kwargs)
                except TimeoutError:
                    print("Function timed out, restarting...")
                    print("...")
                    print("...")
                    print("...")
                    print("...")
                    continue
        return wrapper
    return decorator


@restartable_timeout(20)
def ChatGPT_allVariants(stringAdditionalText, stringCode, stringAllVariantTask, stringAnswers, listAllVariantTRUE):
    n = len(listAllVariantTRUE)

    # Als was soll sich das System verstehen. Optionale Sache
    system = "You are a poet who creates poems that evoke emotions."

    # PATTERN MUSS LEICHT ANGEPASST WERDEN FALLS ÜBERHAUPT CODE DABEI IST ODER ZUM ADDITONAL TEXT

    # stringPatternONE = "The following question is asked by me according to the following pattern: Example, question, and 1/2/3/4 answer alternatives. Answer me this question only with the number of the correct answer alternative.\n\n\n"
    # stringPattern = "The following question is asked by me according to the following pattern: Example like Code, a task question, and answer alternatives with numbers like 1.). Of these answer alternatives, exactly " + str(
    #    n) + " are correct. Answer me this question only with all the numbers of the correct answer alternatives.\n\n\n"
    # stringPatternTEXT = "The following question is asked by me according to the following pattern: Example like Code, a task question, and answer alternatives with numbers like 1.). Answer me this question with the numbers and the text of the correct answer alternatives.\n\n\n"
    stringPattern = "The following question is asked by me according to the following pattern:\n - an \"additionalText\" that describes the context of the task in more detail\n - \"Code\" that will be considered for this task. \n - a \"task question\"\n - and \"answer alternatives\" with numbers like 1.). \n Of these answer alternatives, exactly " + str(
        n) + " are correct. Answer me this question only with all numbers of the correct answer alternatives, in the form 1.) , 2.) and so on. The number, the dot, and the closed parenthesis should always be there\n\n\n"

    stringPattern = "The following question is asked by me according to the following pattern:\n - an \"additionalText\" that describes the context of the task in more detail\n - \"Code\" that will be considered for this task. \n - a \"task question\"\n - and \"answer alternatives\" with numbers like 1.). \n . Answer me this question correctly only with all numbers of the correct answer alternatives, in the form 1.) , 2.) and so on. \n\n\n"

    #stringPattern = "The following question is asked by me according to the following pattern:\n - an \"additionalText\" that describes the context of the task in more detail\n - \"Code\" that will be considered for this task. \n - a \"task question\"\n - and \"answer alternatives\" with numbers like 1.). \n . Answer me this question correctly only with all numbers of the correct answer alternatives, in the form 1.) , 2.) and so on. \n" \
    #                "If [C++:...] is written in the answer alternatives, the content without the C++: in the square brackets is the C++ code you should treat as such. \n\n"

    #stringPattern = "The following question is asked by me according to the following pattern:\n - an \"additionalText\" that describes the context of the task in more detail\n - \"Code\" that will be considered for this task. \n - a \"task question\"\n - and \"answer alternatives\" with numbers like 1.). \n . Answer me this question correctly only with all numbers of the correct answer alternatives, in the form 1.) , 2.) and so on. \n" \
    #                "All questions refer to the programming language C++ \n\n"

    # falls Code existiert muss die Frage ein wenig angepasst werden
    if stringCode != "":
        stringAllVariantTask = "If you look at the code above: " + stringAllVariantTask

    user = stringPattern + "additionalText\n" + stringAdditionalText + "\n\n" + "Code\n" + stringCode + "\n\n\n" + "task question\n" + stringAllVariantTask + "\n\n" + "answer alternatives\n" + stringAnswers
    print(user)

    completion = openai.ChatCompletion.create(
         model="gpt-3.5-turbo",
         temperature=0.2,
         max_tokens=2000,
         messages=[
            # {"role": "system", "content": system },
            # {"role": "assistant", "content": "Programmers drink a lot of coffee!"},
             {"role": "user", "content": user}
         ]
    )

    #response = openai.Completion.create(
    #    engine="text-davinci-003",
    #    prompt=user,
    #    max_tokens=2000,
    #    temperature=0.2,
    # )

    # return response.choices[0].text
    return completion.choices[0].message.content
    # return "1., 2. 3. 4., 6."
    # return ""
