"""
Gemini LLM agent subprocess for the ngram CLI.

DOCS: docs/llm_agents/PATTERNS_Provider_Specific_LLM_Subprocesses.md
"""

import argparse
import json
import os
import sys # Import sys for sys.stderr
import google.genai as genai # Update to use google.genai
from dotenv import dotenv_values # Import dotenv

def main():
    parser = argparse.ArgumentParser(description="Gemini LLM agent for ngram CLI.")
    parser.add_argument("-p", "--prompt", required=True, help="User prompt.")
    parser.add_argument("--system-prompt", default="", help="System prompt.")
    parser.add_argument("--output-format", default="stream-json", help="Output format (stream-json or text).")
    parser.add_argument("--allowed-tools", help="Comma-separated list of allowed tools.")
    parser.add_argument("--api-key", help="Gemini API key.")

    args = parser.parse_args()

    # Load from .env file first
    config = dotenv_values()
    
    # Configure Gemini API
    api_key = args.api_key or config.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        print(json.dumps({"error": "GEMINI_API_KEY not found. Please set it in a .env file, as an environment variable, or pass it with --api-key."}), flush=True)
        exit(1)
    genai.configure(api_key=api_key)

    # --- Start Debugging: List available models ---
    try:
        print("Available Gemini models:", file=os.stderr)
        for m in genai.list_models():
            if "generateContent" in m.supported_generation_methods:
                print(f"- {m.name} (supports generateContent)", file=os.stderr)
            else:
                print(f"- {m.name}", file=os.stderr)
    except Exception as e:
        print(f"Error listing models: {e}", file=os.stderr)
    # --- End Debugging ---

    # Initialize the model
    # TODO: Allow model selection
    model = genai.GenerativeModel('gemini-pro')

    contents = []
    if args.system_prompt:
        contents.append({'role': 'user', 'parts': [args.system_prompt]})
        contents.append({'role': 'model', 'parts': ['ok']}) # Gemini expects a reply from model if user starts with system prompt
    
    contents.append({'role': 'user', 'parts': [args.prompt]})

    try:
        if args.output_format == "stream-json":
            # For streaming, we'll try to emulate the Claude JSON output for tool_code/text
            response_parts = []
            
            # Start a chat session
            chat_session = model.start_chat(history=contents[:-1]) # history is everything except the last user prompt

            # Send the last user prompt
            stream = chat_session.send_message(contents[-1]['parts'][0], stream=True)

            for chunk in stream:
                if chunk.text:
                    response_parts.append(chunk.text)
                    # For now, just stream text. More complex tool_use parsing might be needed later.
                    print(json.dumps({
                        "type": "assistant",
                        "message": {
                            "content": [
                                {"type": "text", "text": chunk.text}
                            ]
                        }
                    }), flush=True)
            
            # Send a final 'result' type message, combining all parts
            final_response_text = "".join(response_parts)
            print(json.dumps({
                "type": "result",
                "result": final_response_text
            }), flush=True)

        else: # text output format
            chat_session = model.start_chat(history=contents[:-1])
            response = chat_session.send_message(contents[-1]['parts'][0])
            print(response.text, flush=True)

    except Exception as e:
        print(json.dumps({"error": str(e)}), flush=True)
        exit(1)

if __name__ == "__main__":
    main()
