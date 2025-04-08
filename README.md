# Making a Chatbot that Shows the Applications, History, Advantages, Disadvantages, and Benefits of AI

This project is a pattern-matching AI chatbot built using Flask and SQLite, designed to answer questions about **Artificial Intelligence (AI)**, including its **applications**, **history**, **advantages**, **disadvantages**, and **benefits**. The chatbot can interact with users based on predefined patterns and responses, record conversation history, provide usage statistics, and allow users to add new patterns dynamically. Additionally, it integrates with the **Gemini API** to provide advanced responses.

# AI Chatbot with Flask and SQLite

This project is a pattern-matching AI chatbot built using Flask and SQLite. The chatbot is capable of interacting with users based on predefined patterns and responses, recording conversation history, providing statistics, and even allowing users to add custom patterns and responses dynamically. Additionally, it includes an advanced chatbot using the Gemini API for more accurate responses.

## Features

### 1. **Pattern-Based Chatbot**

- The chatbot matches user inputs with predefined patterns and generates corresponding responses.
- Patterns cover a wide range of topics such as AI fundamentals, machine learning, data science, and everyday conversational queries.

### 2. **Conversation History**

- Each interaction between the user and the chatbot is stored in an SQLite database.
- Users can view a history of all interactions, including the user’s prompts, the chatbot’s responses, and timestamps.

### 3. **Chatbot Statistics**

- The application tracks how many times each question is asked.
- Provides statistics such as the most frequently asked questions and recent interactions.

### 4. **Custom Pattern Addition**

- The system allows users to dynamically add new patterns and responses through a dedicated interface.
- Custom patterns are saved in a database, and the chatbot can use them immediately in future interactions.

### 5. **Advanced Chatbot (Gemini API)**

- The chatbot includes an advanced conversational model powered by the Gemini API, offering more sophisticated and context-aware responses.
- Users can switch between the basic pattern-based responses and the advanced chatbot.

## Project Structure

- **`app.py`**: The main application file containing the logic for handling user input, generating responses, saving conversations, and providing statistics.
- **`routes.py`**: A separate file to manage Flask routes, cleanly separating the logic.
- **`templates/`**: Contains the HTML templates for rendering the web interface, including pages for conversation history, chatbot statistics, and pattern addition.
- **`chatbot.db`**: SQLite database used to store conversation history, user feedback, and custom patterns.

## How It Works

1. **User Interaction**: The chatbot receives input from the user through a web interface. It uses pattern matching (via regular expressions) to determine an appropriate response.
2. **Pattern Matching**: Patterns are pre-programmed in the `app.py` file, but users can also add new patterns and responses dynamically via the `/add_pattern` page.
3. **Conversation History**: Each interaction is recorded in the database, which can be accessed via the `/history` page.
4. **Statistics**: The `/stats` page provides insights into the chatbot's usage, such as the total number of questions asked, the most common inputs, and recent activity.
5. **Advanced Mode**: For more complex conversations, the chatbot can switch to an advanced model using the Gemini API.

## programming languages

    ## frontend
    1:   HTML, CSS

    ## Backend
    1: Flask, java script

    ## required liberaris
    : python liberary : Flask

## Running the application

    python app.py

Usage
Visit http://127.0.0.1:5000/ to start interacting with the chatbot.

Use the /history page to view previous conversations.

Visit /stats to see usage statistics.

Use /add_pattern to add new custom patterns and responses to the chatbot.


