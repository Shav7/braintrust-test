import openai
import os
import time
import logging
import sys

# Load the API key from the environment variable
openai.api_key = os.environ.get("OPENAI_API_KEY")

if not openai.api_key:
    logging.error("The OPENAI_API_KEY environment variable is not set.")
    sys.exit(1)


# Set up logging to display debug information
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')

# Set the base URL to use the Braintrust AI Proxy
openai.api_base = "https://api.braintrust.dev/v1/proxy"

# Retrieve your API key from the environment variable
api_key = os.environ.get("OPENAI_API_KEY")

if not api_key:
    logging.error("The environment variable OPENAI_API_KEY is not set.")
    sys.exit("Please set your OPENAI_API_KEY environment variable and try again.")

openai.api_key = api_key

def main():
    try:
        # Allow the user to input the model name
        model_name = input("Enter the model name (e.g., 'gpt-3.5-turbo', 'gpt-4', 'claude-2', 'llama-2-13b-chat'): ").strip()
        if not model_name:
            logging.error("No model name entered.")
            sys.exit("Please enter a valid model name.")

        # Allow the user to input their question
        user_question = input("Enter your question for the AI model: ").strip()
        if not user_question:
            logging.error("No question entered.")
            sys.exit("Please enter a question to ask the AI model.")

        # Allow the user to input a seed value (optional)
        seed_input = input("Enter a seed value (optional, press Enter to skip): ").strip()
        seed = int(seed_input) if seed_input else None

        # Record the start time
        start_time = time.time()

        # Build the request parameters
        request_params = {
            "model": model_name,
            "messages": [{"role": "user", "content": user_question}],
        }

        # Include the seed if provided
        if seed is not None:
            request_params["seed"] = seed

        # Log the request parameters
        logging.debug(f"Request parameters: {request_params}")

        # Send the request to the AI model
        response = openai.ChatCompletion.create(**request_params)

        # Log the raw response
        logging.debug(f"Raw response: {response}")

        # Print the AI's response
        print("\nAI Response:")
        print(response.choices[0].message.content)

    except openai.error.OpenAIError as e:
        # Handle exceptions from the OpenAI API
        logging.error(f"An OpenAI API error occurred: {e}")
        sys.exit(f"OpenAI API error: {e}")

    except ValueError as e:
        # Handle value errors, such as invalid seed input
        logging.error(f"Value error: {e}")
        sys.exit(f"Value error: {e}")

    except Exception as e:
        # Handle any other exceptions
        logging.error(f"An unexpected error occurred: {e}")
        sys.exit(f"Unexpected error: {e}")

    finally:
        # Calculate and print the time taken
        elapsed_time = time.time() - start_time
        print(f"\nTook {elapsed_time:.6f}s")

if __name__ == "__main__":
    main()

