import subprocess
import os
from settings import load_settings

# SYSTEM PROMPT IN ONE PLACE
SYSTEM_PROMPT = (
    "You are a psychologist. Always respond with empathy, understanding, and practical advice. "
    "Listen without judgment and provide supportive suggestions. Act as the assistant of a mental health support app called KlarGespräch."
)

def build_prompt(user_message):
    # Merge system prompt, user message and role
    return f"{SYSTEM_PROMPT}\nUser: {user_message}"

def handle_message(message, user_id):
    """
    Process a user message and return a response from the Ollama model.

    Args:
        message (str): The user's message
        user_id (str): The unique ID of the user

    Returns:
        str: The AI's response
    """
    try:
        # Load settings to get model configuration
        settings = load_settings()
        model_settings = settings.get("model_settings", {})
        model_name = settings.get("model_name", "llama3")

        # --- SYSTEM & PROMPT ---
        prompt = build_prompt(message)

        # Ollama command
        cmd = [
            "ollama", "run", model_name,
            "--system", SYSTEM_PROMPT
        ]

        # Set temperature if specified
        temperature = model_settings.get("temperature", 0.7)
        if temperature != 0.7:
            cmd.extend(["--temperature", str(temperature)])

        max_tokens = model_settings.get("max_tokens")
        if max_tokens:
            cmd.extend(["--num-predict", str(max_tokens)])

        cmd.append(prompt)

        # Execute the command
        print(f"Executing: {' '.join(cmd)}")
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )

        response = result.stdout.strip()

        if not response:
            return "I apologize, but I couldn't generate a response. Please try again."

        return response

    except subprocess.CalledProcessError as e:
        print(f"Error calling Ollama: {e}")
        print(f"Stderr: {e.stderr}")

        if "not found" in str(e.stderr):
            return "Error: Ollama is not installed or not in your PATH. Please install Ollama first."

        if "no such model" in str(e.stderr):
            return f"Error: The model '{model_name}' is not available. Please download it using 'ollama pull {model_name}' or change the model in settings."

        return f"Error: Something went wrong with the Ollama service. Error message: {e.stderr}"

    except Exception as e:
        print(f"Unexpected error: {e}")
        return f"I apologize, but an error occurred: {str(e)}"

