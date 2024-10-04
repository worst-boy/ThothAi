# Thoth AI - A Telegram AI Bot for Multiple Personas

#### Video Demo: <URL HERE>

## Introduction

Thoth AI is a versatile and intelligent Telegram bot designed to assist users with a range of needs. Whether you're looking for mental health guidance from a therapist, financial advice, career coaching, or learning mentorship, Thoth AI provides expert-level conversations across multiple personas. The bot leverages the **Gemini-1.0-Pro** API from Google’s generative AI services to deliver high-quality, human-like responses.

## Features

- **Therapist**: Provides empathetic, therapeutic support based on user input.
- **Doctor**: Gives accurate and professional medical advice.
- **Financial Advisor**: Offers guidance on personal finance and investment strategies.
- **Career Coach**: Helps users navigate their career paths with personalized advice.
- **Learning Mentor**: Provides learning strategies and study techniques to boost productivity.

## How It Works

The bot allows users to select different personas via inline keyboard buttons. Once a persona is selected, the bot will adopt the corresponding personality and respond accordingly based on user queries. This is achieved through pre-configured persona instruction prompts that guide the AI responses.

## Technologies Used

- **Telegram Bot API**: To handle messaging and bot interaction ([API Docs](https://core.telegram.org/bots/api)).
- **Google Gemini-1.0-Pro API**: Provides generative AI for intelligent responses ([API Docs](https://ai.google.dev/gemini-api/docs)).
- **Python**: The core programming language used for scripting the bot ([Python Website](https://www.python.org/downloads/)).
- **Telebot**: A Python wrapper for working with the Telegram Bot API ([Telebot Docs](https://pytba.readthedocs.io/en/latest/)).
- **Google Generative AI Library**: For integrating the Gemini API ([PyPi](https://pypi.org/project/google-generativeai/)).

## Requirements

To run Thoth AI, you will need:

- Python 3.8 or higher
- **Telebot Library**: Install via pip 
    ```bash
    pip install pyTelegramBotAPI
    ```
- **Google Generative AI Library**:
    ```bash
    pip install google-generativeai
    ```
- A **Google Gemini API Key** and **Telegram Bot Token**

## Installation

1. Clone the repository.
    ```bash
    git clone <repository_url>
    cd <project_directory>
    ```

2. Install the required dependencies.
    ```bash
    pip install pyTelegramBotAPI
    pip install google-generativeai
    ```

3. Set up environment variables for your Google API Key and Telegram Bot Token in `.env` file:
    ```bash
    TELEGRAM_BOT_TOKEN=your_telegram_token
    GOOGLE_API_KEY=your_google_api_key
    ```

4. Start the bot:
    ```bash
    python bot.py
    ```

## Setup Instructions

1. **Create a Bot**: Set up a Telegram bot by talking to [BotFather](https://t.me/BotFather), then obtain the bot token.
2. **Configure API Access**: Obtain your Google Gemini API key from Google Cloud and set it in the script.
3. **Start the Bot**: Run the bot locally or on a server, and it will be available on Telegram for users to interact with.
4. **User Interaction**: Users can choose from the following personas to begin conversations:
    - Therapist
    - Doctor
    - Financial Advisor
    - Career Coach
    - Learning Mentor

## Testing the Project

1. After starting the bot, open Telegram and search for your bot.
2. Begin by typing `/start` to view the persona options.
3. Choose a persona and start interacting. For example, say "Hi" to the therapist or ask for financial advice.
4. Check if the bot responds appropriately according to the selected persona.

## Known Bugs/Limitations

- The bot may sometimes exceed the character limit for a single message, leading to message truncation.
- The response time depends on the availability and speed of the Google Gemini API.
- This bot does not provide real-time updates on medical conditions; it is purely informational.

## Future Enhancements

- Add more personas for specialized needs like legal advice, fitness training, or nutritional coaching.
- Improve the conversation logging mechanism to store session data more efficiently.
- Explore hosting the bot on cloud platforms for 24/7 availability.
