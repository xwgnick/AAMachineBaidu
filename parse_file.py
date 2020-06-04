import json
from tkinter import *
from tqdm import tqdm
from bypy import ByPy

def add_in(top_add):
    # with open("text.txt", 'r', encoding='UTF-8') as org, open("text_clean.txt", "w") as cleaned:
    #     content = org.readlines()
    #     for i, element in tqdm(enumerate(content)):
    #         if element in ["A\n", "B\n", "C\n", "D\n", "E\n"]:
    #             cleaned.write(element[:-1])
    #         else:
    #             cleaned.write(element)

    num_repeted = 0
    with open("text.txt") as f:
        with open("qa_dict_auto_final.json") as f_qa_dict:
            content = f.readlines()
            qa_dict_auto = json.load(f_qa_dict)
            question = ""
            answers = {}
            correct_answer_ind = []
            correct_answer = ""
            for element in tqdm(content):
                if element[0] == "第" and element[-2] == "错":
                    if question != "":
                        qa_dict_auto[question] = correct_answer
                
                    question = ""
                    answers = {}
                    correct_answer_ind = []
                    correct_answer = ""

                    porsition_A = element.find("A")
                    if porsition_A != -1:
                        if element[porsition_A + 1] == "错":
                            answers["A"] = "错误"
                            answers["B"] = "正确"
                        else:
                            answers["B"] = "错误"
                            answers["A"] = "错误"
                    
                else:
                    if element[0] in ["A", "B", "C", "D", "E"]:
                        if len(element) == 0:
                            print(f"!!!!!!!!!!! wron at question{question}!")
                        answers[element[0]] = element[1:-1]
                    
                    elif "正确答案" in element:
                        element = element[:-1]
                        if "A" in element or "B" in element or "C" in element or "D" in element or "E" in element:
                            correct_answer_ind = element[7:].split(",")
                            if len(correct_answer_ind) > 1:
                                for index in correct_answer_ind:
                                    correct_answer += (answers[index] + "/")
                            else:
                                    correct_answer = answers[correct_answer_ind[0]]
                        
                        else:
                            correct_answer = element[7:]


                    # elif "答题结果" in element or "选项得分" in element or element == "\n" or element in ["1\n", "2\n", "3\n", "4\n", "5\n", "6\n"]:
                    #     continue
                
                    else:
                        if question != "":
                            continue
                        question = element[:-1]
                        if question in qa_dict_auto:
                            num_repeted += 1


    # print("qa_dict_auto", qa_dict_auto)
    qa_dict_auto[question] = correct_answer
    print(f"批量添加完成！目前题库共有题{len(qa_dict_auto)}道!扫描到重复题目{num_repeted}道！")
    dumped = json.dumps(qa_dict_auto)
    f = open("qa_dict_auto_final.json","w")
    f.write(dumped)
    f.close()
    top_add_succ = Toplevel()
    top_add_succ.title("录入成功")
    label0 = Label(top_add_succ, text = f"批量录入完成！目前题库共有题{len(qa_dict_auto)}道!扫描到重复题目{num_repeted}道!").grid(row = 0, column = 0)
    btn_quitAnswer = Button(top_add_succ, text="关闭", command=top_add_succ.destroy).grid(row=1, column=0)
    # # while line:
    # #     print(line)
    # #     line = f.readline