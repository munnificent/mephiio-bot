@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'data1':
                today1 = day(1)
                if str(call.message.chat.id) in joinedUsers1:
                    if today1 == 0:
                        img = open('pic/monday.png', 'rb')
                        bot.send_photo(call.message.chat.id, img)
                    elif today1 == 1:
                        img = open('pic/tuesday.png', 'rb')
                        bot.send_photo(call.message.chat.id, img)
                    elif today1 == 2:
                        img = open('pic/wednesday.png', 'rb')
                        bot.send_photo(call.message.chat.id, img)
                    elif today1 == 3:
                        img = open('pic/thursday.png', 'rb')
                        bot.send_photo(call.message.chat.id, img)
                    elif today1 == 4:
                        img = open('pic/friday.png', 'rb')
                        bot.send_photo(call.message.chat.id, img)
                    elif today1 == 5:
                        img = open('pic/saturday.png', 'rb')
                        bot.send_photo(call.message.chat.id, img)
                    elif today1 == 6:
                        img = open('pic/saturday.png', 'rb')
                        bot.send_photo(call.message.chat.id, img)
                    else:
                        bot.send_message(call.message.chat.id, "Ошибка")
                elif str(call.message.chat.id) in joinedUsers2:
                    if today1 == 0:
                        img = open('pic1/monday.png', 'rb')
                        bot.send_photo(call.message.chat.id, img)
                    elif today1 == 1:
                        img = open('pic1/tuesday.png', 'rb')
                        bot.send_photo(call.message.chat.id, img)
                    elif today1 == 2:
                        img = open('pic1/wednesday.png', 'rb')
                        bot.send_photo(call.message.chat.id, img)
                    elif today1 == 3:
                        img = open('pic1/thursday.png', 'rb')
                        bot.send_photo(call.message.chat.id, img)
                    elif today1 == 4:
                        img = open('pic1/friday.png', 'rb')
                        bot.send_photo(call.message.chat.id, img)
                    elif today1 == 5:
                        img = open('pic1/saturday.png', 'rb')
                        bot.send_photo(call.message.chat.id, img)
                    elif today1 == 6:
                        img = open('pic1/saturday.png', 'rb')
                        bot.send_photo(call.message.chat.id, img)
                    else:
                        bot.send_message(call.message.chat.id, "Ошибка")
                elif str(call.message.chat.id) in joinedUsers3:
                    if today1 == 0:
                        img = open('pic2/monday.png', 'rb')
                        bot.send_photo(call.message.chat.id, img)
                    elif today1 == 1:
                        img = open('pic2/tuesday.png', 'rb')
                        bot.send_photo(call.message.chat.id, img)
                    elif today1 == 2:
                        img = open('pic2/wednesday.png', 'rb')
                        bot.send_photo(call.message.chat.id, img)
                    elif today1 == 3:
                        img = open('pic2/thursday.png', 'rb')
                        bot.send_photo(call.message.chat.id, img)
                    elif today1 == 4:
                        img = open('pic2/friday.png', 'rb')
                        bot.send_photo(call.message.chat.id, img)
                    elif today1 == 5:
                        img = open('pic2/saturday.png', 'rb')
                        bot.send_photo(call.message.chat.id, img)
                    elif today1 == 6:
                        img = open('pic2/saturday.png', 'rb')
                        bot.send_photo(call.message.chat.id, img)
                    else:
                        bot.send_message(call.message.chat.id, "Ошибка")
                elif str(call.message.chat.id) in joinedUsers4:
                    if today1 == 0:
                        img = open('pic3/monday.png', 'rb')
                        bot.send_photo(call.message.chat.id, img)
                    elif today1 == 1:
                        img = open('pic3/tuesday.png', 'rb')
                        bot.send_photo(call.message.chat.id, img)
                    elif today1 == 2:
                        img = open('pic3/wednesday.png', 'rb')
                        bot.send_photo(call.message.chat.id, img)
                    elif today1 == 3:
                        img = open('pic3/thursday.png', 'rb')
                        bot.send_photo(call.message.chat.id, img)
                    elif today1 == 4:
                        img = open('pic3/friday.png', 'rb')
                        bot.send_photo(call.message.chat.id, img)
                    elif today1 == 5:
                        img = open('pic3/saturday.png', 'rb')
                        bot.send_photo(call.message.chat.id, img)
                    elif today1 == 6:
                        img = open('pic3/saturday.png', 'rb')
                        bot.send_photo(call.message.chat.id, img)
                    else:
                        bot.send_message(call.message.chat.id, "Ошибка")
            elif call.data == 'data2':
                today1 = day(1)
                if str(call.message.chat.id) in joinedUsers1:
                    if today1 == 6:
                        img = open('pic/monday.png', 'rb')
                        bot.send_photo(call.message.chat.id, img)
                    elif today1 == 0:
                        img = open('pic/tuesday.png', 'rb')
                        bot.send_photo(call.message.chat.id, img)
                    elif today1 == 1:
                        img = open('pic/wednesday.png', 'rb')
                        bot.send_photo(call.message.chat.id, img)
                    elif today1 == 2:
                        img = open('pic/thursday.png', 'rb')
                        bot.send_photo(call.message.chat.id, img)
                    elif today1 == 3:
                        img = open('pic/friday.png', 'rb')
                        bot.send_photo(call.message.chat.id, img)
                    elif today1 == 4:
                        img = open('pic/saturday.png', 'rb')
                        bot.send_photo(call.message.chat.id, img)
                    elif today1 == 5:
                        img = open('pic/saturday.png', 'rb')
                        bot.send_photo(call.message.chat.id, img)
                    else:
                        bot.send_message(call.message.chat.id, "Ошибка")
                elif str(call.message.chat.id) in joinedUsers2:
                    if today1 == 6:
                        img = open('pic1/monday.png', 'rb')
                        bot.send_photo(call.message.chat.id, img)
                    elif today1 == 0:
                        img = open('pic1/tuesday.png', 'rb')
                        bot.send_photo(call.message.chat.id, img)
                    elif today1 == 1:
                        img = open('pic1/wednesday.png', 'rb')
                        bot.send_photo(call.message.chat.id, img)
                    elif today1 == 2:
                        img = open('pic1/thursday.png', 'rb')
                        bot.send_photo(call.message.chat.id, img)
                    elif today1 == 3:
                        img = open('pic1/friday.png', 'rb')
                        bot.send_photo(call.message.chat.id, img)
                    elif today1 == 4:
                        img = open('pic1/saturday.png', 'rb')
                        bot.send_photo(call.message.chat.id, img)
                    elif today1 == 5:
                        img = open('pic1/saturday.png', 'rb')
                        bot.send_photo(call.message.chat.id, img)
                    else:
                        bot.send_message(call.message.chat.id, "Ошибка")
                elif str(call.message.chat.id) in joinedUsers3:
                    if today1 == 6:
                        img = open('pic2/monday.png', 'rb')
                        bot.send_photo(call.message.chat.id, img)
                    elif today1 == 0:
                        img = open('pic2/tuesday.png', 'rb')
                        bot.send_photo(call.message.chat.id, img)
                    elif today1 == 1:
                        img = open('pic2/wednesday.png', 'rb')
                        bot.send_photo(call.message.chat.id, img)
                    elif today1 == 2:
                        img = open('pic2/thursday.png', 'rb')
                        bot.send_photo(call.message.chat.id, img)
                    elif today1 == 3:
                        img = open('pic2/friday.png', 'rb')
                        bot.send_photo(call.message.chat.id, img)
                    elif today1 == 4:
                        img = open('pic2/saturday.png', 'rb')
                        bot.send_photo(call.message.chat.id, img)
                    elif today1 == 5:
                        img = open('pic2/saturday.png', 'rb')
                        bot.send_photo(call.message.chat.id, img)
                    else:
                        bot.send_message(call.message.chat.id, "Ошибка")
                elif str(call.message.chat.id) in joinedUsers4:
                    if today1 == 6:
                        img = open('pic3/monday.png', 'rb')
                        bot.send_photo(call.message.chat.id, img)
                    elif today1 == 0:
                        img = open('pic3/tuesday.png', 'rb')
                        bot.send_photo(call.message.chat.id, img)
                    elif today1 == 1:
                        img = open('pic3/wednesday.png', 'rb')
                        bot.send_photo(call.message.chat.id, img)
                    elif today1 == 2:
                        img = open('pic3/thursday.png', 'rb')
                        bot.send_photo(call.message.chat.id, img)
                    elif today1 == 3:
                        img = open('pic3/friday.png', 'rb')
                        bot.send_photo(call.message.chat.id, img)
                    elif today1 == 4:
                        img = open('pic3/saturday.png', 'rb')
                        bot.send_photo(call.message.chat.id, img)
                    elif today1 == 5:
                        img = open('pic3/saturday.png', 'rb')
                        bot.send_photo(call.message.chat.id, img)
                    else:
                        bot.send_message(call.message.chat.id, "Ошибка")