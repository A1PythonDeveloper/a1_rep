import telebot
import random
from telebot import types
from telebot.types import InlineKeyboardButton

token = 'token'
bot = telebot.TeleBot(token)

player_start = {
    'HP': 100,
    'Max HP': 100,
    'Points': 0,
    'Rounds': 3,
    'Max rounds': 3,
    'Damage': 20,
    'current_level': 1,
    'in_battle': False
}
enemies = [
    {'name': "Slave", 'HP': 50, 'Damage': 20},
    {'name': "Грязный Богдан", 'HP': 75, 'Damage': 30},
    {'name': "Никита", 'HP': 75, 'Damage': 50},
    {'name': "ЧЕРНЫЙ МЕМЧИК", 'HP': 100, 'Damage': 52},
    {'name': "ГЕЙб", 'HP': 120, 'Damage': 60}
]

users = {}


@bot.message_handler(commands=['start'])
def  start_message(message):
    show_main_menu(message.chat.id)


def show_main_menu(chat_id):
    markup = types.InlineKeyboardMarkup(row_width=1)
    is_active_game = False
    if chat_id in users:
        player_data = users[chat_id]
        if player_data.get('current_level') <= 5:
            is_active_game = True

    if is_active_game:
        item_continue = InlineKeyboardButton('Продолжить мучения', callback_data='continue_game')
        markup.add(item_continue)

    item_new = InlineKeyboardButton('Начать мучения', callback_data='new_game')
    item_rules = InlineKeyboardButton('Правила бойцовского клуба', callback_data='show_rules')
    item_exit = InlineKeyboardButton('Сдаться', callback_data='exit_game')
    markup.add(item_new, item_rules, item_exit)

    bot.send_message(chat_id, 'Добро пожаловать в GDungeon!', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    chat_id = call.message.chat.id

    try:
        bot.answer_callback_query(call.id)

        if call.data == 'new_game':
            start_new_game(chat_id)
        elif call.data == 'continue_game':
            continue_game(chat_id)
        elif call.data == 'show_rules':
            show_rules(chat_id)
        elif call.data == 'exit_game':
            bot.send_message(chat_id,'Sosik')
        elif call.data == 'battle_attack':
            handle_battle_action(chat_id, 'attack')
        elif call.data == 'battle_reload':
            handle_battle_action(chat_id, 'reload')

        elif call.data == 'shop_hp':
            handle_shop(chat_id, 'hp')
        elif call.data == 'shop_damage':
            handle_shop(chat_id, 'damage')
        elif call.data == 'shop_rounds':
            handle_shop(chat_id, 'rounds')
        elif call.data == 'shop_skip':
            handle_shop(chat_id, 'skip')

        elif call.data == 'back_to_menu':
            show_main_menu(chat_id)

    except Exception as err:
        print(err)
        show_main_menu(chat_id)

def start_new_game(chat_id):
    users[chat_id] = player_start.copy()
    users[chat_id]['current_level'] = 1
    print(f"Новая игра для {chat_id}. Уровень: {users[chat_id]['current_level']}")
    start_battle(chat_id)


def continue_game(chat_id):
    if chat_id in users:
        player_data = users[chat_id]
        if player_data['current_level'] <= 5:
            if player_data.get('in_battle', False):
                show_battle_screen(chat_id)
            else:
                start_battle(chat_id)
        else:
            bot.send_message(chat_id, 'Подземелье пройдено, ебашь заново')
            show_main_menu(chat_id)
    else:
        bot.send_message(chat_id, 'Тебя нет в подземелье, пиздуй в начало')
        show_main_menu(chat_id)


def start_battle(chat_id):
    player_data = users[chat_id]
    player_data['HP'] = player_data['Max HP']
    player_data['Rounds'] = player_data['Max rounds']
    player_data['in_battle'] = True
    current_level = player_data['current_level']
    enemy = enemies[current_level - 1].copy()
    users[chat_id]['current_enemy'] = enemy
    print(f'{chat_id} начал бой лвл {player_data['current_level']}')
    show_battle_screen(chat_id)


def show_battle_screen(chat_id):
    player_data = users[chat_id]
    enemy = users[chat_id]['current_enemy']

    battle_text = (
        f'Уровень {player_data['current_level']}: {enemy['name']}\n\n'
        f'Ты:\n'
        f'HP: {player_data['HP']}\n'
        f'Пульки: {player_data['Rounds']}\n'
        f'Дамаг: {player_data['Damage']}\n'
        f'{enemy['name']}\n'
        f'HP: {enemy['HP']}'
    )
    markup = types.InlineKeyboardMarkup(row_width=2)

    if player_data['Rounds'] > 0:
        attack_button = types.InlineKeyboardButton('Выстрелить в уебка', callback_data='battle_attack')
    else:
        attack_button = types.InlineKeyboardButton('Маслины кончились', callback_data='battle_attack')

    reload_button = types.InlineKeyboardButton('Докинуть пульки', callback_data='battle_reload')
    markup.add(attack_button, reload_button)

    if 'last_message_id' in users[chat_id]:
        try:
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=users[chat_id]['last_message_id'],
                text=battle_text,
                reply_markup=markup
            )
            return
        except:
            pass

    sent = bot.send_message(chat_id, battle_text, reply_markup=markup)
    users[chat_id]['last_message_id'] = sent.message_id


def handle_battle_action(chat_id, action):
    player_data = users[chat_id]
    enemy = users[chat_id]['current_enemy']
    result_message = ''

    if action == 'attack' and player_data['Rounds'] > 0:
        damage = random.randint(player_data['Damage'] - 5, player_data['Damage'] + 7)
        enemy['HP'] -= damage
        player_data['Rounds'] -= 1
        result_message = f'{enemy['name']} лишился дев... {damage} HP!'
    elif action == 'reload':
        result_message = 'Перезарядка...'
        player_data['Rounds'] = player_data['Max rounds']

    if enemy['HP'] <= 0:
        win_text = f'{enemy['name']} пал под твоим натиском'
        player_data['Points'] += 1
        player_data['in_battle'] = False
        if player_data['current_level'] < 5:
            bot.send_message(chat_id, win_text)
            show_shop(chat_id)
        else:
            print(f'{chat_id} прошёл игру')
            bot.send_message(chat_id, 'Поздравляю, ты прошёл эту помойку'
                                      '(приложи балумбу к экрану)')
            del users[chat_id]
            show_main_menu(chat_id)
        return

    if enemy['HP'] > 0:
        enemy_damage = random.randint(enemy['Damage'] - 7, enemy['Damage'] + 5)
        player_data['HP'] -= enemy_damage
        result_message = f'{enemy['name']} нанес тебе {enemy_damage} ударов по жопе'

    if player_data['HP'] <= 0:
        print(f'{chat_id} проиграл на лвле {player_data['current_level']}')
        bot.send_message(chat_id, f'{enemy['name']} присвоил твое очко. Конец игры!')
        del users[chat_id]
        show_main_menu(chat_id)
        return

    if result_message:
        bot.send_message(chat_id, result_message)

    show_battle_screen(chat_id)


def show_shop(chat_id):
    shop_text = 'Велкам ту зе сикрит шоп!'
    markup = types.InlineKeyboardMarkup(row_width=1)

    hp_button = types.InlineKeyboardButton('+50 HP', callback_data= 'shop_hp')
    dmg_button = types.InlineKeyboardButton('+20 Dmg', callback_data= 'shop_damage')
    rounds_button = types.InlineKeyboardButton('+1 Пулька в магазине', callback_data= 'shop_rounds')
    skip_button = types.InlineKeyboardButton('Пропустить (sosал?)', callback_data= 'shop_skip')

    markup.add(hp_button, dmg_button, rounds_button, skip_button)
    sent = bot.send_message(chat_id, shop_text, reply_markup=markup)
    users[chat_id]['last_message_id'] = sent.message_id


def handle_shop(chat_id, choice):
    player_data = users[chat_id]
    response = ''
    if choice == 'hp':
        player_data['Max HP'] += 50
        response = '+ 50 к макс. ХП!'
    elif choice == 'damage':
        player_data['Damage'] += 20
        response = '+ 20 к длине!'
    elif choice == 'rounds':
        player_data['Max rounds'] += 1
        response = '+ 1 маслина в магазине!'
    elif choice == 'skip':
        response = 'В этом нет смысла, как и в жизни'

    player_data['current_level'] += 1
    bot.send_message(chat_id, response)
    start_battle(chat_id)


def show_rules(chat_id):
    rules_text = (
        "   Правила игры\n\n"
        "В игре 5 уровней, пройди их всех, сохранив свою жопу\n"
        "После каждого уровня вам доступен магазин (платно)\n"
        "Баланс в игре отсутствует, мне тотально похй, удачи :===\n\n"
        "Выбирайте действия кнопками йоу, не будьте мудаками"
    )
    markup = types.InlineKeyboardMarkup()
    back_button = types.InlineKeyboardButton('Домой', callback_data='back_to_menu')
    markup.add(back_button)
    bot.send_message(chat_id, rules_text, reply_markup=markup)


bot.infinity_polling()
