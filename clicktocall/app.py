from flask import Flask
from flask import jsonify
from flask import render_template
from flask import request
from flask import url_for

from twilio import twiml
from twilio.rest import TwilioRestClient

# Declare and configure application
app = Flask(__name__, static_url_path='/static')
app.config.from_pyfile('local_settings.py')


# Route for Click to Call demo page.
@app.route('/')
def index():
    return render_template('index.html',
                           configuration_error=None)


# Voice Request URL
@app.route('/call', methods=['POST'])
def call():
    # Get phone number we need to call
    phone_number = request.form.get('phoneNumber', None)

    try:
        twilio_client = TwilioRestClient(app.config['TWILIO_ACCOUNT_SID'],
                                         app.config['TWILIO_AUTH_TOKEN'])
    except Exception as e:
        msg = 'Missing configuration variable: {0}'.format(e)
        return jsonify({'error': msg})

    try:
        twilio_client.calls.create(from_=app.config['TWILIO_CALLER_ID'],
                                   to=phone_number,
                                   url=url_for('.outbound',
                                               _external=True))
    except Exception as e:
        app.logger.error(e)
        return jsonify({'error': str(e)})

    return jsonify({'message': 'Pick up your phone!'})


@app.route('/outbound', methods=['POST'])
def outbound():
    response = twiml.Response()

    response.say("Thank you for calling here for reentry baltimore's ringdown application."
                 " Please introduce yourself and remember that these volunteers are here to help."
                 "If you are sent to voice mail, record a message then press star or pound in order to continue looking for help."
                 " You will now be connected with a returning citizen voulenteer.",
                 voice='man')
    
    # Uncomment this code and replace the number with the number you want
    # your customers to call.
    with response.dial() as dial:
        dial.number("+14438191461")
    
    return str(response)


# Route for Landing Page after Heroku deploy.
@app.route('/landing.html')
def landing():
    return render_template('landing.html',
                           configuration_error=None)
