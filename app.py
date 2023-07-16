from flask import Flask, jsonify
import time

app = Flask(__name__)

# Token bucket parameters
capacity = 10  # Maximum number of tokens
tokens = capacity  # Current number of tokens
refill_rate = 0.1  # Tokens to be refilled per second
last_refill_time = time.time()  # Time of the last token refill

@app.route('/action', methods=['POST'])
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
        print("Action performed successfully")
        tokens -= 1
        return jsonify({'message': 'Action performed successfully'})
    else:
        # Return an error response if tokens are insufficient
        return jsonify({'message': 'Rate limit exceeded'}), 429

if __name__ == '__main__':
    app.run()
