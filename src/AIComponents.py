import os
from dotenv import load_dotenv
from openai import OpenAI
class ChatGPT:
    def __init__(self):
        load_dotenv() #loads things from env file
        self.client = OpenAI( api_key= os.getenv("OPENAI_API_KEY"))#pulls API key from env file
    def Recommendation(self, info):
        if(len(info) == 0): #no task associtated with users
            return "you have no tasks"
        else:
            task_str = ""
            for counter, task in enumerate(info, start=1): #combines all tasks from the users into one string
                task_str += f"Task {counter} - Title: {task[2]}, Description: {task[3]}\n"
            completion = self.client.chat.completions.create(
            model="gpt-4o-mini", #uses chat gpt 4
            store=True,
            messages=[
                    {"role": "user", "content": "which are the next 3 task I should complete" + task_str} #the message sent to the ai model
                ]
            )
            temp = completion.choices[0].message.content # AI response
            #substring the response
            start_index = temp.find("\n")
            end_index = temp.rfind("\n")
            temp = temp[start_index:end_index]#cut out the end and begining parts of the AI response
            print(temp)
            return temp # return AI Response


