from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
import os

app = Flask(__name__)
CORS(app)

@app.route('/send-email', methods=['POST'])
def send_email():
    data = request.get_json()

    name = data['name']
    email = data['email']
    message = data['message']

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()

        sender_email = os.environ.get('SENDER_EMAIL')
        sender_password = os.environ.get('SENDER_PASSWORD')
        server.login(sender_email, sender_password)

        subject = f'New Message from {name}'
        body = f'Name: {name}\nEmail: {email}\nMessage: {message}'
        message = f'Subject: {subject}\n\n{body}'

        receiver_email = os.environ.get('wheel.c.code@gmail.com')
        server.sendmail(sender_email, receiver_email, message)

        return jsonify({'success': True, 'message': 'Email sent successfully'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})
    finally:
        server.quit()

if __name__ == '__main__':
    app.run(debug=True)
