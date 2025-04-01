from pydantic_ai import Agent

system_prompt = """
You are a helpful assistant that can answer questions and help with tasks.
"""

agent = Agent(
    'google-gla:gemini-1.5-flash',
    system_prompt=system_prompt,
)

def process_message(message: str) -> str:
    """
    Process a message and return the agent's response.
    This function can be used by both CLI and web interface.
    """
    try:
        result = agent.run_sync(message)
        return result.data
    except Exception as e:
        return f"Error during processing: {e}"

def start_cli_conversation():
    print("-" * 20)
    print("🤖 Chatbot\n")
    print(f"System Prompt: {system_prompt}")
    print("-" * 20)

    while True:
        user_input = input("You: ")
        if user_input.lower() in ['quit', 'exit', 'bye']:
            print("Goodbye!")
            break

        response = process_message(user_input)
        print(f"🤖 Assistant: {response}")

# start_cli_conversation()