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
    elif message.text == '/start':
        bot.send_message(message.from_user.id, "Список доступных команд:\n/generate - генерирует персонажа\n"
                                               "/roll20 - бросок 20 с бонусом или без\n"
                                               "/rollChara - генерирует только характеристики персонажа\n"
                                               "/StalkerShots - выстрел очередью по системе сталкера\n"
                                               "/RollPersonalItems - Рандомные личные предметы")
    elif message.text == '/help':
        bot.send_message(message.from_user.id, "Список доступных команд:\n/generate - генерирует персонажа\n"
                                               "/roll20 - бросок 20 с бонусом или без\n"
                                               "/rollChara - генерирует только характеристики персонажа\n"
                                               "/StalkerShots - выстрел очередью по системе сталкера\n"
                                               "/RollPersonalItems - Рандомные личные предметы")
    elif message.text == '/roll20':
        bot.send_message(message.from_user.id, "Укажите бонус (Только число)")
        bot.register_next_step_handler(message, roll_dice)
    elif message.text == '/rollChara':
        ch = Character()
        ch.generate()
        text = ch.chara()
        bot.send_message(message.from_user.id, text)
    elif message.text == '/StalkerShots':
        bot.send_message(message.from_user.id, "Укажите количество пуль (Только число)")
        bot.register_next_step_handler(message, stalker_shot)
    elif message.text == '/RollPersonalItems':
        bot.send_message(message.from_user.id, "Укажите количество предметов (Только число)")
        bot.register_next_step_handler(message, print_personal_items)
    else:
        bot.send_message(message.from_user.id, "Беринг чмо! Некорректный ввод, /help список доступных команд")


def print_personal_items(message):
    rolls = message.text
    stroka = ''
    summa_weight = 0
    summa_volume = 0
    for i in range(int(rolls)):
        items_list = roll_item()
        print(items_list)
        stroka += f'Предмет: {items_list[1]} Вес: {items_list[2]} Объем: {items_list[3]} \n'
        print(items_list[2].split())
        summa_weight += float(items_list[2].split()[0])
        summa_volume += float(items_list[2].split()[0])
    print(stroka)
    text = stroka.split(maxsplit=1)[1]
    print(text)
    if len(text) > 4096:
        for x in range(0, len(text), 4096):
            bot.send_message(message.chat.id, '{}'.format(text[x:x + 4096]))
            print(x)
    else:
        bot.send_message(message.from_user.id, stroka)
    bot.send_message(message.from_user.id, f'Суммарный вес: {summa_weight} кг Cуммарный Объем: {summa_volume} кг')
    print(summa_weight)
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

def roll_dice(message):
    try:
        bonus = int(message.text)
        bot.send_message(message.from_user.id, f'Результат с бонусом:{randint(1, 20) + bonus} \n Результат без бонуса:{randint(1, 20)}')

    except Exception:
        bot.send_message(message.from_user.id, 'Числами, пожалуйста')

def stalker_shot(message):
    shot_dictionary = {'Левая рука': False, 'Правая рука': False, 'Тело': False, 'Левая нога': False, 'Правая нога': False, 'Голова': False}
    try:
        shots = int(message.text)
        if 1 <= shots <= 1000:
            count = 0
            if shots > 1:
                for i in range(shots):
                    n = randint(1, 2)
                    if n == 2:
                        count += 1
                for i in range(count):
                    n = randint(1, 20)
                    if 1 <= n <= 4:
                        n = randint(1, 2)
                        if n == 1:
                            if shot_dictionary['Левая рука']:
                                shot_dictionary['Левая рука'] += 1
                            else:
                                shot_dictionary['Левая рука'] = 1
                        if n == 2:
                            if shot_dictionary['Правая рука']:
                                shot_dictionary['Правая рука'] += 1
                            else:
                                shot_dictionary['Правая рука'] = 1
                    elif 5 <= n <= 9:
                        n = randint(1, 2)
                        if n == 1:
                            if shot_dictionary['Левая нога']:
                                shot_dictionary['Левая нога'] += 1
                            else:
                                shot_dictionary['Левая нога'] = 1
                        if n == 2:
                            if shot_dictionary['Правая нога']:
                                shot_dictionary['Правая нога'] += 1
                            else:
                                shot_dictionary['Правая нога'] = 1
                    elif 10 <= n <= 16:
                        if shot_dictionary['Тело']:
                            shot_dictionary['Тело'] += 1
                        else:
                            shot_dictionary['Тело'] = 1
                    elif 16 <= n <= 20:
                        if shot_dictionary['Голова']:
                            shot_dictionary['Голова'] += 1
                        else:
                            shot_dictionary['Голова'] = 1
            elif shots == 1:
                n = randint(1, 20)
                if 1 <= n <= 4:
                    n = randint(1, 2)
                    if n == 1:
                        if shot_dictionary['Левая рука']:
                            shot_dictionary['Левая рука'] += 1
                        else:
                            shot_dictionary['Левая рука'] = 1
                    if n == 2:
                        if shot_dictionary['Правая рука']:
                            shot_dictionary['Правая рука'] += 1
                        else:
                            shot_dictionary['Правая рука'] = 1
                elif 5 <= n <= 9:
                    n = randint(1, 2)
                    if n == 1:
                        if shot_dictionary['Левая нога']:
                            shot_dictionary['Левая нога'] += 1
                        else:
                            shot_dictionary['Левая нога'] = 1
                    if n == 2:
                        if shot_dictionary['Правая нога']:
                            shot_dictionary['Правая нога'] += 1
                        else:
                            shot_dictionary['Правая нога'] = 1
                elif 10 <= n <= 16:
                    if shot_dictionary['Тело']:
                        shot_dictionary['Тело'] += 1
                    else:
                        shot_dictionary['Тело'] = 1
                elif 16 <= n <= 20:
                    if shot_dictionary['Голова']:
                        shot_dictionary['Голова'] += 1
                    else:
                        shot_dictionary['Голова'] = 1
            print(count)
            print(shot_dictionary)
            stroka = ''
            if shot_dictionary != {}:
                for el in shot_dictionary.items():
                    print(el)
                    if el[1] != False:
                        stroka += f'{el[0]}: {str(el[1])} \n'
            else:
                stroka = 'Отсутвуют'

            print(stroka)
            if stroka != '':
                stroka = 'Попадания:\n' + stroka
            else:
                stroka = 'Попадания отсутствуют'
            bot.send_message(message.from_user.id, stroka)
        else:
            bot.send_message(message.from_user.id, 'Введите число от 1 до 1000')

    except Exception:
        bot.send_message(message.from_user.id, 'Цифрами, пожалуйста')

def roll_item():
    item_roll = randint(1, 19)
    item = cur.execute("""SELECT * FROM Personal_items
                        WHERE id = ?""", (item_roll,)).fetchall()[0]
    return item

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

    def chara(self):
        return f'Сила: {self.st} \n Ловкость: {self.dex} \n Интеллект: {self.int} \n Харизма: {self.cha} \n Мудрость: {self.wis} \n Телосложение: {self.con}'

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