#!/usr/bin/env python3
from agent import PodcastAssistant
# import readline  # For better input handling
from pyfiglet import figlet_format
from termcolor import colored
import time

def main():
    # Print fancy header
    print(colored(figlet_format("PodcastPro", font="slant"), "cyan"))
    print(colored("AI Assistant for Podcast Creators", "yellow"))
    print(colored("Type 'exit' to quit\n", "grey"))

    # Initialize assistant
    assistant = PodcastAssistant()
    print(colored("🟢 Assistant ready! How can I help with your podcast today?\n", "green"))

    while True:
        try:
            # Get user input with colored prompt
            user_input = input(colored("🎙 You: ", "blue"))
            
            if user_input.lower() in ["exit", "quit"]:
                print(colored("\n🎧 Goodbye! Happy podcasting!", "magenta"))
                break

            if not user_input.strip():
                print(colored("🔴 Please enter a valid message", "red"))
                continue

            # Get and display response
            start_time = time.time()
            response = assistant.chat(user_input)
            elapsed = time.time() - start_time

            print(colored(f"\n🤖 PodcastPro ({(elapsed):.2f}s):", "green"))
            print(response + "\n")

        except KeyboardInterrupt:
            print(colored("\n🎧 Session ended", "magenta"))
            break
        except Exception as e:
            print(colored(f"\n🔴 Error: {str(e)}", "red"))

if __name__ == "__main__":
    main()