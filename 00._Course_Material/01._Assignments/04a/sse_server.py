from flask import Flask, Response
import time

app = Flask(__name__)

def generate_messages():
    while True:
        time.sleep(1)
        yield f"data: The current time is {time.ctime()}\n\n"

@app.route('/stream')
def stream():
    return Response(generate_messages(), mimetype='text/event-stream')

@app.route('/')
def index():
    return """
    <!doctype html>
    <html lang="en">
      <head>
        <meta charset="utf-8">
        <title>SSE Example</title>
      </head>
      <body>
        <h1>Server-Sent Events (SSE) Example</h1>
        <div id="events"></div>
        <script>
          const eventSource = new EventSource('/stream');
          eventSource.onmessage = function(event) {
            const newElement = document.createElement("div");
            newElement.textContent = event.data;
            document.getElementById("events").appendChild(newElement);
          };
        </script>
      </body>
    </html>
    """

if __name__ == '__main__':
    app.run(debug=True, threaded=True)
