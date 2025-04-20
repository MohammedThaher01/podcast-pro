import os
from pinecone import Pinecone, ServerlessSpec

# Create a Pinecone instance with your API key
pc = Pinecone(api_key="your_api_key")  # Replace with your actual API key

# Now interact with Pinecone
index = pc.Index("your_index_name")  # Replace with your actual index name

# Sample function to simulate input/output flow
def chat_with_model(user_input):
    # You can replace this with your model's logic
    # For example, query the Pinecone index or any AI model

    # Simulating query logic (replace with actual query)
    response = f"Model output for input '{user_input}'"
    
    return response

def main():
    print("Welcome to the terminal demo! Type 'exit' to quit.")
    
    while True:
        # Taking user input in the terminal
        user_input = input("You: ")

        if user_input.lower() == 'exit':
            print("Exiting demo. Goodbye!")
            break
        
        # Get model response
        model_output = chat_with_model(user_input)

        # Display the model's output in the terminal
        print(f"Model: {model_output}")

if __name__ == "__main__":
    main()
