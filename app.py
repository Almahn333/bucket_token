from flask import Flask, jsonify
from flask_cors import CORS
import time
import logging

CORS(app)

app = Flask(__name__)

# Set up logging
logging.basicConfig(filename='rate_limit.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# Token bucket parameters
capacity = 10  # Maximum number of tokens
tokens = capacity  # Current number of tokens
refill_rate = 1  # Tokens to be refilled per second
last_refill_time = time.time()  # Time of the last token refill

@app.route('/api/action', methods=['POST'])
def perform_action():
    global tokens, last_refill_time

    # Calculate the time elapsed since the last refill
    current_time = time.time()
    time_elapsed = current_time - last_refill_time

    # Refill the tokens based on the time elapsed
    tokens += time_elapsed * refill_rate

    # Ensure tokens don't exceed the capacity
    tokens = min(tokens, capacity)

    # Update the last refill time
    last_refill_time = current_time

    # Check if there are enough tokens to perform the action
    if tokens >= 1:
        # Perform the rate-limited action here
        # For example, you can increment a counter or print a message
        logging.info('Action performed successfully')
        tokens -= 1
        return jsonify({'message': 'Action performed successfully', 'remaining_time': 0})
    else:
        # Calculate the remaining time until tokens recover
        remaining_time = (1 - tokens) / refill_rate

        # Return an error response with the remaining time
        logging.info('Rate limit exceeded')
        return jsonify({'message': 'Rate limit exceeded', 'Please wait for ': remaining_time}), 429

@app.route('/api/rate_limit_events', methods=['GET'])
def get_rate_limit_events():
    with open('rate_limit.log', 'r') as file:
        events = file.readlines()
        return jsonify({'events': events})

if __name__ == '__main__':
    app.run()
