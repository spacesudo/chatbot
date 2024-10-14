from dotenv import load_dotenv
import os
import openai

load_dotenv()

openai_api_key = os.getenv('OPENAI')

def chatbot(prompt):
    openai.api_key = openai_api_key
    
    messages = [
        {
            'role' : 'system',
            'content' : "you are a doctor only and you only answer health questions"
        }
    ]
    
    if prompt:
        messages.append(
            {
                "role" : "user",
                "content" : prompt
            },
        )
        
        chat = openai.chat.completions.create(model='gpt-4o-mini', messages=messages)
        
        reply = chat.choices[0].message.content
        
        #print(reply)
        
        messages.append(
            {
                "role" : "assistant",
                "content" : reply
            }
        )
        
        return reply


if __name__ == "__main__":
    chatbot('what are the symptoms of aids')


