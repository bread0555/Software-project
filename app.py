from flask import Flask, render_template, request
from p2p import CodeBlock

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    i_p = ""
    o_p = ""
    if request.method == "POST":
        i_p = request.form.get("i_p")
        if not i_p:
            return render_template("index.html")
        else:
            c = CodeBlock(i_p.splitlines("\n"))
            c.analyse()
            o_p = "\n".join(c.o_p)
    return render_template("index.html", i_p=i_p, o_p=o_p)

# maybe add a page that describes how to use the app, including specifications of the pseudocode requirements

if __name__ == "__main__":
    app.run(debug=True)