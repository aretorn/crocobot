import random
my_dict = ['слово', 'інше', 'загадка', 'костиль'] #тут нада прикрутить якийсь словник
used_words = [] #вже використані слова
def change_word():
    word = random.choice(my_dict)
    return word
def game():
    while True:
        word = change_word()
        #тут повинна бути функція яка показує яке слово потрібно загадати іншим користувачам конерктному юзеру
        print(word)
        player_word = input()
        print()
        if player_word == word:
            print(word)
            print (f'User_id win! user id2 zagaduye slovo')
game()
