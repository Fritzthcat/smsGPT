from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import os
import openai

app = Flask(__name__)

openai.api_key = os.environ.get("OPENAI_API_KEY")

@app.route("/sms", methods=['POST'])
def chatgpt():
    # Get incoming message
    inb_msg = request.form['Body'].lower()
    print(inb_msg)

    try:
        # Generate response using OpenAI API
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=inb_msg,
            max_tokens=3000,
            temperature=0.7
        )

        # Send response message using Twilio API
        resp = MessagingResponse()
        resp.message(response["choices"][0]["text"])
        print(response["choices"][0]["text"])
        return str(resp)

    except Exception as e:
        # Handle API errors
        print("Error:", e)
        resp = MessagingResponse()
        resp.message("Sorry, there was an error processing your request.")
        return str(resp)

if __name__ == "__main__":
    app.run(debug=True)