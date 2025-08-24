from flask import Flask, render_template, request
from p2p import CodeBlock

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    pseudocode_input = ""
    python_output = ""
    if request.method == "POST":
        pseudocode_input = request.form.get("pseudocode_input")
        if not pseudocode_input:
            return render_template("index.html")
        else:
            c = CodeBlock(pseudocode_input.splitlines("\n"))
            c.analyse()
            python_output = "\n".join(c.o_p)
    return render_template("index.html", pseudocode_input=pseudocode_input, python_output=python_output)

@app.route("/rules")
def rules():
    return render_template("rules.html")

if __name__ == "__main__":
    app.run(debug=True)