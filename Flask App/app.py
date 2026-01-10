from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def home():
    name = request.args.get("name")

    if name:
        upper_name = name.upper()
        return f"HELLO, {upper_name}!"
    else:
        return "Please add ?name=yourname in the URL"

if __name__ == "__main__":
    app.run(debug=False)
