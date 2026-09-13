# app.py
import random
import socket
from flask import Flask

app = Flask(__name__)

# A simple list of compleely neutral jokes.

JOKES = [
    "What has an eye, but cannot see? A needle.",
    "What kind of tree fits in your hand? A palm tree.",
    "What gets wet while drying? A towel.",
    "What can't a bicycl stand on its own? Because it is two-tired.",
    "What has a head and a tail, but no body? A coin.",
    "What has hands, but cannot clap? A clock.",
    "What has a neck, but no head? A bottle.",
    "What has a thumb and four fingers, but is not alive? A glove.",
    ]

@app.route("/")
def tell_a_joke():
    joke = random.choice(JOKES)
    hostname = socket.gethostname()
    # Add a V3 marker to the output!
    return f"{joke}\n[V3] (Served by : {hostname}\n)"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)

