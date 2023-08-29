
from Scripts.tts.TtsMaker import TtsMaker
from Scripts.gpt.chatgpt import Chatgpt
from Scripts.textdeal.wordcmd import WriteWord


# chatgpt chat program
def test_chatgpt():
    chatgpt = Chatgpt()
    chatgpt.clear_conversations()  # clear all conversations
    answer, convo_id = chatgpt.ask_one_question("hello", True)
    print(answer)
    chatgpt.change_title(convo_id, "不知道,good")
    answer = chatgpt.ask_one_question("wonderful是什么意思？")


# test write words
def test_write_word():
    write_word = WriteWord()
    write_word.add_heading('test')
    write_word.add_paragragh('今天是个好日子')
    write_word.add_paragragh('今天下午比较清闲')
    write_word.add_paragragh('晚上跑步五公里！！')
    write_word.save_document('test')


def down_xiangshu():
    from Scripts.storydeal.DownXiangshu import DownXiangshu
    downxiangshu = DownXiangshu()
    story = downxiangshu.down_several_pages()
    write_word = WriteWord()
    write_word.add_paragragh(story)
    write_word.save_document('story')
    print("finished!!")


# Ttsmaker的网页来实现语音合成
def tts_maker():
    ttsmaker = TtsMaker()
    # ttsmaker.request_img()
    for i in range(100):
        ttsmaker.request_page()


def read_word():
    from Scripts.textdeal.wordcmd import ReadWord
    read_word = ReadWord()
    desttop_dir = r'C:\Users\Lenovo\Desktop\\'
    docx_locaiton = desttop_dir + "Input"
    read_word.open_word(docx_locaiton)
    # read_word.get_sections()
    paragraph = read_word.get_all_paragraphs()  # 返回word里面所有的文本

    return paragraph


def get_question_from_word():
    from Scripts.textdeal.wordcmd import ReadWord
    read_word = ReadWord()
    desttop_dir = r'C:\Users\Lenovo\Desktop\\'
    docx_locaiton = desttop_dir + "Input"
    read_word.open_word(docx_locaiton)
    # read_word.get_sections()
    read_word.distinguish_head_para()
    question = read_word.get_all_question()
    print('the number of the question is:{}'.format(len(question)))
    return question
    # print(question)


def answer_chatgpt_over():
    chatgpt = Chatgpt()
    paragraph = "你是谁，回答结束请回答over"
    answer, convo_id = chatgpt.ask_one_question(paragraph, True)
    print(answer)
    print(answer.endswith('over') or answer[-5:-1] == 'over')


def write_qiestion_pycharm():
    chatgpt = Chatgpt()
    # chatgpt.clear_conversations()  # clear all conversations
    paragraph = read_word()
    print(len(paragraph))
    answer, convo_id = chatgpt.give_background_info(paragraph, True)
    print('this is the first answer----------')
    print(answer)
    paragraph = '''
    新闻报告一般是图文结合类型，一段文字结合图片可以更好的帮助观众理解,注意图文的对应关系。
    你将我发的新闻按照原始文章的顺序将其分为三个段落，并对每一个段落进行配一张图，你需要详细一点描述每张图片的细节。我将利用stable diffusion进行图片生成。
    我希望你充当stable diffusion人工智能项目的提示词生成器。
        '''
    answer, _ = chatgpt.ask_one_question(paragraph)
    print(answer)

    chatgpt.change_title(convo_id, "testgpt")


def chat_docx():
    chatgpt = Chatgpt()
    questions = get_question_from_word()
    write_word = WriteWord()
    convo_id = None
    for index, question in enumerate(questions):
        if index == 0:
            answer, convo_id = chatgpt.give_background_info(question, True)
            write_word.add_heading('背景')
            write_word.add_paragragh(question)
        else:
            answer, _ = chatgpt.ask_one_question(question)
            write_word.add_heading(question)
            write_word.add_paragragh(answer)
        if index == (len(questions) - 1):
            print(answer)
    write_word.save_document('answer')
    chatgpt.change_title(convo_id, "chat_docx")

if __name__ == '__main__':
    # tts_maker()
    # test_write_word()

    # print()
    # main()
    chat_docx()
