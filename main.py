
from flask import Flask, render_template, request
from init import create_app
app = create_app()
if __name__ == '__main__':
    app.run(debug=True)
    

#print(ocr_core('images/ocr_example_1.png'))




