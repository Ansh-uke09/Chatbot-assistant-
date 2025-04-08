# app.py
from flask import Flask, render_template, request, jsonify
import sqlite3
import re
import datetime
import random
from routes import setup_routes

app = Flask(__name__)


# Setup routes from routes.py
setup_routes(app)

# Database setup
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS conversations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_input TEXT NOT NULL,
        bot_response TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    conn.commit()
    conn.close()

    # Initialize database
    init_db()

# Pattern matching responses
patterns =[
    # Basic greetings
    (r'hello|hi|hey', ['Hello!', 'Hi there!', 'Hey! How can I help you?']),
    (r'how are you', ['I\'m doing well, thanks for asking!', 'I\'m good! How about you?']),
    (r'what is your name', ['I\'m a chatbot created with Flask.', 'You can call me FlaskBot!']),
    (r'bye|goodbye', ['Goodbye!', 'See you later!', 'Take care!']),
    (r'thank you|thanks', ['You\'re welcome!', 'No problem!', 'Glad to help!']),
    (r'weather', ['I\'m sorry, I don\'t have access to weather information.', 'I can\'t check the weather, but I hope it\'s nice outside!']),
    (r'time', ['I don\'t have access to real-time data, but I can tell you this conversation is being saved!']),
    (r'help', ['I can chat with you about simple topics. What would you like to talk about?', 'I\'m a simple pattern-matching chatbot. How can I assist you?'])
    ]
patterns =[    # AI Fundamentals
    (r'what is (artificial intelligence|ai)\??', [
        "Artificial Intelligence (AI) is a branch of computer science that aims to create intelligent machines that can simulate human-like thinking and behavior. It involves developing systems capable of tasks that typically require human intelligence.",
        "AI refers to the creation of intelligent machines that work and react like humans. It encompasses problem-solving, learning, and adaptation.",
        "In AI, machines are designed to mimic human cognitive functions like learning and problem-solving, automating processes typically performed by humans."
    ]),

    # Machine Learning
    (r'(what is |explain )?(machine learning|ml)\??', [
        "Machine Learning (ML) is a subset of AI where computers use data to learn and make decisions without being explicitly programmed. It relies on algorithms to find patterns and insights from data.",
        "ML is the science of getting computers to act without being explicitly programmed. It allows systems to learn from data and improve over time.",
        "In machine learning, systems automatically learn and improve from experience without being explicitly coded. It's used in a wide range of AI applications like recommendation engines and voice assistants."
    ]),

    # History of AI
    (r'(what is the )?history of (artificial intelligence|ai)\??', [
        "AI's history began in the 1950s with early pioneers like Alan Turing and John McCarthy. Turing proposed the idea of machines thinking like humans, while McCarthy coined the term 'Artificial Intelligence' in 1956.",
        "AI evolved through several phases, including the development of early neural networks, symbolic AI, and expert systems in the 70s and 80s, to modern-day machine learning and deep learning breakthroughs.",
        "AI development has gone through cycles of optimism and setbacks, known as 'AI winters,' but recent advancements in data processing, computing power, and algorithms have propelled the field forward."
    ]),

    # Importance of AI
    (r'why is (artificial intelligence|ai) important\??', [
        "AI is important because it automates complex tasks, boosts efficiency, and unlocks new capabilities in various industries like healthcare, finance, and transportation.",
        "AI revolutionizes industries by improving decision-making processes, personalizing user experiences, and providing insights through data analysis.",
        "AI is vital to the future of technology as it enables automation, reduces human error, and optimizes processes, driving innovation across sectors."
    ]),

    # Applications of AI
    (r'(what are the |examples of )?(applications|uses) of (artificial intelligence|ai)\??', [
        "AI is used in healthcare for diagnostics, personalized medicine, and robotic surgery. In finance, it powers fraud detection, algorithmic trading, and credit scoring.",
        "In manufacturing, AI helps optimize supply chains and perform predictive maintenance. In entertainment, AI is used for content recommendations and gaming.",
        "AI applications range from self-driving cars to voice assistants (Siri, Alexa), customer service chatbots, image recognition, and smart home devices."
    ]),

    # Advantages of AI
    (r'what are the (advantages|benefits) of (artificial intelligence|ai)\??', [
        "AI increases efficiency by automating repetitive tasks and processing large amounts of data quickly. It helps reduce human error and improve decision-making.",
        "AI enables real-time data analysis, providing insights that help businesses make better decisions. It can personalize experiences and deliver consistent performance.",
        "AI can work 24/7 without fatigue, handle complex calculations, and perform tasks faster than humans, leading to greater productivity and cost savings."
    ]),

    # Disadvantages of AI
    (r'what are the (disadvantages|downsides) of (artificial intelligence|ai)\??', [
        "One of the biggest downsides of AI is job displacement, as automation can replace human workers in certain industries.",
        "AI systems may introduce bias if trained on incomplete or biased data, leading to unfair outcomes. Additionally, AI can lead to privacy concerns and data misuse.",
        "Over-reliance on AI could reduce human creativity and problem-solving. It also raises ethical concerns, such as accountability in decision-making systems."
    ]),

    # AI and Data Science
    (r'what is (data science) and how does it relate to (ai|artificial intelligence)\??', [
        "Data Science is a field that focuses on extracting insights and knowledge from structured and unstructured data. It intersects with AI by providing the data used to train AI models.",
        "In Data Science, techniques like statistical analysis, data mining, and machine learning are used to make sense of large datasets, which are essential for building AI systems.",
        "AI relies on Data Science for data collection, preprocessing, and analysis. The synergy between data science and AI helps machines learn and make informed decisions."
    ]),

    # Graphing and Data Visualization in AI
    (r'what is the role of (graphs|data visualization) in (ai|machine learning)\??', [
        "Data visualization in AI and ML helps to understand complex datasets, reveal patterns, and make informed decisions based on insights from data.",
        "Graphs like bar charts, histograms, scatter plots, and line charts are used to visualize data trends and distributions, making it easier to interpret AI results.",
        "Visualizing data helps in model evaluation and optimization, allowing researchers to identify potential issues, compare model performance, and fine-tune algorithms."
    ]),

    # Types of Graphs
    (r'what are the (types of graphs|different graphs) used in (data science|ai)\??', [
        "Common types of graphs used in AI and data science include bar charts, histograms, scatter plots, pie charts, line graphs, and box plots.",
        "Bar charts represent categorical data, while histograms are used for frequency distribution. Scatter plots show relationships between variables, and pie charts display proportions.",
        "Line graphs are useful for time-series data, while box plots provide insight into data spread and identify outliers."
    ]),

    # Challenges and Future of AI
    (r'what are the challenges and future of (ai|artificial intelligence)\??', [
        "Challenges for AI include ethical concerns, such as data privacy, algorithmic bias, and the need for transparency in decision-making. Ensuring safety and control of AI systems is also critical.",
        "The future of AI looks promising with advancements in quantum computing, natural language understanding, and autonomous systems. AI is expected to integrate into more areas of life, driving innovation.",
        "AI's future will likely focus on creating more explainable and ethical AI systems, enhancing human-AI collaboration, and addressing the challenges of data governance and cybersecurity."
    ]),

    # Conclusion
    (r'what is the (conclusion|summary) of (artificial intelligence|ai)\??', [
        "AI is a transformative technology that holds great promise across various fields. While it has its advantages and challenges, it will continue to shape the future of work, innovation, and everyday life.",
        "AI offers unprecedented opportunities to solve complex problems, but it also requires careful management to address ethical concerns and ensure fair and transparent outcomes.",
        "In conclusion, AI is here to stay, and its ongoing development will lead to new possibilities, making it a crucial component of the technological landscape in the coming years."
    ]),
    # 3. What is an algorithm?
    (r'(what is|explain) an algorithm\??', [
        "An algorithm is a step-by-step set of instructions designed to perform a specific task or solve a problem.",
        "An algorithm is a procedure or formula that processes input data to achieve a particular goal or output.",
        "Algorithms are the backbone of computer programs, guiding how a task is executed by processing data and generating results."
    ]),

    # 4. What is a large language model (LLM)?
    (r'(what is|tell me about) (a|an) large language model|llm\??', [
        "A large language model (LLM) is a type of AI model that is trained on vast amounts of text data to understand and generate human-like language.",
        "LLMs, like GPT-3, are AI systems that process natural language by learning patterns and structures from large datasets to generate contextually relevant responses.",
        "Large language models are powerful AI tools used to understand, generate, and predict text based on patterns they have learned from extensive training data."
    ]),

    # 5. What is natural language processing (NLP)?
    (r'(what is|explain) (natural language processing|nlp)\??', [
        "Natural Language Processing (NLP) is a field of AI that focuses on the interaction between computers and humans using natural language.",
        "NLP enables computers to understand, interpret, and respond to human language in a meaningful way, making technologies like chatbots and voice assistants possible.",
        "NLP involves the use of algorithms to analyze and process text and speech data, allowing machines to perform tasks such as translation, summarization, and sentiment analysis."
    ]),

    # 6. What is AI?

    # 9. What is Data Science?
    (r'(what is|tell me about) data science\??', [
        "Data Science is a field that involves analyzing and interpreting large sets of data to extract insights and inform decision-making.",
        "Data Science combines techniques from statistics, computer science, and machine learning to analyze and visualize data for better understanding.",
        "In Data Science, data is collected, cleaned, and processed to discover patterns and trends that can lead to actionable insights."
    ]),

    # 10. What are neural networks?
    (r'(what are|explain) neural networks\??', [
        "Neural networks are computing systems inspired by the human brain, made up of interconnected layers of artificial neurons that process information.",
        "A neural network is a series of algorithms that attempt to recognize underlying relationships in a set of data through a process that mimics the human brain.",
        "Neural networks are used in deep learning to perform tasks such as image classification, language translation, and game playing."
    ]),

    # 11. What is reinforcement learning?
    (r'(what is|explain) reinforcement learning\??', [
        "Reinforcement Learning is a type of machine learning where an agent learns to make decisions by taking actions in an environment and receiving feedback in the form of rewards or penalties.",
        "Reinforcement Learning focuses on training agents to maximize cumulative rewards through trial and error interactions with their environment.",
        "In reinforcement learning, the system learns by interacting with its environment and improving its decision-making based on the outcomes of its actions."
    ]),

    # 12. What is supervised learning?
    (r'(what is|explain) supervised learning\??', [
        "Supervised Learning is a type of machine learning where the model is trained on labeled data, meaning the input data is paired with the correct output.",
        "In supervised learning, the system learns from examples where the correct answers are provided, allowing it to make accurate predictions for new data.",
        "Supervised Learning involves training models to predict outcomes based on known examples, making it ideal for tasks like classification and regression."
    ]),

    # 13. What is unsupervised learning?
    (r'(what is|explain) unsupervised learning\??', [
        "Unsupervised Learning is a type of machine learning where the model is trained on unlabeled data, meaning the system tries to identify patterns or groupings without explicit guidance.",
        "In unsupervised learning, the system learns to identify patterns and structure in data without any prior labels or classifications.",
        "Unsupervised learning is often used for clustering and association tasks, where the goal is to discover hidden patterns in data."
    ]),

    # 14. What is computer vision?
    (r'(what is|explain) computer vision\??', [
        "Computer Vision is a field of AI that enables machines to interpret and understand visual information from the world, such as images and videos.",
        "In computer vision, algorithms are used to extract information from images or videos, allowing machines to 'see' and make decisions based on visual data.",
        "Computer Vision technologies are used in applications like facial recognition, autonomous driving, and medical imaging."
    ]),

    # 15. What is an AI chatbot?
    (r'(what is|tell me about) an ai chatbot\??', [
        "An AI chatbot is a program that uses natural language processing to simulate conversation with users, allowing it to answer questions, provide information, or carry out tasks.",
        "AI chatbots are built using machine learning algorithms that enable them to understand and respond to human language in real time.",
        "Chatbots can automate customer service, assist with tasks, and provide interactive support through text or voice-based interactions."
    ]),

    # 16. What are the applications of AI?
    (r'(what are|give me examples of) applications of ai\??', [
        "AI is applied in healthcare for diagnostics, predictive analytics, and personalized treatment plans. It is also used in drug discovery and medical imaging.",
        "In finance, AI helps with fraud detection, algorithmic trading, and credit scoring. It enhances decision-making and risk management processes.",
        "AI is also transforming the automotive industry with self-driving cars and driver assistance systems, as well as powering virtual assistants in everyday life."
    ]),

    # 17. What is data mining?
    (r'(what is|explain)| data mining\??', [
        "Data mining is the process of discovering patterns and knowledge from large amounts of data, often using techniques like clustering, association, and anomaly detection.",
        "In data mining, algorithms are used to explore large datasets to identify trends, relationships, or patterns that can provide valuable insights.",
        "Data mining is widely used in business, marketing, and healthcare to extract actionable insights from raw data."
    ]),

    # 18. What is big data?
    (r'(what is|explain) big data\??', [
        "Big Data refers to extremely large datasets that cannot be processed by traditional data management tools. It involves high volumes, high velocity, and a variety of data.",
        "Big Data is characterized by the 3Vs: Volume, Variety, and Velocity, which present challenges in storing, processing, and analyzing data efficiently.",
        "Big Data analytics involves using advanced algorithms to handle and analyze massive datasets for decision-making and predictive modeling."
    ]),

    # 19. What is data preprocessing?
    (r'(what is|explain) data preprocessing\??', [
        "Data preprocessing involves preparing raw data for analysis by cleaning, normalizing, and transforming it into a usable format.",
        "Data preprocessing is a crucial step in machine learning, where data is cleaned, scaled, and transformed to ensure high-quality input for algorithms.",
        "Data preprocessing steps include handling missing values, scaling features, and converting categorical data into numerical values."
    ]),

    # 20. What is a support vector machine (SVM)?
    (r'(what is|explain) (support vector machine|svm)\??', [
        "A Support Vector Machine (SVM) is a supervised learning algorithm used for classification and regression tasks. It works by finding the optimal hyperplane that separates data into classes.",
        "SVMs are powerful tools for classification problems, especially in high-dimensional spaces, as they maximize the margin between data points of different classes.",
        "Support Vector Machines are widely used in applications like image classification, handwriting recognition, and bioinformatics."
    ]),
     # 1. Who made you?
    (r'(who (made|created) you|who is your creator)\??', [
        "I was created by the students of the Artificial Intelligence and Data Science department at Pr Pote Patil College of Engineering in Amravati, Maharashtra.",
        "I was made by the talented students of Pr Pote Patil College's AI and Data Science department, as part of their advanced learning project.",
        "I was created by students from the AI and Data Science program at Pr Pote Patil College, under their innovative efforts in artificial intelligence."
    ]),

    # 2. Who guides you?
    (r'(who guides you|who is your guide)\??', [
        "I am guided by Pratik Angitkar Sir, a dedicated professor in the AI and Data Science department at Pr Pote Patil College of Engineering.",
        "My guidance comes from Pratik Angitkar Sir, who leads the AI and Data Science students at Pr Pote Patil College.",
        "I follow the guidance of Pratik Angitkar Sir, who oversees the AI and Data Science projects at Pr Pote Patil College."
    ]),
     # 1. Why is AI important?
    (r'why is (artificial intelligence|ai) important\??', [
        "AI is important because it automates complex tasks, boosts efficiency, and unlocks new capabilities in various industries like healthcare, finance, and transportation.",
        "AI revolutionizes industries by improving decision-making processes, personalizing user experiences, and providing insights through data analysis.",
        "AI is vital to the future of technology as it enables automation, reduces human error, and optimizes processes, driving innovation across sectors."
    ]),

    # 4. What are the advantages of AI?
    (r'what are the (advantages|benefits) of (artificial intelligence|ai)\??', [
        "AI increases efficiency by automating repetitive tasks and processing large amounts of data quickly. It helps reduce human error and improve decision-making.",
        "AI enables real-time data analysis, providing insights that help businesses make better decisions. It can personalize experiences and deliver consistent performance.",
        "AI can work 24/7 without fatigue, handle complex calculations, and perform tasks faster than humans, leading to greater productivity and cost savings."
    ]),

    # 5. What are the disadvantages of AI?
    (r'what are the (disadvantages|downsides) of (artificial intelligence|ai)\??', [
        "One of the biggest downsides of AI is job displacement, as automation can replace human workers in certain industries.",
        "AI systems may introduce bias if trained on incomplete or biased data, leading to unfair outcomes. Additionally, AI can lead to privacy concerns and data misuse.",
        "Over-reliance on AI could reduce human creativity and problem-solving. It also raises ethical concerns, such as accountability in decision-making systems."
    ]),


    # 7. What are the challenges and future of AI?
    (r'what are the challenges and future of (ai|artificial intelligence)\??', [
        "Challenges for AI include ethical concerns, such as data privacy, algorithmic bias, and the need for transparency in decision-making. Ensuring safety and control of AI systems is also critical.",
        "The future of AI looks promising with advancements in quantum computing, natural language understanding, and autonomous systems. AI is expected to integrate into more areas of life, driving innovation.",
        "AI's future will likely focus on creating more explainable and ethical AI systems, enhancing human-AI collaboration, and addressing the challenges of data governance and cybersecurity."
    ]),

    # 8. What are the types of AI?
    (r'what are the types of (artificial intelligence|ai)\??', [
        "AI is generally categorized into three types: narrow AI, which is designed for specific tasks; general AI, which can perform any intellectual task a human can; and superintelligence, which surpasses human intelligence.",
        "Narrow AI focuses on specific tasks such as facial recognition or language translation, while general AI would have the ability to perform a wide range of tasks.",
        "The types of AI are narrow AI (weak AI), general AI (strong AI), and artificial superintelligence, which exists in theory but not yet in practice."
    ]),

    # 9. What is the difference between AI and machine learning?
    (r'what is the difference between (ai|artificial intelligence) and machine learning\??', [
        "AI is the broader concept of creating intelligent machines, while machine learning is a subset of AI that focuses on enabling machines to learn from data and improve over time.",
        "Machine learning is one of the techniques used to achieve AI, specifically allowing systems to learn patterns and make decisions based on data.",
        "AI encompasses all forms of machine intelligence, while machine learning is specifically about teaching machines to recognize patterns from data."
    ]),
    # Who is Anup?
    (r'who is (anup)\??', [
        "Anup is a student in the Artificial Intelligence and Data Science department at Pr Pote College of Engineering and Management.",
    ]),
    # Who is Anup?
    (r'who is (ansh)\??', [
        "Ansh is a student from the AI and Data Science department at Pr Pote College of Engineering and Management.",
    ]),
    # Who is Anup?
    (r'who is (shrutika)\??', [
        
        "Shrutika is one of the students in the AI and Data Science department at Pr Pote College of Engineering and Management.",
    ]),
    # Who is Anup?
    (r'who is (anuradha)\??', [
        
        "Anuradha is a dedicated student from the AI and Data Science department at Pr Pote College of Engineering and Management.",
    ]),
    # Who is Anup?
    (r'who is (sonal)\??', [
        "Sonal is a student in the Artificial Intelligence and Data Science department at Pr Pote College of Engineering and Management."
    ]),

    # Who is Pratik Angitkar?
    (r'who is (pratik angitkar|professor pratik angitkar)\??', [
        "Pratik Angitkar is a professor in the Artificial Intelligence and Data Science department at Pr Pote College of Engineering and Management.",
        "Professor Pratik Angitkar teaches in the AI and Data Science department at Pr Pote College of Engineering and Management.",
        "Pratik Angitkar is a respected professor from the AI and Data Science department of Pr Pote College of Engineering and Management, guiding students in AI and data science projects."
    ]),

    # What is a Data Scientist?
    (r'(what is|who is) a data scientist\??', [
        "A Data Scientist is a professional who uses their expertise in mathematics, statistics, and programming to analyze and interpret complex data.",
        "A Data Scientist extracts meaningful insights from data, builds predictive models, and helps organizations make data-driven decisions.",
        "Data Scientists are responsible for analyzing data, building machine learning models, and communicating insights to stakeholders."
    ]),
    
    # What is Data Visualization?
    (r'(what is|define) data visualization\??', [
        "Data Visualization is the graphical representation of data, making it easier to understand patterns, trends, and insights.",
        "Data Visualization uses charts, graphs, and plots to help users understand complex datasets and communicate insights effectively.",
        "In Data Visualization, data is presented in a visual context, such as bar charts, pie charts, or scatter plots, to reveal hidden patterns and insights."
    ]),

    # What is a Dataset?
    (r'(what is|define) a dataset\??', [
        "A Dataset is a collection of data, typically organized in rows and columns, where each row represents an instance and each column represents a feature.",
        "A Dataset contains structured data used for analysis, modeling, or machine learning, and can be labeled (for supervised learning) or unlabeled (for unsupervised learning).",
        "In Data Science, a Dataset is a structured collection of data that is used to train models, perform analysis, or generate insights."
    ]),

    # What is Feature Engineering?
    (r'(what is|define) feature engineering\??', [
        "Feature Engineering is the process of selecting, modifying, or creating features from raw data to improve the performance of machine learning models.",
        "In Feature Engineering, new features are created from the existing data to enhance the model’s ability to make accurate predictions.",
        "Feature Engineering involves transforming raw data into meaningful features that help improve the accuracy and performance of machine learning models."
    ])
]


# Default response if no pattern matches
default_responses = [
    "I'm not sure I understand. Could you rephrase that?",
    "I don't have an answer for that yet.",
    "Interesting question! Unfortunately, I don't know how to respond to that.",
    "I'm still learning. Could you try asking something else?"
]
# app.py (continued)

# Let's enhance our chatbot with more advanced pattern matching and features

# Add more sophisticated pattern matching with context awareness
class ContextAwareChatbot:
    def __init__(self):
        self.conversation_context = {}
        self.last_topic = None
        
        # Enhanced patterns with context awareness
        self.topic_patterns = {
            'greeting': {
                'patterns': [r'\b(hello|hi|hey|howdy|greetings)\b', r'good (morning|afternoon|evening)'],
                'responses': [
                    'Hello! How can I help you today?',
                    'Hi there! What can I do for you?',
                    'Hey! Nice to chat with you. How can I assist?'
                ],
                'follow_up': 'How are you doing today?'
            },
            'farewell': {
                'patterns': [r'\b(bye|goodbye|see you|farewell|exit|quit)\b'],
                'responses': [
                    'Goodbye! Come back anytime.',
                    'See you later! Have a great day.',
                    'Farewell! It was nice chatting with you.'
                ]
            },
            'thanks': {
                'patterns': [r'\b(thanks|thank you|appreciate|grateful)\b'],
                'responses': [
                    'You\'re welcome!',
                    'Happy to help!',
                    'No problem at all!'
                ]
            },
            'bot_identity': {
                'patterns': [r'(who are you|what are you|your name|about you)'],
                'responses': [
                    'I\'m a pattern-matching chatbot built with Flask and SQLite.',
                    'I\'m FlaskBot! I was created to demonstrate pattern matching and database storage.',
                    'I\'m a simple chatbot that can recognize patterns in text and respond accordingly.'
                ],
                'follow_up': 'Is there anything specific you\'d like to know about me?'
            },
            'user_feeling': {
                'patterns': [r'i (?:am|feel) (sad|happy|tired|excited|bored|angry|confused)'],
                'responses': {
                    'sad': [
                        'I\'m sorry to hear that you\'re feeling sad. Is there anything I can do to help?',
                        'That\'s unfortunate. Remember that it\'s okay to feel sad sometimes.'
                    ],
                    'happy': [
                        'That\'s great to hear! What made you happy today?',
                        'Wonderful! Happiness is contagious!'
                    ],
                    'tired': [
                        'I hope you can get some rest soon.',
                        'Being tired can be tough. Maybe take a short break?'
                    ],
                    'excited': [
                        'Excitement is wonderful! What are you excited about?',
                        'That\'s great! I hope whatever you\'re excited about goes well!'
                    ],
                    'bored': [
                        'Would you like me to suggest something fun to do?',
                        'Boredom can sometimes lead to creativity!'
                    ],
                    'angry': [
                        'I understand that anger can be difficult. Taking deep breaths sometimes helps.',
                        'I hope whatever made you angry resolves soon.'
                    ],
                    'confused': [
                        'What\'s confusing you? Maybe I can help clarify things.',
                        'Confusion is often the first step to understanding.'
                    ]
                }
            },
            'weather': {
                'patterns': [r'\b(weather|rain|sunny|forecast)\b'],
                'responses': [
                    'I don\'t have access to real-time weather data, but I can tell you about weather-related topics!',
                    'While I can\'t check the current weather for you, I hope it\'s pleasant where you are!'
                ]
            },
            'help': {
                'patterns': [r'\b(help|assist|support|guide)\b'],
                'responses': [
                    'I can help with basic conversations. Try asking me about myself, or just chat with me!',
                    'I\'m here to help! I can respond to greetings, questions about myself, and more.',
                    'Need help? I\'m a simple chatbot, but I\'ll do my best to assist you!'
                ],
                'follow_up': 'Is there something specific you need help with?'
            },
            'learning': {
                'patterns': [r'\b(learn|study|teach|educate)\b'],
                'responses': [
                    'Learning is a great way to grow! What would you like to learn about today?',
                    'I can help you with topics like AI, data science, machine learning, and more. Just ask!',
                    'Studying something new? Let me guide you through it. What’s the topic on your mind?'
                ],
                'follow_up': 'What would you like to explore today? I’m here to help you learn!'
            },
            'greetingss': {
                'patterns': [r'(good morning|good afternoon|good evening)'],
                'responses': [
                    'Good morning! How can I assist you today?',
                    'Good afternoon! Hope your day’s going well. Need help with something?',
                    'Good evening! Ready to dive into some learning or just chat? I’m here!'
                ],
                'follow_up': 'Let me know how I can assist you today. Any topics you’re curious about?'
            },
            'bye': {
                'patterns': [r'(bye|goodbye|see you|later)'],
                'responses': [
                    'Goodbye! Feel free to reach out anytime you need help!',
                    'See you soon! Take care!',
                    'Goodbye, and have a great day ahead!'
                ],
                'follow_up': 'If you need anything in the future, don’t hesitate to ask!'
            }
            
        }
        
        # For when we don't understand the user
        self.default_responses = [
            "I'm not sure I understand. Could you rephrase that?",
            "I don't have a response for that yet.",
            "That's interesting, but I'm not sure how to respond.",
            "I'm still learning and didn't quite catch that. Could you try saying it differently?"
        ]
    
    def extract_feeling(self, text):
        for feeling in ['sad', 'happy', 'tired', 'excited', 'bored', 'angry', 'confused']:
            if re.search(r'i (?:am|feel) ' + feeling, text.lower()):
                return feeling
        return None
    
    def get_response(self, user_input):
        user_input_lower = user_input.lower()
        
        # Check for user feelings first (context-specific responses)
        feeling = self.extract_feeling(user_input_lower)
        if feeling:
            self.last_topic = 'user_feeling'
            self.conversation_context['feeling'] = feeling
            return random.choice(self.topic_patterns['user_feeling']['responses'][feeling])
        
        # Check other patterns
        for topic, data in self.topic_patterns.items():
            for pattern in data['patterns']:
                if re.search(pattern, user_input_lower):
                    self.last_topic = topic
                    
                    # Basic response
                    if isinstance(data['responses'], list):
                        response = random.choice(data['responses'])
                    else:
                        # This handles nested response structures
                        response = "I understood your topic, but couldn't find a specific response."
                    
                    # Add follow-up if available and not recently used
                    if 'follow_up' in data and topic != self.conversation_context.get('last_follow_up_topic'):
                        self.conversation_context['last_follow_up_topic'] = topic
                        response += " " + data['follow_up']
                    
                    return response
        
        # No pattern matched
        self.last_topic = None
        return random.choice(self.default_responses)

# Create an instance of our enhanced chatbot
chatbot = ContextAwareChatbot()

# Update the get_bot_response function to use our enhanced chatbot
def get_bot_response(user_input):
    return chatbot.get_response(user_input)

# Add a new route to get chat statistics
@app.route('/stats')
def view_stats():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Get total number of conversations
    cursor.execute("SELECT COUNT(*) as total FROM conversations")
    total = cursor.fetchone()['total']
    
    # Get most common user inputs
    cursor.execute("""
        SELECT user_input, COUNT(*) as count 
        FROM conversations 
        GROUP BY user_input 
        ORDER BY count DESC 
        LIMIT 5
    """)
    common_inputs = cursor.fetchall()
    
    # Get most recent conversations
    cursor.execute("""
        SELECT * FROM conversations
        ORDER BY timestamp DESC
        LIMIT 10
    """)
    recent = cursor.fetchall()
    
    conn.close()
    
    return render_template('stats.html', 
                          total=total, 
                          common_inputs=common_inputs, 
                          recent=recent)

# Add a feedback mechanism
@app.route('/feedback', methods=['POST'])
def save_feedback():
    data = request.json
    conversation_id = data.get('conversation_id')
    rating = data.get('rating')
    feedback_text = data.get('feedback', '')
    
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # Check if feedback table exists, if not create it
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        conversation_id INTEGER,
        rating INTEGER,
        feedback_text TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (conversation_id) REFERENCES conversations (id)
    )
    ''')
    
    cursor.execute(
        "INSERT INTO feedback (conversation_id, rating, feedback_text, timestamp) VALUES (?, ?, ?, ?)",
        (conversation_id, rating, feedback_text, datetime.datetime.now())
    )
    
    conn.commit()
    conn.close()
    
    return jsonify({'status': 'success'})

# Add a route to train/add new patterns
@app.route('/add_pattern', methods=['GET', 'POST'])
def add_pattern():
    if request.method == 'POST':
        data = request.form
        pattern = data.get('pattern')
        response = data.get('response')
        
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        
        # Check if patterns table exists, if not create it
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS custom_patterns (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pattern TEXT NOT NULL,
            response TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        cursor.execute(
            "INSERT INTO custom_patterns (pattern, response) VALUES (?, ?)",
            (pattern, response)
        )
        
        conn.commit()
        conn.close()
        
        # Reload patterns (in a real app, you'd want a more sophisticated way to do this)
        load_custom_patterns()
        
        return redirect('/add_pattern')
    
    return render_template('add_pattern.html')

def load_custom_patterns():
    # This would load custom patterns from the database
    # and add them to the chatbot's patterns in a real implementation
    pass

def get_bot_response(user_input):
    # Convert to lowercase for easier matching
    user_input = user_input.lower()
    
    # Try to match the input with a pattern
    for pattern, responses in patterns:
        if re.search(pattern, user_input):
            return random.choice(responses)
    
    # If no pattern matches, return a default response
    return random.choice(default_responses)

def save_conversation(user_input, bot_response):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    cursor.execute(
        "INSERT INTO conversations (user_input, bot_response, timestamp) VALUES (?, ?, ?)",
        (user_input, bot_response, datetime.datetime.now())
    )
    
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def process_input():
    user_input = request.json.get('user_input', '')
    
    if not user_input.strip():
        return jsonify({'response': 'Please say something!'})
    
    bot_response = get_bot_response(user_input)
    
    # Save the conversation to the database
    save_conversation(user_input, bot_response)
    
    return jsonify({'response': bot_response})

@app.route('/history')
def view_history():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM conversations ORDER BY timestamp DESC")
    conversations = cursor.fetchall()
    
    conn.close()
    
    return render_template('history.html', conversations=conversations)

if __name__ == '__main__':
    app.run(debug=True)