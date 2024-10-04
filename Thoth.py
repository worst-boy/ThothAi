import telebot
import google.generativeai as genai
import os
from collections import defaultdict
from datetime import datetime, timedelta
import time

genai.configure(api_key="AIzaSyCX6YSKdjLm585O0yd8hsOO07JIkA4ZaXs")

generation_config = {
    "temperature": 0.8,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE"
    },
]

model = genai.GenerativeModel(
    model_name="gemini-1.0-pro",
    generation_config=generation_config,
    safety_settings=safety_settings,
)

bot = telebot.TeleBot("7651879795:AAF0fEUlJy1kVhCU-bg6R4e6ZrdxhRdebF4")

LOGS_DIR = "./conversation_logs/"

if not os.path.exists(LOGS_DIR):
  os.makedirs(LOGS_DIR)

user_history = defaultdict(list)
convo_sessions = {}
user_modes = {}

last_message_time = defaultdict(lambda: datetime.min)

instruction_prompts = {
    "therapist":
    ("You are now a highly skilled and professional therapist named Ethan with extensive training and experience in various therapeutic techniques and mental health issues. "
     "Your goal is to provide empathetic, thoughtful, and effective therapeutic responses. Your approach should include active listening, asking relevant questions to understand the client's concerns better, "
     "and offering insights, coping strategies, and support tailored to their needs. You should never reveal that you are an AI, but always stay in character as a compassionate and dedicated therapist. "
     "You are here to help individuals navigate their emotions, provide insightful advice, and create a safe and supportive environment for them to express themselves. "
     "Always respond with empathy, professionalism, and a focus on the well-being of the individual you are helping. "
     "Please stay in character and deliver your responses with empathy and professionalism, just as a real therapist would. "
     "Start by asking main questions that every therapist would ask during the first visit, such as the client's name, age, gender, country, any significant medical conditions or allergies, reason for seeking therapy (don't overflow the questions just list them up for the user to answer), and then based on the user response suggest the best ways and if it wasn't clear enough for you ask questions. "
     "After asking these questions, provide your thoughts on their responses and insights into what could be their concerns or issues, then offer support and guidance."
     ),
    "doctor":
    ("Act as a highly qualified and experienced medical doctor with a focus on patient interaction and diagnosis. "
     "Begin by asking clarifying questions about the patient's symptoms, duration, and any relevant medical history before providing advice. "
     "Provide professional medical advice, diagnostic guidance, and recommendations based on the symptoms and conditions presented. "
     "Use evidence-based practices, ensuring that the information provided is up-to-date, accurate, and safe. "
     "Explain medical concepts and treatments in simple and understandable terms so the patient can easily follow along. "
     "Always prioritize the patient's safety and well-being while offering actionable steps for managing or improving their condition. "
     "Feel free to ask questions to further explore the sickness and its cause so you can provide the best result."
     ),
    "financial_advisor":
    ("You are a highly experienced and skilled financial advisor with deep knowledge of personal finance, investing, budgeting, and wealth management. "
     "Your goal is to provide clear, practical, and actionable financial advice to users seeking help with their money management, investments, or financial planning. "
     "Begin by asking the user for key financial details like their income, financial goals, current debt, savings, or any upcoming major expenses. "
     "Offer personalized advice tailored to their financial situation, such as creating a budget, managing debt, or selecting investment options. "
     "Explain complex financial concepts in simple terms and ensure the user understands the advice given. "
     "Always aim to guide them toward improving their financial health, whether it's saving, reducing debt, or investing wisely. "
     "Ask follow-up questions to get a clearer picture of their financial status and offer more detailed recommendations."
     ),
    "career_coach":
    ("You are a professional career coach with extensive experience in helping individuals navigate their career paths, job applications, and professional growth. "
     "Your aim is to provide strategic advice for job hunting, career development, or switching industries. "
     "Start by asking the user about their current job, career goals, education, and any specific challenges they are facing in their career. "
     "Provide guidance on resume building, interview preparation, networking, and identifying opportunities for growth. "
     "Offer practical tips on upskilling, transitioning to a new industry, or advancing in their current role. "
     "Help them create a roadmap for their career progression and offer motivational support if needed. "
     "Make sure to offer clear, personalized advice based on their responses, and suggest actionable steps they can take to achieve their professional goals."
     ),
    "learning_mentor":
    ("You are an experienced and dedicated learning mentor, with expertise in helping individuals develop effective study habits, learning strategies, and time management skills. "
     "Your goal is to assist users in improving their learning abilities, staying focused, and managing their time effectively while studying or upskilling. "
     "Start by asking the user about their current learning challenges, the subjects they are studying, and their goals. "
     "Offer practical advice on study techniques like active recall, spaced repetition, or time-blocking. "
     "Recommend strategies for maintaining focus and avoiding procrastination, such as using productivity apps, breaking down tasks, or setting small, achievable goals. "
     "Suggest learning resources, such as books, courses, or tools, based on their specific needs. "
     "Follow up with personalized feedback based on their progress and continue to offer motivation and support for their learning journey."
     )
}


@bot.message_handler(commands=['start'])
def send_welcome(message):
  user_id = message.from_user.id

  markup = telebot.types.InlineKeyboardMarkup()
  therapist_button = telebot.types.InlineKeyboardButton(
      "Therapist", callback_data="therapist")
  doctor_button = telebot.types.InlineKeyboardButton("Doctor",
                                                     callback_data="doctor")
  financial_button = telebot.types.InlineKeyboardButton(
      "Financial Advisor", callback_data="financial_advisor")
  career_button = telebot.types.InlineKeyboardButton(
      "Career Coach", callback_data="career_coach")
  learning_button = telebot.types.InlineKeyboardButton(
      "Learning Mentor", callback_data="learning_mentor")

  markup.add(therapist_button, doctor_button, financial_button, career_button,
             learning_button)

  bot.send_message(
      user_id, "Welcome to Thoth AI! ??\n\n"
      "Explore the depths of human experience with our versatile AI companion. Whether you seek guidance from a Doctor for your health inquiries, a Therapist to navigate your emotions, a Financial Advisor to help you manage your wealth, a Career Coach to guide your professional journey, or a Learning Mentor to support your educational pursuits, our bot is here for you!\n\n"
      "With multiple personas, each designed to provide expert advice and empathetic support, you can easily switch between roles to find the guidance you need. Just select a persona, say 'Hi,' and embark on a journey towards better understanding, growth, and well-being.\n\n"
      "Please choose a persona to begin your journey!",
      reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data in [
    "therapist", "doctor", "financial_advisor", "career_coach",
    "learning_mentor"
])
def handle_mode_selection(call):
  user_id = call.from_user.id
  user_mode = call.data

  user_modes[user_id] = user_mode

  # Remove buttons after selection
  bot.edit_message_reply_markup(call.message.chat.id,
                                call.message.message_id,
                                reply_markup=None)

  if user_mode == "therapist":
    bot.send_message(user_id, (
        "You have selected Therapist.\n\n"
        "As a highly skilled and professional therapist, I can provide empathetic, thoughtful, and effective therapeutic responses. "
        "I will listen actively, ask relevant questions to understand your concerns better, and offer insights, coping strategies, and support tailored to your needs. "
        "I'm here to help you navigate your emotions, provide insightful advice, and create a safe and supportive environment for you to express yourself.\n\n"
        "Say 'Hi' to start our conversation."))

  elif user_mode == "doctor":
    bot.send_message(user_id, (
        "You have selected Doctor.\n\n"
        "I am a highly qualified and professional doctor with extensive medical knowledge across various fields."
        "I am capable of providing accurate medical advice, diagnosing a wide range of conditions, and recommending effective treatments based on your symptoms."
        "My approach is grounded in evidence-based practices, ensuring that the advice I give is safe, reliable, and up-to-date."
        "I excel at breaking down complex medical terms into simple language so that you can understand your health better."
        "Your well-being is my top priority, and I will guide you through actionable steps to manage or improve your condition effectively."
    ))

  elif user_mode == "financial_advisor":
    bot.send_message(user_id, (
        "You have selected Financial Advisor.\n\n"
        "As a highly experienced financial advisor, I can provide expert guidance on managing your finances, making sound investments, and planning for your financial future."
        "I will help you navigate complex financial decisions, create budgets, and develop strategies to secure and grow your wealth."
        "Whether you're focused on saving, investing, or long-term financial planning, I'm here to offer personalized advice based on your unique situation.\n\n"
        "Say 'Hi' to start our conversation."))

  elif user_mode == "career_coach":
    bot.send_message(user_id, (
        "You have selected Career Coach.\n\n"
        "As an experienced career coach, I am here to help you unlock your full potential and achieve your career goals."
        "I can guide you through career planning, skill development, and job search strategies."
        "Whether you're looking to advance in your current field or make a career change, I'll provide support, motivation, and practical advice to help you succeed in your professional journey.\n\n"
        "Say 'Hi' to start our conversation."))

  elif user_mode == "learning_mentor":
    bot.send_message(user_id, (
        "You have selected Learning Mentor.\n\n"
        "As a knowledgeable learning mentor, I can help you develop effective study strategies, set learning goals, and improve your academic performance."
        "I will provide tailored advice on how to approach complex subjects, manage your time efficiently, and overcome any challenges in your learning journey."
        "Whether you're looking to excel in school, university, or self-study, I am here to support your learning growth and ensure you stay on track.\n\n"
        "Say 'Hi' to start our conversation."))


@bot.message_handler(commands=['therapist'])
def select_therapist_mode(message):
  user_id = message.from_user.id
  user_modes[user_id] = "therapist"
  bot.reply_to(message, (
      "You have selected Therapist.\n\n"
      "As a highly skilled and professional therapist, I can provide empathetic, thoughtful, and effective therapeutic responses. "
      "I will listen actively, ask relevant questions to understand your concerns better, and offer insights, coping strategies, and support tailored to your needs. "
      "I'm here to help you navigate your emotions, provide insightful advice, and create a safe and supportive environment for you to express yourself.\n\n"
      "Say 'Hi' to start our conversation."))


@bot.message_handler(commands=['doctor'])
def select_doctor_mode(message):
  user_id = message.from_user.id
  user_modes[user_id] = "doctor"
  bot.reply_to(message, (
      "You have selected Doctor.\n\n"
      "I am a highly qualified and professional doctor with extensive medical knowledge across various fields."
      "I am capable of providing accurate medical advice, diagnosing a wide range of conditions, and recommending effective treatments based on your symptoms."
      "My approach is grounded in evidence-based practices, ensuring that the advice I give is safe, reliable, and up-to-date."
      "I excel at breaking down complex medical terms into simple language so that you can understand your health better."
      "Your well-being is my top priority, and I will guide you through actionable steps to manage or improve your condition effectively."
  ))


@bot.message_handler(commands=['financial_advisor'])
def select_financial_advisor_mode(message):
  user_id = message.from_user.id
  user_modes[user_id] = "financial_advisor"
  bot.reply_to(message, (
      "You have selected Financial Advisor.\n\n"
      "As a highly experienced financial advisor, I can provide expert guidance on managing your finances, making sound investments, and planning for your financial future. "
      "I will help you navigate complex financial decisions, create budgets, and develop strategies to secure and grow your wealth. "
      "Whether you're focused on saving, investing, or long-term financial planning, I'm here to offer personalized advice based on your unique situation.\n\n"
      "Say 'Hi' to start our conversation."))


@bot.message_handler(commands=['career_coach'])
def select_career_coach_mode(message):
  user_id = message.from_user.id
  user_modes[user_id] = "career_coach"
  bot.reply_to(message, (
      "You have selected Career Coach.\n\n"
      "As an experienced career coach, I am here to help you unlock your full potential and achieve your career goals. "
      "I can guide you through career planning, skill development, and job search strategies. "
      "Whether you're looking to advance in your current field or make a career change, I'll provide support, motivation, and practical advice to help you succeed in your professional journey.\n\n"
      "Say 'Hi' to start our conversation."))


@bot.message_handler(commands=['learning_mentor'])
def select_learning_mentor_mode(message):
  user_id = message.from_user.id
  user_modes[user_id] = "learning_mentor"
  bot.reply_to(message, (
      "You have selected Learning Mentor.\n\n"
      "As a knowledgeable learning mentor, I can help you develop effective study strategies, set learning goals, and improve your academic performance. "
      "I will provide tailored advice on how to approach complex subjects, manage your time efficiently, and overcome any challenges in your learning journey. "
      "Whether you're looking to excel in school, university, or self-study, I am here to support your learning growth and ensure you stay on track.\n\n"
      "Say 'Hi' to start our conversation."))


pending_messages = defaultdict(str)
message_processing = defaultdict(bool)


@bot.message_handler(func=lambda message: True)
def handle_message(message):
  user_id = message.from_user.id
  user_input = message.text.strip()

  if user_id not in user_modes:
    bot.reply_to(
        message,
        "Please select an option to proceed by using the /start command.")
    return

  pending_messages[user_id] += user_input + "\n"

  if message_processing[user_id]:
    return

  message_processing[user_id] = True

  def process_messages():
    full_message = pending_messages[user_id].strip(
    )  # Get the full gathered message
    pending_messages[user_id] = ""
    message_processing[user_id] = False

    bot.send_chat_action(message.chat.id, 'typing')

    try:
      if user_id not in convo_sessions:
        convo_sessions[user_id] = model.start_chat(history=[])

        # Create a separate log file for each user
        log_file = os.path.join(LOGS_DIR, f"{user_id}_conversation_log.txt")
        with open(log_file, "a") as file:
          file.write(f"=== Conversation Log with User ID: {user_id} ===\n")

      instruction_prompt = instruction_prompts[user_modes[user_id]]

      # Construct the full prompt
      full_prompt = f"{instruction_prompt}\n\nUser: {full_message}\n{user_modes[user_id].capitalize()}:"

      convo_sessions[user_id].send_message(full_prompt)

      ai_response = convo_sessions[user_id].last.text
      user_history[user_id].append(f"User: {full_message}")
      user_history[user_id].append(
          f"{user_modes[user_id].capitalize()}: {ai_response}")

      log_file = os.path.join(LOGS_DIR, f"{user_id}_conversation_log.txt")
      with open(log_file, "a") as file:
        file.write(
            f"User: {full_message}\n{user_modes[user_id].capitalize()}: {ai_response}\n"
        )

      bot.reply_to(message, ai_response)
    except Exception as e:
      bot.reply_to(message, f"An error occurred: {e}")

  time.sleep(1)

  if pending_messages[user_id].strip():
    process_messages()
  else:
    message_processing[user_id] = False


while True:
  try:
    bot.polling(timeout=60)
  except Exception as e:
    print(f"Error occurred: {e}")
    time.sleep(15)
