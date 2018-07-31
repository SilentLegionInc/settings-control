from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

numbers = []


@app.route('/', methods=['GET'])
def main():
    return render_template('index.html', numbers=numbers)


@app.route('/add_number', methods=['POST'])
def add_number():
    numbers.append(1)
    return redirect(url_for('main'))


if __name__ == '__main__':
    app.run()
