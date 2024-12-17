import google.generativeai as genai

# INSERT YOUR API KEY BELOW
genai.configure(api_key="AIzaSyD3LYSrWFEEKt6cMEmmqxzko37_--qnWow")
model = genai.GenerativeModel("gemini-1.5-flash")
def generate_response(prompt: str, emotion: str) -> str:
    """
    @param prompt: str -> This parameter is the textual user input (or transscribed audio)
    @param emotion: str -> This parameter is the emotion detected either in text or speech

    @return: str -> The return value of this function is the textual response of the LLM for 
    the user.

    Description: This function takes the user input, adds the some part between the | and then returns the textual response. 
    The length of this is limitted to 10-30 words, to not significantly impact performance by too long responses.
    """
    response = model.generate_content(prompt + f" | request: keep the answer between 10 and 30 words! | Take into account that user is in emotion {emotion}")
    print(response)
    return response.text
    