import telebot
from telebot.handler_backends import SkipHandler as Skip
from telebot.util import quick_markup
from email.message import EmailMessage
import ssl
import smtplib

#constants temp
id="YTUVBNQ"
otp="862139"
user_access = False
data = { "primary" : {"CCTV ID":"284619","Station":"C1","Zone":"Central Zone","Location-lat":11.020987,"Location-long": 76.970909},
"secondary" : {"CCTV ID":"986821","Station":"B6","Zone":"East Zone","Location-lat":11.024802,"Location-long": 77.010389},
"third" : {"CCTV ID":"728177","Station":"C2","Zone":"Central Zone","Location-lat":11.001057,"Location-long": 76.973492},
"fourth": {"CCTV ID":"754446","Station":"B1","Zone":"South Zone","Location-lat":10.993843,"Location-long": 76.959645}}

#import pandas as P
print("\n\n\tARCS-UYIR")

#setting API key for telegram bot
bot=telebot.TeleBot("7388798451:AAHAw644qjICpCAzfmNFCyQcW0zMXriT4mI")
markup_1=quick_markup({'Login':{'callback_data':'ln'},'Station':{'callback_data':'s'},'Logout':{'callback_data':'lo'},'Clear':{'callback_data':'c'},'Help':{'callback_data':'h'}},row_width=2)
class Helper:
    

    def send_mail(self):
        email_sender='2495immanuel@gmail.com'
        email_password='hbin nxdd howj lgpu'
        email_receiver="charlesms2006@gmail.com"
        subject=f"Login OTP for ARCS"
        body=f"""
        Hello {email_receiver.split("@")[0]},
        This is an automated message about your login attempt into ARCS the Telegram bot

        Please use the OTP given below to access real-time notification

        OTP: 862139

        If you think this is not an login attempt by you. Please ignore this email

        Thanks & Regards
        0 Brain Cells
        """
        em=EmailMessage()
        em['From']=email_sender
        em['TO']=email_receiver
        em['Subject']=subject
        em.set_content(body)
        context=ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as stmp:
            stmp.login(email_sender,email_password)
            stmp.sendmail(email_sender,email_receiver,em.as_string())
            return True

#defining function of "/start"------------------------------------------------------------------
@bot.message_handler(commands=['start'])
def greet(message):
    msg="Hello, "+message.chat.first_name +" "+ message.chat.last_name +", This is\nARCS - Automated Road Cognition System\n\nA custom solution built for Chennai City Police in order to provide real-time update on hazards, accidents and crime in Chennai\n\nProject part of Ctrl+Alt+Hacks \n\n-0 Brain Cells"
    bot.send_message(message.chat.id,msg,reply_markup=markup_1)
def otp_call():
    @bot.message_handler(func=lambda message: True)
    def A9(otpmessge):
        la=otpmessge.text
        if(la == otp):
            global user_access
            user_access = True
            bot.send_message(otpmessge.chat.id,"You are all set to go.\nWelcome to ARCS a Real-time hazard report system for Coimbatore city \n\n To proceed use /station to set the station to recieve notification from.")
            return True
        else:
            bot.send_message(otpmessge.chat.id,"OTP validation failed, try again.")
            user_access=False
            return False
def login_handler():
    @bot.message_handler(func=lambda message: True)
    def A1(messge):
        print(messge.text)
        lm=messge.text
        print(lm)
        if(lm == id):
            bot.send_message(messge.chat.id,"Welcome, Charles M S. \nPlease enter the OTP you recieved in your mail.")
            obj=Helper()
            print(messge.chat.id)
            obj.send_mail()
            m=otp_call()
            print('reached here',m)
        if(lm != id):
            print(lm,"fhvb")
            print('how??')
            bot.send_message(messge.chat.id, "You are all set to go.\nWelcome to ARCS a Real-time hazard report system for Chennai city \n\n To proceed use /station to set the station to recieve notification from.")
        
#Inline Keyboard Reply -------------------------------------------------------------------------
@bot.callback_query_handler(func=lambda message: True)
def cbq(call):
    #search button
    if call.data =='ln':
        bot.send_message(call.from_user.id,"Please give your ID:")
        login_handler()

    #newsletter button
    if call.data =='n':
        news='''\t\tWEEKLY NEWSLETTER     
17/02/2024: Attended the I-CUBE 3.0 Hackathon and came 3rd
18/02/2024: It was a long day, but we forced ourselves to complete the presented idea
19/02/2024: Still continuing the dev process, seems like this is another 24hr hackthon
19/02/2024(evening): A meeting with the company where I'm going to start my internship at.

-By Lex Magna
            '''
        bot.send_message(call.from_user.id,news)
    #advocate search button
    if call.data =='a':
        bot.answer_callback_query(call.id,"newsletter",True)
    #feedback button
    if call.data =='f':
        bot.answer_callback_query(call.id,"Feeback")
    #tutorial button
    if call.data =='t':
        bot.answer_callback_query(call.id,"Tutorial")
    
#defining function for "/search"
@bot.message_handler(commands=['search'])
def greet(message):
    bot.send_message(message.chat.id,"Search access granted.\nEg:What's Article 269A\n\nShortcuts:\nArticle:<article_no>\nTitle:<title_name>")
    @bot.message_handler(func=lambda message: True)
    def A01(messge):
        print(messge.text)#changes and csv file and pandas here
        bot.send_message(messge.chat.id,"Article:0\nTitle:Preamble\nContent:\n WE, THE PEOPLE OF INDIA, having solemnly resolved to constitute India into a SOVEREIGN SOCIALIST SECULAR DEMOCRATIC REPUBLIC and to secure to all its citizens: JUSTICE, social, economic and political;\n LIBERTY of thought, expression, belief, faith and worship;\nEQUALITY of status and of opportunity;\n and to promote among them all FRATERNITY assuring the dignity of the individual and the unity and integrity of the Nation;\n IN OUR CONSTITUENT ASSEMBLY this twenty-sixth day of November, 1949, do HEREBY ADOPT, ENACT AND GIVE TO OURSELVES THIS CONSTITUTION")

#defining function for "/adv"
@bot.message_handler(commands=['adv'])
def greet(message):
    bot.send_message(message.chat.id,"Search and connect to advocates related to your query.\nEg:Cybercrime advocate in Chennai\n\nShortcut: <location>,<type>,<law firm/advocate>")
    @bot.message_handler(func=lambda message: True)
    def A2(messge):
        print(messge.text)
        s=str(messge.text)
        #search 

#defining function for "/help"
@bot.message_handler(commands=['help'])
def greet(message):
    msg="Hello,"+message.chat.first_name +" "+ message.chat.last_name +",Thanks for choosing Lex Magna, this is your walkthrough for the Telegram Chatbot version of the main web-app lex-magna.xyz."
    msg_2="Command: /search\n-This command is to search through the articles in the Constitution and the other laws and rules proposed by Government of India\n\n-You can also use shortcuts like:\nArticle:<article_no>\n(Used to shortlist your search using the article no)\nEg: Article 15\n\nTitle:<title_name>\n(Used to shortlist your search using the title of the article)\n(Dont worry about the spelling mistakes or accuracy of the title"
    msg_3="\n\nCommand:/adv\n-This command is to search through the list of available lawyers for the specified firm in your locality "
    bot.send_message(message.chat.id,msg)
    bot.send_message(message.chat.id,msg_2)
    bot.send_message(message.chat.id,msg_3)

#call handler and looper
bot.infinity_polling()
