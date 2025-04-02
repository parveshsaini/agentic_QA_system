# BTP 2025

## Local Dev Setup:

To set up the project, follow these steps:

1. Install Python and create a virtual environment:
   ```bash
   python -m venv venv
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create `.env` file and add your `OPEN_AI_API_KEY`, `TAVILY_API_KEY`, and `LANGCHAIN_API_KEY`.

4. Run `prepare_vector_db.py` module once to prepare both vector databases.
   ```bash
   python src\prepare_vector_db.py
   ```
5. Run the app:
   ```bash
   python src\app.py
   ```
Open the Gradio URL generated in the terminal and start chatting.

*Sample questions are available in `sample_questions.txt`.*

---

## Key Frameworks and Libraries

- **LangChain:** [Introduction](https://python.langchain.com/docs/get_started/introduction)
- **LangGraph**
- **LangSmith**
- **Gradio:** [Documentation](https://www.gradio.app/docs/interface)
- **OpenAI:** [Developer Quickstart](https://platform.openai.com/docs/quickstart?context=python)
- **Tavily Search**
---