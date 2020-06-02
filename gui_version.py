from tkinter import *
from parse_file import add_in
import json, requests, webbrowser
from bypy import ByPy

root = Tk()

def OpenUrl(url):
    webbrowser.open_new(url)

def cp(content, window):
    window.clipboard_clear()
    window.clipboard_append(content)

def search_answer(content, qa_dict):
    question = ""
    is_choice = False
    choices = {}
    if "A" in content:
        is_choice = True
        letter_list = ["A", "B", "C", "D", "E", "F", "G"]
        previous_pos = -1
        for (i, letter) in enumerate(letter_list):
            potential_answer = ""
            pos = content.find(letter, 0)
            if pos == -1:
                potential_answer = content[previous_pos + 1:]
            else:
                potential_answer = content[previous_pos + 1: pos]
            previous_pos = pos
            potential_answer = potential_answer.replace("\n", "")
            if letter == "A":
                question = potential_answer
            else:
                choices[potential_answer] = letter_list[i - 1]
            if previous_pos == -1:
                break
    else:
        question = content.replace("\n", "")

    top_answer = Toplevel()
    top_answer.title("答案")
    question = question.replace("纠错", "")
    if question in qa_dict:
        if is_choice == False:
            text_answer = Text(top_answer)
            text_answer.insert(1.0, f"问题：“{question}“\n\n\n\n答案：" + qa_dict[question])
            text_answer.grid(row = 0, column = 0)
            btn_quitAnswer = Button(top_answer, text="复制答案", command=lambda: cp(qa_dict[question], top_answer)).grid(row=1, column=0)
            btn_quitAnswer = Button(top_answer, text="关闭", command=top_answer.destroy)
            btn_quitAnswer.grid(row=2, column=0)
        else:
            answers = qa_dict[question].split("/")
            correct_answer = ""
            try:
                for answer in answers:
                    if answer == "":
                        continue
                    correct_answer += choices[answer] + ","
                correct_answer = correct_answer[:-1]
            except KeyError as e:
                correct_answer = f"由于格式原因无法为您自动选择对应选项，请自行比照正确答案选择对应选项。正确答案如下\n{answers}"
            label0 = Label(top_answer, text = f"问题：“{question}“\n\n答案：" + correct_answer).grid(row = 0, column = 0)
            btn_quitAnswer = Button(top_answer, text="关闭", command=top_answer.destroy).grid(row = 1, column = 0)
            

    else:
        fakeua = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36"}
        searchPage = requests.get('https://www.baidu.com/s?wd=' + question, headers = fakeua)
        labelBaiduAnswerFound = Label(top_answer, text = f"问题: “{question}”\n不在题库中，已为您百度，请点击“跳转”用浏览器查看结果")
        labelBaiduAnswerFound.grid(row = 0, column = 0)
        jumpBtn = Button(top_answer, text="跳转", command=lambda: OpenUrl(searchPage.url))
        jumpBtn.grid(row = 1, column = 0)
        btn_quitBaiduAnswer = Button(top_answer, text="关闭", command=top_answer.destroy)
        btn_quitBaiduAnswer.grid(row = 2, column = 0)

def ModifyAnswer(answer, question, qa_dict):
    qa_dict[question] = answer
    topModified = Toplevel()
    topModified.title("修改成功")
    label1 = Label(topModified, text = "修改成功！").grid(row = 0, column = 0)
    btnQuitModified = Button(topModified, text="关闭", command=topModified.destroy)
    btnQuitModified.grid(row = 1, column = 0)

def SeachModifyAnswer(question, qa_dict):
    question = question.replace("\n", "")
    top_answer = Toplevel()
    top_answer.title("修改")
    if question in qa_dict:
        label1 = Label(top_answer, text = f"当前问题答案为: {qa_dict[question]}，请录入要修改的答案:").grid(row = 0, column = 0)
        e = Entry(top_answer, width=35, borderwidth=5)
        e.grid(row=1, column=0, columnspan=3, padx=10, pady=10)
        btnModify = Button(top_answer, text="修改", command=lambda: ModifyAnswer(e.get(), question, qa_dict)).grid(row=2, column=0)
        btnQuitModify = Button(top_answer, text="关闭", command=top_answer.destroy)
        btnQuitModify.grid(row = 3, column = 0)

def clear_entry(e):
    e.delete(0, 'end')    

def start(mode):
    top = Toplevel()
    top.title(mode + "模式")
    with open("qa_dict_auto_final.json") as f:
        qa_dict = json.load(f)
        # label0 = Label(top, text = f"当前题库存题{len(qa_dict)}道").grid(row = 0, column = 0)
        label1 = Label(top, text = f"当前题库存题{len(qa_dict)}道, 请输入问题全文:")
        label1.grid(row=1, column=0)
        e = Entry(top, width=35, borderwidth=5)
        e.grid(row=2, column=0, columnspan=3, padx=10, pady=10)
        if mode == "答题":
            btn_search = Button(top, text="搜索", command=lambda: search_answer(e.get(), qa_dict)).grid(row=3, column=0)
        else:
            btn_search = Button(top, text="搜索", command=lambda: SeachModifyAnswer(e.get(), qa_dict)).grid(row=3, column=0)
        
        btn_clear = Button(top, text="清除", command=lambda: clear_entry(e)).grid(row = 2, column = 3)
        btn_start = Button(top, text="关闭", command=top.destroy)
        btn_start.grid(row = 4, column = 0)

def add():
    top_add = Toplevel()
    top_add.title("录入模式")
    open("text.txt", "w").close()
    webbrowser.open("text.txt")
    label1 = Label(top_add, text = "进入录入模式，请将解析页面复制粘贴入text.txt文件，若已完成，请单击“开始录入”").grid(row = 0, column = 0)
    btnStartAdd = Button(top_add, text="开始录入", command=lambda: add_in(top_add)).grid(row=1, column=0)
    btnQuirAdd = Button(top_add, text="关闭", command=top_add.destroy).grid(row=2, column=0)

def sycup():
    bp=ByPy()
    bp.upload("qa_dict_auto_final.json")
    top_syc = Toplevel()
    label0 = Label(top_syc, text = "同步完成！").grid(row = 0, column = 0)
    btnQuirSyc = Button(top_syc, text="关闭", command=top_syc.destroy).grid(row=1, column=0)

def sycdown():
    bp=ByPy()
    bp.download("qa_dict_auto_final.json")
    top_syc = Toplevel()
    label0 = Label(top_syc, text = "同步完成！").grid(row = 0, column = 0)
    btnQuirSyc = Button(top_syc, text="关闭", command=top_syc.destroy).grid(row=1, column=0)

label1 = Label(root, text = f"欢迎使用自动答题机！请选择以下模式进入：").grid(row = 0, column = 0)
btn_start = Button(root, text="答题模式", command=lambda: start("答题")).grid(row=1, column=0)
btn_start = Button(root, text="修改模式", command=lambda: start("修改")).grid(row=2, column=0)
btn_start = Button(root, text="录入模式", command=lambda: add()).grid(row=3, column=0)
btn_loc2clo = Button(root, text="同步本地到云端", command=lambda: sycup()).grid(row=4, column=0)
btn_clo2loc = Button(root, text="同步云端到本地", command=lambda: sycdown()).grid(row=5, column=0)
button_quit = Button(root, text="退出", command=root.quit).grid(row = 6, column = 0)
mainloop()