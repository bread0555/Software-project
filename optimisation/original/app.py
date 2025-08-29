from flask import Flask, render_template, request
from p2p import CodeBlock
import time

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    pseudocode_input = ""
    python_output = ""
    error_message = ""
    if request.method == "POST":
        pseudocode_input = request.form.get("pseudocode_input")
        if not pseudocode_input:
            return render_template("index.html")
        else:
            try:
                c = CodeBlock(pseudocode_input.splitlines("\n"))
                start_time = time.time()
                c.analyse()
                end_time = time.time()
                elapsed_time = end_time - start_time
                print(f"Analyse execution time: {elapsed_time:.6f} seconds")
                python_output = "\n".join(c.o_p)
            except Exception as e:
                error_message = str(e)
    return render_template("index.html", pseudocode_input=pseudocode_input, python_output=python_output, error_message=error_message)

@app.route("/rules")
def rules():
    return render_template("rules.html")

if __name__ == "__main__":
    app.run(debug=True)