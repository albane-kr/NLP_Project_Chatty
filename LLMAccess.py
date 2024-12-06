import openai

# # Set your OpenAI API key
# openai.api_key = 'your-api-key'

# def generate_response(prompt):
    # response = openai.Completion.create(
        # engine="gpt2",  # You can use other engines like "gpt-3.5-turbo"
        # prompt=prompt,
        # max_tokens=150,
        # n=1,
        # stop=None,
        # temperature=0.7
    # )
    # return response.choices[0].text.strip()

# # # Example usage
# # user_input = "I'm feeling really down today. Can you help me?"
# # response = generate_response(user_input)
# # print("Chatbot:", response)

import google.generativeai as genai

genai.configure(api_key="AIzaSyD3LYSrWFEEKt6cMEmmqxzko37_--qnWow")
model = genai.GenerativeModel("gemini-1.5-flash")
def generate_response(prompt):
    response = model.generate_content("Explain how AI works")
    return response.text
    