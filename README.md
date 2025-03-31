# Conversation Toxicity Analyser

A simple web-based application built with Python and Gradio, designed to analyse text conversations and identify toxicity levels of participants. Users can either paste conversation text or upload a `.txt` file containing conversation logs formatted as "User: Message".

The idea was to build something for gaming companies to use to automate the banning of toxic players who use toxicity within the game chat.

The application utilises the **Friendly Text Moderation** API hosted on Hugging Face to:
- Detect toxic messages in conversations.
- Calculate average toxicity scores for each participant.
- Identify and display the specific toxicity categories flagged (e.g., harassment, hate speech, sexual content).

### Try the App:
https://huggingface.co/spaces/HeyiTzSully/conversation-toxicity-analyser

### Features:
- Easy-to-use web interface built with Gradio.
- Customizable toxicity sensitivity using the safer value slider.
- Supports direct text input and `.txt` file uploads.
- Provides detailed analysis results including message-level toxicity classification.

### Technologies Used:
- **Python**
- **Gradio** for rapid UI development
- **Gradio Client** for API interaction
- **Hugging Face Spaces** for seamless deployment

### How to Use:
- Paste your conversation into the provided text box, or upload a conversation file (`.txt`).
- Adjust the sensitivity slider as needed.
- Click the "Analyse" button to view the toxicity analysis results.

### Deployment:
Deployed quickly and easily using Hugging Face Spaces.

### Future Enhancements:
- Visualisation of results through interactive charts.
- Downloadable reports in PDF or CSV format.

### License:
This project is open-source and available under the MIT License.

