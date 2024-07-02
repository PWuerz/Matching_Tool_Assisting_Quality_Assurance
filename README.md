The tool was executed with Ubuntu 22.04.03 LTS on a Windows machine.



The figure illustrates the process used for the experiment, which is consistently implemented in a tool.
For the experiment, exam questions from the courses "Basic Programming Paradigms" and "Advanced Programming Paradigms" were used as the ground truth, as they have been utilized in several exams and have undergone a traditional quality assurance process. These questions, consisting of a question text and multiple true and false answers including code snippets, were not directly presented to the AI system but served as a basis for assessing the correctness rate of the AI compared to the ground truth. To create test questions, the answer alternatives were randomly selected and incorrectly classified to simulate human errors. These questions were then presented to the AI system in random order to avoid bias. For the experiment, a sample size of 31 was determined based on Bayesian statistics and a 97.5% criterion for robust evidence. The AI model, gpt-3.5-turbo, received the tasks within a predetermined answer pattern, and API parameters were adjusted to reduce the model's creativity and unpredictability. Each AI response was parsed and classified as matching or non-matching compared to the artificial human error classification. This process was repeated until the required sample size was reached. Finally, the answers and corresponding tasks were categorized as potentially erroneous.

![image](https://github.com/PWuerz/Matching_Tool_Assisting_Quality_Assurance/assets/49491245/3b1d658b-646a-4442-aa92-49659dd53903)


It was used to create the data for the paper "Assisting Quality Assurance of Examination Tasks: Using a GPT Model and Bayesian Testing for Formative Assessment" by Nico Willert and Phi Katharina Würz.

