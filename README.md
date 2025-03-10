# LyX LLM Assistant

A LyX add-on that provides intelligent text suggestions and completions using Large Language Models (LLMs).

## Features

- Real-time text completion suggestions
- Academic writing style assistance
- Seamless integration with LyX editor
- Powered by OpenAI's GPT models

## Prerequisites

- Windows 10 or later
- Python 3.8 or higher
- LyX 2.3 or higher
- OpenAI API key

## Installation

1. Clone this repository:
   ```powershell
   git clone https://github.com/yourusername/lyx_llm_assistant.git
   cd lyx_llm_assistant
   ```

2. Install the required dependencies:
   ```powershell
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project directory with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

4. Configure LyX to use the assistant:
   - Open LyX
   - Go to Tools > Preferences > Paths
   - Set the "LyX server pipe" to: `C:\Users\slons\AppData\Roaming\lyx\lyxpipe`
   - Click Apply
   - Close LyX completely
   - Restart LyX

## Verifying Installation

1. Run the test script to verify your LyX configuration:
   ```powershell
   python test_lyx_pipe.py
   ```

2. If the test fails, ensure:
   - LyX is running
   - Server pipe support is enabled
   - You have correct permissions for the AppData directory
   - The pipe path is set correctly in LyX preferences

## Usage

1. Start the LyX LLM Assistant:
   ```powershell
   python lyx_llm_assistant.py
   ```

2. Open LyX and start writing. The assistant will automatically provide suggestions based on your current context.

3. To stop the assistant, press Ctrl+C in the terminal.

## Configuration

You can customize the assistant's behavior by modifying the following environment variables in your `.env` file:

- `OPENAI_API_KEY`: Your OpenAI API key
- `LYXPIPE_PATH`: Custom path to LyX pipe (default: `C:\Users\slons\AppData\Roaming\lyx\lyxpipe`)

## Troubleshooting

1. If you get "Permission denied" errors:
   - Ensure you have write permissions to the AppData directory
   - Try running the terminal as administrator

2. If the pipes are not found:
   - Verify LyX is running
   - Check the pipe path in LyX preferences
   - Make sure you've restarted LyX after changing settings

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 