"""
CHATBOT MINI PROJECT
A conversational chatbot built with NLTK for NLP and Tkinter for GUI
Features: Intent recognition, pattern matching, and conversational responses
"""

import tkinter as tk
from tkinter import scrolledtext, messagebox
import random
import re
from datetime import datetime
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet')

try:
    nltk.data.find('corpora/omw-1.4')
except LookupError:
    nltk.download('omw-1.4')


class ChatBot:
    """Chatbot class with NLP capabilities"""

    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))

        # Intent-based responses
        self.intents = {
            'greeting': {
                'patterns': ['hello', 'hi', 'hey', 'greetings', 'howdy'],
                'responses': [
                    'Hello! How can I help you today?',
                    'Hi there! Nice to meet you!',
                    'Hey! What can I do for you?',
                    'Greetings! How are you doing?'
                ]
            },
            'goodbye': {
                'patterns': ['bye', 'goodbye', 'see you', 'farewell', 'take care', 'exit'],
                'responses': [
                    'Goodbye! Have a great day!',
                    'See you later! Take care!',
                    'Bye! Thanks for chatting with me!',
                    'Farewell! Come back soon!'
                ]
            },
            'name': {
                'patterns': ['what is your name', 'who are you', 'tell me your name', 'your name'],
                'responses': [
                    'I\'m ChatBot, your friendly AI assistant!',
                    'My name is ChatBot. Nice to meet you!',
                    'You can call me ChatBot!'
                ]
            },
            'how_are_you': {
                'patterns': ['how are you', 'how do you do', 'how\'s it going', 'what\'s up'],
                'responses': [
                    'I\'m doing great, thanks for asking!',
                    'I\'m functioning perfectly! How about you?',
                    'All systems running smoothly! How are you?'
                ]
            },
            'time': {
                'patterns': ['what time is it', 'tell me the time', 'current time', 'what\'s the time'],
                'responses': None  # Dynamic response
            },
            'help': {
                'patterns': ['help', 'can you help', 'assistance', 'support', 'aid'],
                'responses': [
                    'Of course! I can help with greetings, answer questions about myself, tell you the time, and have a friendly conversation.',
                    'Sure! Try asking me about: greetings, my name, the time, or just chat with me!'
                ]
            },
            'gratitude': {
                'patterns': ['thank you', 'thanks', 'appreciate', 'grateful', 'thank', 'thx'],
                'responses': [
                    'You\'re welcome!',
                    'Happy to help!',
                    'My pleasure!',
                    'Anytime! Glad I could assist!'
                ]
            },
            'weather': {
                'patterns': [
                    'what is the weather',
                    'how is the weather',
                    'what is the weather like',
                    'is it raining',
                    'will it rain today',
                    'weather today'
                ],
                'responses': [
                    'I cannot check live weather right now.',
                    'I do not have access to live weather information.',
                    'You can check a weather app for the latest forecast.'
                ]
            },
            'age': {
                'patterns': [
                    'how old are you',
                    'what is your age',
                    'do you have an age'
                ],
                'responses': [
                    'I am a chatbot, so I do not have an age.',
                    'I do not have an age like a human.',
                    'Age does not really apply to me.'
                ]
            },
            'creator': {
                'patterns': [
                    'who created you',
                    'who developed you',
                    'who built you',
                    'who is your creator'
                ],
                'responses': [
                    'I was created as a Python chatbot project.',
                    'I was developed using Python, NLTK and Tkinter.',
                    'I am a chatbot created using Python programming.'
                ]
            },
            'capabilities': {
                'patterns': [
                    'what can you do',
                    'what are your capabilities',
                    'what features do you have',
                    'what capabilities do you have'
                ],
                'responses': [
                    'I can answer simple questions and have basic conversations.',
                    'I can respond to different messages using predefined intents.',
                    'I can help with basic conversation and simple questions.'
                ]
            },
            'joke': {
                'patterns': [
                    'tell me a joke',
                    'tell me something funny',
                    'make me laugh',
                    'say something funny'
                ],
                'responses': [
                    'Why did the computer go to the doctor? Because it had a virus!',
                    'Why was the computer cold? It left its Windows open!',
                    'Why did the programmer quit his job? Because he did not get arrays!'
                ]
            },
            'compliment': {
                'patterns': [
                    'you are great',
                    'you are awesome',
                    'you are smart',
                    'you are helpful',
                    'nice chatbot',
                    'you are amazing'
                ],
                'responses': [
                    'Thank you! That is very kind of you.',
                    'Thanks! I appreciate that.',
                    'I am glad you think so!'
                ]
            },
            'favorite': {
                'patterns': [
                    'what is your favorite color',
                    'what is your favorite food',
                    'what is your favorite movie',
                    'what is your favorite game'
                ],
                'responses': [
                    'I do not have personal favorites.',
                    'I do not have personal preferences like humans do.',
                    'I do not have favorites, but I enjoy chatting with you!'
                ]
            },
            'study': {
                'patterns': [
                    'help me study',
                    'help me learn',
                    'i want to study',
                    'study help',
                    'can you help me learn',
                    'can you help me study'
                ],
                'responses': [
                    'Sure! Tell me what subject you want to study.',
                    'Of course! What topic would you like to learn?',
                    'Sure! Tell me the topic and I will try to help.'
                ]
            },
            'food': {
                'patterns': [
                    'i am hungry',
                    'what should i eat',
                    'suggest some food',
                    'recommend some food'
                ],
                'responses': [
                    'How about having your favorite meal?',
                    'You could try something healthy and delicious.',
                    'Maybe have something you really enjoy!'
                ]
            },
            'default': {
                'patterns': [],
                'responses': [
                    'That\'s interesting! Tell me more.',
                    'I understand. Can you elaborate?',
                    'Hmm, I\'m still learning. Could you rephrase that?',
                    'That\'s a good point! Anything else?',
                    'I\'m not quite sure about that, but I\'m learning!'
                ]
            }
        }

    def preprocess_text(self, text):
        """Preprocess text: tokenize, lowercase, remove stopwords, lemmatize"""
        text = text.lower()
        tokens = word_tokenize(text)
        tokens = [self.lemmatizer.lemmatize(token) for token in tokens
                  if token.isalnum() and token not in self.stop_words]
        return tokens

    def get_response(self, user_input):
        """Generate a response based on user input"""

        # Check for time intent
        if any(word in user_input.lower() for word in ['time', 'what time']):
            current_time = datetime.now().strftime('%I:%M %p')
            return f'The current time is {current_time}.'

        user_tokens = set(self.preprocess_text(user_input))

        best_intent = None
        best_match = 0

        # Compare user input with patterns
        for intent_name, intent_data in self.intents.items():
            if intent_name == 'default':
                continue

            for pattern in intent_data['patterns']:
                pattern_tokens = set(self.preprocess_text(pattern))

                # Calculate similarity
                if pattern_tokens:
                    similarity = len(user_tokens & pattern_tokens) / len(user_tokens | pattern_tokens)

                    if similarity > best_match:
                        best_match = similarity
                        best_intent = intent_name

        # Threshold for pattern matching
        if best_match > 0.3 and best_intent:
            responses = self.intents[best_intent]['responses']
            if responses:
                return random.choice(responses)

        # Default response
        return random.choice(self.intents['default']['responses'])


class ChatBotGUI:
    """GUI for the chatbot using Tkinter"""

    def __init__(self, root):
        self.root = root
        self.root.title('ChatBot - Powered by NLTK & Tkinter')
        self.root.geometry('500x600')
        self.root.configure(bg='#f0f0f0')

        self.chatbot = ChatBot()
        self.chat_history = []

        # Create GUI components
        self.create_widgets()

        # Bind Enter key to send message
        self.root.bind('<Return>', lambda event: self.send_message())

    def create_widgets(self):
        """Create all GUI elements"""

        # Title
        title_frame = tk.Frame(self.root, bg='#2c3e50')
        title_frame.pack(fill=tk.X, padx=0, pady=0)

        title = tk.Label(
            title_frame,
            text='🤖 ChatBot Assistant',
            font=('Arial', 18, 'bold'),
            bg='#2c3e50',
            fg='white',
            pady=15
        )
        title.pack()

        # Chat display area
        chat_frame = tk.Frame(self.root, bg='white')
        chat_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.chat_display = scrolledtext.ScrolledText(
            chat_frame,
            wrap=tk.WORD,
            state='disabled',
            font=('Arial', 10),
            bg='white',
            fg='#2c3e50',
            height=25
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True)

        # Configure tags for formatting
        self.chat_display.tag_config('user', foreground='#3498db', font=('Arial', 10, 'bold'))
        self.chat_display.tag_config('bot', foreground='#27ae60', font=('Arial', 10, 'bold'))
        self.chat_display.tag_config('timestamp', foreground='#95a5a6', font=('Arial', 8))

        # Input frame
        input_frame = tk.Frame(self.root, bg='#ecf0f1')
        input_frame.pack(fill=tk.X, padx=10, pady=10)

        # User input field
        self.user_input = tk.Entry(
            input_frame,
            font=('Arial', 11),
            bg='white',
            fg='#2c3e50',
            relief=tk.FLAT
        )
        self.user_input.pack(fill=tk.X, side=tk.LEFT, padx=(0, 10), ipady=8)
        self.user_input.focus()

        # Send button
        send_btn = tk.Button(
            input_frame,
            text='Send',
            command=self.send_message,
            bg='#3498db',
            fg='white',
            font=('Arial', 10, 'bold'),
            relief=tk.FLAT,
            padx=20,
            cursor='hand2'
        )
        send_btn.pack(side=tk.LEFT, padx=(0, 5))

        # Clear button
        clear_btn = tk.Button(
            input_frame,
            text='Clear',
            command=self.clear_chat,
            bg='#e74c3c',
            fg='white',
            font=('Arial', 10, 'bold'),
            relief=tk.FLAT,
            padx=20,
            cursor='hand2'
        )
        clear_btn.pack(side=tk.LEFT)

        # Welcome message
        self.display_welcome_message()

    def display_welcome_message(self):
        """Display a welcome message when the chatbot starts"""
        welcome = "Welcome to ChatBot! 👋\n\nYou can try asking me:\n• Greetings (hello, hi, hey)\n• My name\n• The current time\n• General questions\n• Type 'exit' or 'bye' to leave\n\nType your message below and press Enter or click Send!\n"

        self.chat_display.config(state='normal')
        self.chat_display.insert(tk.END, welcome, 'bot')
        self.chat_display.insert(tk.END, '\n' + '=' * 50 + '\n\n')
        self.chat_display.config(state='disabled')
        self.chat_display.see(tk.END)

    def send_message(self):
        """Send user message and get bot response"""
        user_message = self.user_input.get().strip()

        if not user_message:
            return

        # Display user message
        self.display_message('You', user_message, 'user')

        # Get bot response
        bot_response = self.chatbot.get_response(user_message)
        self.display_message('Bot', bot_response, 'bot')

        # Store in history
        self.chat_history.append({
            'user': user_message,
            'bot': bot_response,
            'timestamp': datetime.now().strftime('%H:%M:%S')
        })

        # Clear input field
        self.user_input.delete(0, tk.END)

        # Check for exit intent
        if any(word in user_message.lower() for word in ['exit', 'bye', 'goodbye']):
            self.root.after(1000, self.root.quit)

    def display_message(self, sender, message, tag):
        """Display a message in the chat window"""
        self.chat_display.config(state='normal')

        timestamp = datetime.now().strftime('%H:%M:%S')
        self.chat_display.insert(tk.END, f'{sender} [{timestamp}]: ', tag)
        self.chat_display.insert(tk.END, f'{message}\n\n')

        self.chat_display.config(state='disabled')
        self.chat_display.see(tk.END)

    def clear_chat(self):
        """Clear the chat history and display"""
        if messagebox.askyesno('Clear Chat', 'Are you sure you want to clear the chat history?'):
            self.chat_history = []
            self.chat_display.config(state='normal')
            self.chat_display.delete(1.0, tk.END)
            self.chat_display.config(state='disabled')
            self.display_welcome_message()


def main():
    """Main function to run the chatbot"""
    root = tk.Tk()
    gui = ChatBotGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()