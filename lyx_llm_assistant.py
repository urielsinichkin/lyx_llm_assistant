import os
import sys
import json
import time
from pathlib import Path
from typing import Optional, Dict, Any
import openai
from dotenv import load_dotenv

class LyxLLMAssistant:
    def __init__(self):
        load_dotenv()
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.lyx_pipe_in = None
        self.lyx_pipe_out = None
        self.setup_lyx_pipes()

    def setup_lyx_pipes(self):
        """Setup communication pipes with LyX."""
        # Windows-specific LyX 2.3 pipe location
        lyxpipe_path = os.getenv("LYXPIPE_PATH", r"C:\Users\slons\AppData\Roaming\LyX2.3\lyxpipe")
        
        try:
            self.lyx_pipe_in = open(f"{lyxpipe_path}.in", "w")
            self.lyx_pipe_out = open(f"{lyxpipe_path}.out", "r")
        except FileNotFoundError:
            print(f"Error: LyX pipes not found at {lyxpipe_path}")
            print("Please ensure:")
            print("1. LyX is running")
            print("2. Server pipe support is enabled in Tools > Preferences > Paths")
            print("3. The pipe path is set to:", lyxpipe_path)
            print("\nRun test_lyx_pipe.py to verify your configuration.")
            sys.exit(1)
        except PermissionError:
            print(f"Error: Permission denied accessing LyX pipes at {lyxpipe_path}")
            print("Please ensure you have the correct permissions.")
            sys.exit(1)

    def get_current_context(self) -> str:
        """Get the current context from LyX editor."""
        # Send LYXCMD:buffer-get-content
        self.lyx_pipe_in.write("LYXCMD:buffer-get-content\n")
        self.lyx_pipe_in.flush()
        
        # Read response
        response = self.lyx_pipe_out.readline().strip()
        return response

    def suggest_completion(self, context: str) -> str:
        """Get completion suggestion from OpenAI."""
        try:
            response = self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant for LyX document editing. "
                                                "Suggest completions that maintain academic writing style."},
                    {"role": "user", "content": f"Complete the following text:\n{context}"}
                ],
                max_tokens=150,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error getting suggestion: {str(e)}"

    def insert_text(self, text: str):
        """Insert text at current cursor position."""
        # Escape special characters
        text = text.replace("\\", "\\\\").replace('"', '\\"')
        cmd = f'LYXCMD:server-set-xy:{{"text": "{text}"}}\n'
        self.lyx_pipe_in.write(cmd)
        self.lyx_pipe_in.flush()

    def run(self):
        """Main loop to watch for requests and provide suggestions."""
        print("LyX LLM Assistant started. Watching for changes...")
        print("Press Ctrl+C to stop")
        try:
            while True:
                context = self.get_current_context()
                if context:
                    suggestion = self.suggest_completion(context)
                    self.insert_text(suggestion)
                time.sleep(1)  # Avoid excessive CPU usage
        except KeyboardInterrupt:
            print("\nShutting down LyX LLM Assistant...")
        except Exception as e:
            print(f"\nError: {str(e)}")
        finally:
            if self.lyx_pipe_in:
                self.lyx_pipe_in.close()
            if self.lyx_pipe_out:
                self.lyx_pipe_out.close()

if __name__ == "__main__":
    assistant = LyxLLMAssistant()
    assistant.run() 