from revChatGPT.V1 import Chatbot
from decouple import config

ANSWER_OVER = 'over'
QUESTION_ONLY_OVER =  "阅读完下面的内容，不要回答其它内容,仅回答over。"
QUESTION_CONTINUE = "请继续你上面的回答，紧跟你上面回答的最后一个字。"
QUESTION_ADD_OVER = "根据我下面的要求，回答问题结束后告诉我over表述你作答完毕"
class Chatgpt:
    def __init__(self):
        # login in
        login_user = config('USER')
        login_password = config('PASSWORD')
        self.chatbot = Chatbot(config={  # chatgpt api
            "email": login_user,
            "password": login_password
        })
        print("Chatbot: ")
        # config
        self.output_text = ''  # 全部对话的结果

    # 判断一次回答有没有说完
    def judge_answer_over(self,response):
        return (response[-5:-1].lower() == 'over' or response[-4:].lower() == 'over') == False

   # 针对那种长结果，需要多次输出，也即是需要多次请求
    def ask_all_result(self,response,answer_over = True):
        this_prompt = ''
        if answer_over:
            this_prompt = QUESTION_CONTINUE + this_prompt
        index = 0
        while self.judge_answer_over(response) and answer_over: # 如果没有回答结束的话
            res = None
            for data in self.chatbot.ask(this_prompt):
                res = data["message"]
            response += res
            index += 1
            if index == 10:
                break
        return response

    # ask one question and receive the answer
    def ask_one_question(self, prompt, first=False,answer_over=True):
        response = None
        uuid = None
        if answer_over:
            prompt = QUESTION_ADD_OVER + prompt
        for data in self.chatbot.ask(prompt):
            response = data["message"]
        response = self.ask_all_result(response)
        if first:
            latest_uuid = self.chatbot.get_conversations(limit=1, offset=0)
            uuid = latest_uuid[0]['id']
        return response,uuid

    def give_background_info(self,prompt,first=True):
        prompt = QUESTION_ONLY_OVER +   prompt
        return self.ask_one_question(prompt,first=first,answer_over=False)

    def change_title(self, convo_id, title):
        self.chatbot.change_title(convo_id, title)

    def delete_one_conversation(self, convo_id: str):
        self.chatbot.delete_conversation(convo_id)

    def clear_conversations(self):
        self.chatbot.clear_conversations()
