import threading

from flask import Flask, jsonify

app = Flask(__name__)


def is_prime(n: int) -> bool:
    """CPU-bound check for primality in O(√n) time."""
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    i = 3
    while i * i <= n:
        if n % i == 0:
            return False
        i += 2
    return True


@app.route("/prime/<int:n>")
def prime_check(n):
    """View that performs a CPU-bound prime check."""
    result = is_prime(n)
    return jsonify(number=n, is_prime=result)

@app.route("/prime_thread/<int:n>")
def prime_thread_check(n):
    """View that performs a CPU-bound prime check in a separate thread."""
    result = [None]  # Use a list to store the result from the thread

    def calculate_prime():
        result[0] = is_prime(n)

    # Create and start the thread
    t = threading.Thread(target=calculate_prime)
    t.start()
    t.join()  # Wait for the thread to complete

    return jsonify(number=n, is_prime=result[0])


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
