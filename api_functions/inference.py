from ollama import chat
from ollama import ChatResponse

def predict(question: str) -> str:

    resposne: ChatResponse = chat(
        model='llama3.2', messages=[
        {
            'role': 'user',
            'content': question,
        },
    ])

    return resposne.message.content