from flask import render_template

def navigation():
    return render_template(
        "navigation.html",
    )
