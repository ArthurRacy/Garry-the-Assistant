import openai

def generate_chatgpt_response(input_text):
    openai.api_key = "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"

    prompt = f"{input_text}\nResposta:"
    
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.5,
    )

    return response.choices[0].text.strip()
