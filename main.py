import os
import random
from dataclasses import dataclass
from tkinter import *
from tkinter import messagebox
from questionList import QuestionList, Question

root = Tk()
root.geometry("1000x700")
root.title("Симулятор Азарова: Підвал Авраменка")
root.iconphoto(False, PhotoImage(file=os.path.join("pictures", "mainIcon.png")))

dialogs = ("Ось ти й попався, Азіров!", 
           "Я ні Азіров, я Азаров!", 
           "Мені начхати, як тебе називати. Ти роками калічив українську мову,\nза що будеш сидіти в моєму підвалі.",
           "ААА, АВРАМЕНКО ВИПУСТИ МЕНЕ ЗВЄДСИ!",
           "Я тебе випущу, якщо ти складеш іспит з державної мови.\n Від кількости помилок залежатиме твоя доля."
           )
photos = (0, 1, 0, 2, 0)
dialog_index = 0
#план - 51 завдання на рід V, 20 на спрощення V, 20 на у/в V, 20 на і/й, 10 на е/и,
#20 на ь, 20 на апостроѳ, 10 на кптхѳ, 30 на велику букву й лапки, 30 складних іменників разом/деѳіс, 
# 10 не разом/окремо, 10 перенос (так/ні), ЛЕКСИКА (скільки зможу, буду також брати відео Максима Прудеуса)
# 10 ѳемінітивів, 3 (Ігорӧвич, Лазарӧвич, Якович), 10 звертань, ДРУЖНИЙ і ДРУЖНІЙ (4 приклади), природний, зворотний, додатний
# 5 на ступені порівняння (самий, більш -іший), 20 розписати числа буквами, 10 назвати час за цифровим записом, 10 збірні числівники, 
# 15 займенників разом/окремо/деѳіс, 20 кома при зворотах (10 дієприкм. 10 дієприсл.), 20 прислівники разом/окремо/деѳіс   
#20 - свобода, [15-19] слуга, [10-14] чіп, [5-9] розстріл, [1-4] на гілляку, 0 - мідний бик
selected_questions = []
question_number = 0
correct_answers = 0
selected_variant = IntVar() 
current_correct_answer = 0
current_explanation = ""
radiobuttons = []
def display_info():
    messagebox.showinfo("Про гру", "Автор: Шульга Роман\nВерсія: 1.0\nВихідний код: ")
def continue_dialog():
    global dialog_index
    dialog_index+=1
    if dialog_index >= len(dialogs):
        start_exam()
        return
    dialog_label.config(text=dialogs[dialog_index])
    match photos[dialog_index]:
        case 0:
            speaker_image_label.config(image=avramenko_image)
        case 1:
            speaker_image_label.config(image=azarov_image)
        case 2:
            speaker_image_label.config(image=azarov_angry)

def start_exam():
    speaker_image_label.config(image=azarov_reads)
    continue_button.place_forget() 
    global question_number_label 
    question_number_label = Label(text=str(question_number)+"/20", font=("Times New Roman", 20))
    question_number_label.place(relx=0.03, rely=0.1)
    global correct_answers_label
    correct_answers_label = Label(text="Правильних: "+str(correct_answers), fg="green", font=("Times New Roman", 20))
    correct_answers_label.place(relx=0.03, rely=0.15)
    question_list_object = QuestionList()
    questions = question_list_object.get_questions()
    for i in range(20):
        index = random.randint(0, len(questions)-1)
        random_question = questions[index]
        questions.pop(index)
        selected_questions.append(random_question)
    global answer_button
    answer_button = Button(text="⟶", font=("Times New Roman", 20), bg="white", command=answer)
    answer_button.place(relx=0.45, rely=0.9)
    load_question()

def load_question():
    selected_variant.set(0)
    for radiobutton in radiobuttons:
        radiobutton.pack_forget()
    radiobuttons.clear()
    global question_number
    question_number+=1
    if question_number > len(selected_questions):
        game_end()
        return
    question = selected_questions[question_number-1]
    dialog_label.config(text=question.question)
    question_number_label.config(text=str(question_number)+"/20")
    correct_answers_label.config(text="Правильних: "+str(correct_answers))
    iteration = 0
    for answer in question.answers:
        iteration+=1
        variant = Radiobutton(root, text=answer, font=("Times New Roman", 20), variable=selected_variant, value=iteration)
        radiobuttons.append(variant)
        variant.pack()
    global current_correct_answer 
    current_correct_answer = question.correct_answer
    global current_explanation
    current_explanation = question.explanation

def answer():
    if selected_variant.get() == 0:
        return
    elif current_correct_answer != selected_variant.get():
       messagebox.showerror("Неправильно!", current_explanation) 
    else:
        global correct_answers
        correct_answers+=1
    load_question()

def game_end():
    question_number_label.place_forget()
    answer_button.place_forget()
    if correct_answers >= 20:
        speaker_image_label.config(image=azarov_image)
        dialog_label.config(text="Ви вийшли на свободу!", fg="green")
    elif correct_answers >= 15:
        speaker_image_label.config(image=ending_housework)
        dialog_label.config(text="Авраменко зробив вас своїм слугою.")
    elif correct_answers >= 10:
        speaker_image_label.config(image=ending_chip)
        dialog_label.config(text="Бандерівці з біолабораторії вставили Азарову українізуючий чіп.")
    elif correct_answers >= 5:
        speaker_image_label.config(image=ending_shoot)
        dialog_label.config(text="Вас розстріляли.", fg="red")
    elif correct_answers >= 1:
        speaker_image_label.config(image=ending_hangman)
        dialog_label.config(text="Москаляку на гілляку!", fg="red")
    else:
        speaker_image_label.config(image=ending_bull)
        dialog_label.config(text="Ви відповіли на 0 запитань правильно.\n МІДНИЙ БИК", bg="red", fg="white")

dialog_label = Label(text=dialogs[0], font=("Times New Roman", 20))

avramenko_image = PhotoImage(file=os.path.join("pictures", "Avramenko.png"))
azarov_image = PhotoImage(file=os.path.join("pictures", "Azarov.png"))
azarov_angry = PhotoImage(file=os.path.join("pictures", "AzarovAngry.png"))
azarov_reads = PhotoImage(file=os.path.join("pictures", "AzarovReads.png"))
info_sign = PhotoImage(file=os.path.join("pictures", "infoButton.png"))
ending_housework = PhotoImage(file=os.path.join("pictures", "endingHousework.png"))
ending_chip = PhotoImage(file=os.path.join("pictures", "endingChip.png"))
ending_shoot = PhotoImage(file=os.path.join("pictures", "endingShoot.png"))
ending_hangman = PhotoImage(file=os.path.join("pictures", "endingHangman.png"))
ending_bull = PhotoImage(file=os.path.join("pictures", "endingBull.png"))

speaker_image_label = Label(root, image=avramenko_image)
continue_button = Button(text="⟶", font=("Times New Roman", 20), bg="white", command=continue_dialog)
info_button = Button(image=info_sign, command=display_info)
speaker_image_label.pack(pady=40)
dialog_label.pack(pady=30)
continue_button.place(relx=0.45, rely=0.80)
info_button.place(relx=0.9, rely=0.9)

#for debug
'''
def hack_score():
    global correct_answers
    correct_answers = int(score_entry.get())
    print(score_entry.get())
instant_end_button = Button(text="Миттєво закінчити", command=game_end)
score_entry = Entry()
hack_score_button = Button(text="Змінити рахунок", command=hack_score)
instant_end_button.place(relx=0.1, rely=0.8)
score_entry.place(relx=0.1, rely=0.9)
hack_score_button.place(relx=0.1, rely=0.95)
'''
root.mainloop()
