from openai import OpenAI
class ChatGPT:
    def __init__(self):
        self.client = OpenAI( api_key="")

    def Recommendation(self, info):
        if(len(info) == 0):
            return "you have no tasks"
        else:
            task_str = ""
            for counter, task in enumerate(info, start=1):
                task_str += f"Task {counter} - Title: {task[2]}, Description: {task[3]}\n"
            completion = self.client.chat.completions.create(
            model="gpt-4o-mini",
            store=True,
            messages=[
                    {"role": "user", "content": "which are the next 3 task I should complete" + task_str}
                ]
            )
            temp = completion.choices[0].message.content
            #substring the response
            start_index = temp.find("\n")
            end_index = temp.rfind("\n")
            temp = temp[start_index:end_index]
            print(temp)
            return temp #f"{task_1_block} {task_2_block} {task_3_block}"
