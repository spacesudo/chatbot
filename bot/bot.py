import telebot
from telebot.util import antiflood, quick_markup ,extract_arguments
from dotenv import load_dotenv
import os
from db import Users
from func import chatbot


load_dotenv()


Token = os.getenv('TOKEN')

bot = telebot.TeleBot(Token, parse_mode='Markdown', disable_web_page_preview=True)

db_user = Users()
db_user.setup()

@bot.message_handler(commands=['broadcast'])
def broadcast(message):
    print(message.from_user.id)
    messager = message.chat.id
    if str(messager) == "7034272819" or str(messager) == "6219754372":
        send = bot.send_message(message.chat.id,"Enter message to broadcast")
        bot.register_next_step_handler(send,sendall)

    else:
        bot.reply_to(message, "You're not allowed to use this command")



def sendall(message):
    users = db_user.get_users()
    for chatid in users:
        try:
            msg = antiflood(bot.send_message, chatid, message.text)
        except Exception as e:
            print(e)

    bot.send_message(message.chat.id, "done")


@bot.message_handler(commands=['userno'])
def userno(message):
    print(message.from_user.id)
    messager = message.chat.id
    if str(messager) == "7034272819" or str(messager) == "6219754372":
        x = db_user.get_users()
        bot.reply_to(message,f"Total bot users: {len(x)}")
    else:
        bot.reply_to(message, "admin command")
        
        
@bot.message_handler(commands=['start'])
def start(message):
    owner = message.chat.id
    db_user.add_user(owner)
    msg = f"""Welcome to Health Tracker AI *{message.chat.first_name}*!!!
    
We offer a wide range of health tracking system right from your telegram app to help you diagnose and keep track of everything health related

Keep fit and stay healthy with Tracker AI
    """
    markup = quick_markup({
        'Health AI chat bot' : {'callback_data' : 'chatbot'},
        "Health Record" : {'callback_data' : 'record'},
        "HealthCare Connect/Data" : {'callback_data' : 'connect'},
        "Health Products" : {'callback_data' : 'products'}
    })
    bot.send_message(owner, msg, reply_markup=markup)
    

def product(message):
    owner = message.chat.id
    msg = """Welcome to Tracker AI stores
    
We have a wide range of products for you to choose from to track and monitor your health status.

    
    """
    m = quick_markup({
        'Start Shopping' : {'callback_data' : 'shop'},
    })
    bot.send_message(owner, msg, reply_markup=m)
    
    
    
@bot.callback_query_handler(func= lambda call: True)
def call_handler(call):
    owner = call.message.chat.id
    
    if call.data == 'shop':
        msg = 'Feature and products coming soon...'
        bot.send_message(owner, msg)
        
    elif call.data == 'products':
        product(call.message)
        
    elif call.data == 'record':
        s = bot.send_message(owner, "Send a full detailed text of your health report from a clinic or hospital for detailed assistance")
        bot.register_next_step_handler(s, record)
        
    elif call.data == 'chatbot':
        bot.send_message(owner, "Talk to the bot about health related matters")
        
    elif call.data == 'connect':
        msg = "Welcome to Tracker AI healthcare connect where we give you special access to health records and specialized doctors to help you right from your telegram.\nWhether you're a Users, Doctor, or Developer looking to work with us, Our rich-culture environment makes it all easy as we prioritize the best among others in terms of HealthCare Data to provide you all you need.\nTo Procced, use any of the buttons below to connect with us..."
        markup = quick_markup({
            'Users' : {'callback_data' : 'Users'}, 
            'Doctors' : {'callback_data' : 'doctor'},
            'Developers' : {'callback_data' : 'developers'},
        })
        bot.edit_message_text(msg, owner, call.message.message_id, reply_markup=markup)
        
    elif call.data == 'Users':
        s = bot.send_message(owner, "Send your health report file")
        bot.register_next_step_handler(s, file_record)
        
    elif call.data == 'doctor':
        msg = "To authenticate yourself as a Doctor to get healthcare record, click on the button below and our admin will perform all necessary checks "
        markup = quick_markup({
            'Authenticate ' : {'callback_data' : 'auth'}
        })
        bot.send_message(owner, msg, reply_markup=markup)
        
    elif call.data == 'developers':
        msg = "To authenticate yourself as a Developer to get healthcare record, click on the button below and our admin will perform all necessary checks "
        markup = quick_markup({
            'Authenticate ' : {'callback_data' : 'auth'}
        })
        bot.send_message(owner, msg, reply_markup=markup)
        
    elif call.data == 'auth':
        bot.send_message(owner, 'Thanks for coming this far...\nYou will be authenticated in the next 48hrs')
        
def record(message):
    owner = message.chat.id
    text = message.text
    reply = chatbot(text)
    bot.send_message(owner, reply)
    
def file_record(message):
    owner = message.chat.id
    if message.content_type == 'document':
        markup = quick_markup({
            'Authenticate ' : {'callback_data' : 'auth'}
        })
        msg = "To authenticate yourself to get healthcare rewards, click on the button below and our admin will perform all necessary checks "
        bot.send_message(owner, msg, reply_markup=markup)
    else:
        bot.send_message(owner, "Please send a health report file")
           
@bot.message_handler(func=lambda message: True)
def chat_bot(message):
    owner = message.chat.id
    text = message.text
    #bot.reply_to(message, message.text)
    reply = chatbot(text)
    bot.send_message(owner, reply)
        
        
bot.infinity_polling()