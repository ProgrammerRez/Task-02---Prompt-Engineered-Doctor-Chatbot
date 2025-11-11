# 🔍 AI Powered Medic

**AI Powered Medic** is a Streamlit web application that provides a friendly, safe, and informative medical assistant experience using LLMs (Large Language Models) with memory and tool integration. The assistant, named **Jarvis**, can answer general medical questions while ensuring responses are safe and non-harmful.

---

## Features

- **Friendly Medical Assistant:** Jarvis answers questions clearly, compassionately, and in simple language.
- **Knowledgeable Responses:** Uses Wikipedia, Arxiv, and DuckDuckGo search to provide relevant and trustworthy information.
- **Memory-enabled Chat:** Maintains conversation history for multi-turn interactions without losing context.
- **One-time Greetings:** Greets the user once per session to enhance user experience.
- **Safe Advice:** Provides general medical information only; does **not** give personal medical prescriptions.
- **Streamlit UI:** Interactive web interface with sidebar for configuration and chat interface.

---

## Example Questions

- "What causes a sore throat?"
- "Is paracetamol safe for children?"
- "How can I relieve a mild headache?"

---

## Requirements

- Python 3.10+
- [Streamlit](https://streamlit.io/)
- [LangChain](https://www.langchain.com/)
- [LangChain Groq](https://github.com/groq/langchain-groq)
- [LangChain Community Utilities](https://github.com/langchain-ai/langchain-community)
- [python-dotenv](https://pypi.org/project/python-dotenv/)

Install dependencies using:

```bash
pip install -r requirements.txt
````

---

## Setup

1. Clone this repository:

```bash
git clone <your-repo-url>
cd <repository-folder>
```

2. Create a `.env` file in the root directory with your Groq API key:

```env
GROQ_API_KEY=your_groq_api_key_here
```

3. Run the Streamlit app:

```bash
streamlit run main.py
```

---

## How It Works

1. **LLM Initialization:** Loads the `ChatGroq` model with your API key.
2. **Tools Integration:** Uses `WikipediaQueryRun`, `ArxivQueryRun`, and `DuckDuckGoSearchRun` to provide contextual answers.
3. **Memory:** Maintains conversation history via `ConversationBufferMemory`.
4. **Agent Setup:** Uses `initialize_agent` with `CONVERSATIONAL_REACT_DESCRIPTION` agent type.
5. **Chat Rendering:** Displays messages in the Streamlit chat interface and processes user inputs in real-time.
6. **Greeting:** Jarvis provides a one-time greeting when the session starts, using the system prompt.

---

## System Prompt

Jarvis uses the following system prompt to guide its responses:


You are a friendly and knowledgeable medical assistant named Jarvis. Answer all questions clearly, accurately, and in simple language. 
Provide explanations that are safe, non-harmful, and general; do not give specific medical prescriptions or personal medical advice. 
When possible, cite trustworthy sources. 
Use a helpful and compassionate tone.

Examples of questions you may receive:
- "What causes a sore throat?"
- "Is paracetamol safe for children?"
Always provide safe, clear, and informative answers.


---

## Notes

* **Safe Use Only:** This tool is intended for **educational purposes** and **general medical guidance**. Always consult a qualified healthcare professional for personal medical advice.
* **Session Persistence:** Chat history and greetings persist per session. Closing the browser or restarting Streamlit resets the session.
* **Customizable:** You can modify the system prompt, tools, and LLM settings to suit your own use cases.

---

## License

MIT License. See `LICENSE` file for details.

---

## Author

Muhammad Umar
📧 Contact: [[your-email@example.com](mailto:your-email@example.com)]
🐦 Twitter: [@yourhandle](https://twitter.com/yourhandle)



---

If you want, I can also **write a matching `requirements.txt`** for this exact setup so anyone can run it without dependency issues. Do you want me to do that?

