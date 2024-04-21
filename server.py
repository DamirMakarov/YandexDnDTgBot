import telebot
from telebot import types
bot = telebot.TeleBot('7081308465:AAG5GBexiomM6zuN9PK7xgv5-mkoKy0yFXc')
from random import randint, choice
from heapq import nlargest
import sqlite3


con = sqlite3.connect('dnd_bot_database.db', check_same_thread=False)
cur = con.cursor()

def randomch():
    num = sum(nlargest(3, [randint(1, 6), randint(1, 6),
                           randint(1, 6), randint(1, 6)]))
    return str(num)




@bot.message_handler(content_types=['text'])
def start(message):
    if message.text == '/generate':
        bot.send_message(message.from_user.id, "Введите имя персонажа")
        bot.register_next_step_handler(message, print_ch)
    elif message.text == '/help':
        bot.send_message(message.from_user.id, "Список доступных команд:\n/generate - генерирует персонажа")
    else:
        bot.send_message(message.from_user.id, "Беринг чмо! Некорректный ввод, /help список доступных команд")


def print_ch(message):
    ch = Character()
    ch.generate()
    name = message.text
    text = ch.print_pers(name)
    text = text.split(maxsplit=1)[1]
    print(text)
    if len(text) > 4096:
        for x in range(0, len(text), 4096):
            bot.send_message(message.chat.id, '{}'.format(text[x:x + 4096]))
            print(x)


class Character():
    def __init__(self, *arg):
        self.st = '-'
        self.load_name = arg
        self.dex = '-'
        self.int = '-'
        self.cha = '-'
        self.wis = '-'
        self.con = '-'
        self.back = ''
        self.back_name = '-'
        self.back_roll = 0
        self.cclass = ''
        self.cclass_roll = 0
        self.ski = ''
        self.feat = ''
        self.tra = ''
        self.bon = ''
        self.inv = ''
        self.cla_ski = ''
        self.hp = ''
        self.hp_dice = ''
        self.ini = ''
        self.ra = ''
        self.race_roll = ''
        self.spe = ''
        self.pas = ''
        self.save_name = 'Введите имя персонажа'

    def generate(self):
        self.ski = ''

        self.st = randomch()
        self.dex = randomch()
        self.int = randomch()
        self.cha = randomch()
        self.wis = randomch()
        self.con = randomch()

        self.cclass_roll = randint(1, 3)
        self.race_roll = randint(1, 6)
        self.back_roll = randint(1, 14)

        self.back = cur.execute("""SELECT background FROM backgrounds
                     WHERE id = ?""", (self.back_roll,)).fetchall()[0][0]
        self.back_name = cur.execute("""SELECT title FROM backgrounds
                             WHERE id = ?""", (self.back_roll,)).fetchall()[0][0]
        self.ra = cur.execute("""SELECT title FROM races
                                     WHERE id = ?""", (self.race_roll,)).fetchall()[0][0]
        self.ski = cur.execute("""SELECT skills FROM backgrounds
             WHERE id = ?""", (self.back_roll,)).fetchall()[0][0]
        self.cclass = cur.execute("""SELECT title FROM classes
                     WHERE id = ?""", (self.cclass_roll,)).fetchall()[0][0]

        self.feat = (cur.execute("""SELECT features FROM classes
                     WHERE id = ?""", (self.cclass_roll,)).fetchall()[0][0] +
                     cur.execute("""SELECT features FROM races
                     WHERE id = ?""", (self.race_roll,)).fetchall()[0][0])

        self.tra = (cur.execute("""SELECT traits FROM classes
                    WHERE id = ?""", (self.cclass_roll,)).fetchall()[0][0] +
                    cur.execute("""SELECT traits FROM races
                    WHERE id = ?""", (self.race_roll,)).fetchall()[0][0])

        self.spe = cur.execute("""SELECT speed FROM races
                                             WHERE id = ?""", (self.race_roll,)).fetchall()[0][0]

        self.inv = cur.execute("""SELECT inventory FROM classes
                             WHERE id = ?""", (self.cclass_roll,)).fetchall()[0][0]
        self.cla_ski = cur.execute("""SELECT inventory FROM classes
                                     WHERE id = ?""", (self.cclass_roll,)).fetchall()
        self.ski += ', ' + self.skill_choice() + '.'

        self.hp = cur.execute("""SELECT hit FROM classes
                                     WHERE id = ?""", (self.cclass_roll,)).fetchall()[0][0]
        self.hp_dice = cur.execute("""SELECT hitdice FROM classes
                                             WHERE id = ?""", (self.cclass_roll,)).fetchall()[0][0]
        self.race_ch_plus()

        self.hp = int(self.hp) + (int(self.con) - 10) // 2
        self.ini = (int(self.dex) - 10) // 2
        self.pas = str(10 + (int(self.wis) - 10) // 2)

    def print_pers(self, name):
        return f'Имя: {name}\n \n Сила: {self.st} \n Ловкость: {self.dex} \n Интеллект: {self.int} \n Харизма: {self.cha} \n Мудрость: {self.wis} \n Телосложение: {self.con} \n \n Класс: {self.cclass} \n Раса: {self.ra} \n \n Предыстория: {self.back_name} \n \n {self.back} \n \n Навыки: {self.ski} \n Владения: {self.feat} \n \n Умения: {self.tra} \n\n \n Бонус мастерства: {self.bon} \n Хиты: {self.hp} \nКость хитов: {self.hp_dice} \n Инициатива: {self.ini} \n Скорость: {self.spe} \n Пассивная внимательность: {self.pas} \n \n Снаряжение: {self.inv} \n'

    def skill_choice(self):
        class_skill = cur.execute("""SELECT skills FROM classes
                                                WHERE id = ?""", (self.cclass_roll,)).fetchall()
        class_dict = {1: 2, 2: 4, 3: 2}

        list_of_skills_ski = self.ski.split(', ')
        list_of_skills = list()
        while len(list_of_skills) != class_dict[int(self.cclass_roll)]:
            random_skill = choice(class_skill[0][0].split(', '))
            if random_skill not in list_of_skills and random_skill not in list_of_skills_ski:
                list_of_skills.append(random_skill)

        list_of_skills = ', '.join(list_of_skills)
        return list_of_skills

    def race_ch_plus(self):

        bonus_ch = cur.execute("""SELECT bonus_ch FROM races
                                WHERE id = ?""", (self.race_roll,)).fetchall()[0][0]
        bonus_ch = bonus_ch.split()

        for el in bonus_ch:
            if el in bonus_ch:
                if el[:2] == 'st':
                    self.st = str(int(self.st) + int(el[2]))
                elif el[:3] == 'dex':
                    self.dex = str(int(self.dex) + int(el[3]))
                elif el[:3] == 'int':
                    self.int = str(int(self.int) + int(el[3]))
                elif el[:3] == 'cha':
                    self.cha = str(int(self.cha) + int(el[3]))
                elif el[:3] == 'wis':
                    self.wis = str(int(self.wis) + int(el[3]))
                elif el[:3] == 'con':
                    self.con = str(int(self.con) + int(el[3]))



bot.polling(none_stop=True, interval=0)