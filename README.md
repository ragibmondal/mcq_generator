This app helps you create multiple-choice questions (MCQs) from your documents.

**What You Need**

* **Python:** Make sure you have Python installed on your computer.
* **Libraries:** Install these: 
    * `streamlit`
    * `langchain`
    * `pdfkit`
* **API Key:** If your language model requires one, get it and add it to the `src/helper.py` file.

**How to Run**

1. **Open your terminal.**
2. **Go to the app's folder.**
3. **Type this and press Enter:** `streamlit run app.py`
4. **The app will open in your web browser.**

**Using the App**

1. **Upload your file (text or PDF).**
2. **Choose how many questions you want.**
3. **Pick the difficulty (Easy, Medium, Hard).**
4. **Select the language.**
5. **Click "Generate."**
6. **Wait for the questions to appear.**
7. **Download as a Word or PDF file.**

**Key Files**

* `app.py`: The main file that runs the app.
* `src/helper.py`: This is where you set up your language model.

**Need Help?**

If you have any trouble, check the terminal or the app's console for error messages.
