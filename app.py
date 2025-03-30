import gradio as gr
from gradio_client import Client
import json

def read_file(file):
    if file is None:
        return ""
    with open(file.name, 'r', encoding='utf-8') as f:
        content = f.read()
    return content

def analyze_toxicity(text_input, file_input, safer_value):
    # Initialize the client
    client = Client("duchaba/Friendly_Text_Moderation")
    
    # Get the text content (either from text input or file)
    content = read_file(file_input) if file_input else text_input
    if not content:
        return "Please provide either text input or upload a file."
    
    # Split the conversation into lines
    messages = [msg.strip() for msg in content.split('\n') if msg.strip()]
    
    results = []
    toxicity_by_user = {}
    
    # Analyze each message
    for message in messages:
        if not message:
            continue
        
        try:
            parts = message.split(':', 1)
            if len(parts) != 2:
                continue
            
            user = parts[0].strip()
            msg_content = parts[1].strip()

            result = client.predict(
                msg=msg_content,
                safer=safer_value,
                api_name="/fetch_toxicity_level"
            )

            toxicity_data = json.loads(result[1])

            # Check toxicity correctly
            is_toxic = toxicity_data.get('is_flagged', False)
            toxicity_score = toxicity_data.get('max_value', 0.0) if is_toxic else 0.0
            toxicity_type = toxicity_data.get('max_key', 'None') if is_toxic else 'None'

            # Accumulate scores per user
            if user not in toxicity_by_user:
                toxicity_by_user[user] = []
            toxicity_by_user[user].append((toxicity_score, toxicity_type))
                
        except Exception as e:
            results.append(f"Error analyzing message: {str(e)}")
    
    # Calculate average toxicity per user
    summary = []
    for user, scores in toxicity_by_user.items():
        avg_toxicity = sum(score for score, _ in scores) / len(scores)
        summary.append((user, avg_toxicity))
    
    # Sort by toxicity score (highest to lowest)
    summary.sort(key=lambda x: x[1], reverse=True)
    
    # Format results
    output = "Toxicity Analysis Results:\n\n"
    for user, scores in toxicity_by_user.items():
        avg_toxicity = sum(score for score, _ in scores) / len(scores)
        output += f"{user}: {avg_toxicity:.2%} average toxicity\n"
    
        # List each toxic message type specifically
        for idx, (score, t_type) in enumerate(scores, 1):
            if score > 0:
                output += f"   - Message {idx}: {t_type.capitalize()} ({score:.2%})\n"
            
    output += "\n"
    
    return output

# Create the Gradio interface
iface = gr.Interface(
    fn=analyze_toxicity,
    inputs=[
        gr.Textbox(
            label="Enter conversation text (format: 'User: Message' per line)",
            placeholder="John: Hello!\nJane: Hi there!",
            lines=10
        ),
        gr.File(
            label="Or upload a .txt file",
            file_types=[".txt"]
        ),
        gr.Slider(
            minimum=0.01,
            maximum=0.5,
            value=0.02,
            label="Personalize Safer Value (larger value is less safe)"
        )
    ],
    outputs=gr.Textbox(label="Analysis Results", lines=10),
    title="Conversation Toxicity Analyser",
    description="Analyse the toxicity levels in a conversation between multiple participants. Enter text directly or upload a .txt file.",
)

if __name__ == "__main__":
    iface.launch()
