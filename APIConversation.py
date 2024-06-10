import openai

openai.api_key = ""

model_id = "gpt-3.5-turbo"
# Initial message to ask the first question
messages = [ {"role": "user", "content": "Where was the last olympics held? Just tell me the year & country?"} ]

# Call the API
completion = openai.ChatCompletion.create(
model=model_id,
messages=messages
)

# Print the answer we received for the 1st question
print(completion.choices[0].message.content)

# Save the response we received for the 1st question
# so we can pass this context when asking the 2nd question
previousresponse = completion.choices[0].message.content

# Message to ask the Second question
messages.append({"role": "user", "content": "Which country won the most medals in that? Just tell me the country name?"} )

# Send the previous response for the 1st question as well
# so that the context is preserved.
# If this is not sent ChatGPT will have no context to answer the second question
messages.append({"role": "assistant", "content": previousresponse})

# Send the new question along with the context
completion = openai.ChatCompletion.create(
model=model_id,
messages=messages
)
print(completion.choices[0].message.content)
