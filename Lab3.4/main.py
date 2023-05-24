from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        amount = float(request.form['amount'])
        rate = float(request.form['rate']) / 100
        time = int(float(request.form['time']))
    except ValueError:
        return 'Invalid input', 400

    if amount <= 0:
        return render_template('error.html', message='Amount must be greater than 0')
    if time <= 0:
        return render_template('error.html', message='Time must be greater than 0')

    monthly_rate = rate / 12

    # Вычисляем ежемесячный платеж
    try:
        monthly_payment = (amount * monthly_rate * (1 + monthly_rate) ** (time * 12)) / \
            ((1 + monthly_rate) ** (time * 12) - 1)
    except OverflowError:
        return render_template('error.html', message='Result too large to display')
    monthly_payment = round(monthly_payment, 2)

    # Вычисляем начисленные проценты
    total_paid = monthly_payment * time * 12
    total_interest = total_paid - amount
    total_interest = round(total_interest, 2)
    total_paid = round(total_paid, 2)

    if total_paid >= 1e50:
        return render_template('error.html', message='Result too large to display')

    return render_template('result.html', monthly_payment=monthly_payment,
                           total_interest=total_interest, total_paid=total_paid)

if __name__ == '__main__':
    app.run(debug=True)