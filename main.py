
# import statements
from flask import Flask, render_template, request
from init import create_app

# create app
app = create_app()
if __name__ == '__main__':
    app.run(debug=True)




