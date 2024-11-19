from flask import Flask
from dotenv import load_dotenv
import os
import logging
from signalwire_swaig.core import SWAIG, SWAIGArgument

# Load environment variables from a .env file
load_dotenv()

# Set logging level for Flask's built-in server
logging.getLogger('werkzeug').setLevel(logging.WARNING)

# Enable debug mode if specified in environment variables
if os.environ.get('DEBUG', False):
    print("Debug mode is enabled")
    logging.getLogger('werkzeug').setLevel(logging.DEBUG)

# Initialize Flask and SWAIG
app = Flask(__name__)
swaig = SWAIG(
    app,
    auth=(os.getenv('HTTP_USERNAME'), os.getenv('HTTP_PASSWORD'))
)

# Mock data for customers and tickets
customers = {
    "+19184249378": {
        "support_pin": "1234",
        "name": "John Doe",
        "service_type": "Fiber",
        "account_status": "Active",
        "line_status": "Online"
    },
    "+13322819378": {
        "support_pin": "5678",
        "name": "Jane Smith",
        "service_type": "DSL",
        "account_status": "Active",
        "line_status": "Offline"
    },
    "+14087419378": {
        "support_pin": "9012",
        "name": "Bob Johnson",
        "service_type": "Cable",
        "account_status": "Inactive",
        "line_status": "Offline"
    }
}

tickets = [
    {
        "ticket_id": 1,
        "phone_number": "+19184249378",
        "issue_description": "Internet connectivity issues.",
        "status": "Open"
    },
    {
        "ticket_id": 2,
        "phone_number": "+14087419378",
        "issue_description": "Slow internet speed.",
        "status": "Closed"
    },
    {
        "ticket_id": 3,
        "phone_number": "+13322819378",
        "issue_description": "Account deactivation.",
        "status": "Open"
    }
]

# Function to verify customer PIN
def verify_customer(phone_number, support_pin):
    customer = customers.get(phone_number)
    if customer and customer['support_pin'] == support_pin:
        return True
    return False

# SWAIG endpoint to verify PIN
@swaig.endpoint("Verify customer PIN",
    phone_number=SWAIGArgument("string", "Customer's digit phone number in e.164 format.", required=True),
    support_pin=SWAIGArgument("string", "Customer's support PIN.", required=True))
def verify_pin(phone_number, support_pin, meta_data_token=None, meta_data=None):
    if meta_data is None:
        meta_data = {}
    
    if verify_customer(phone_number, support_pin):
        meta_data = {'verified': True, 'phone_number': phone_number}
        customer = customers.get(phone_number)
        if customer:
            customer_info = f"Name: {customer['name']}"
            return f"Verification successful. {customer_info}", [{"set_meta_data": meta_data}]
        return "Verification successful.", [{"set_meta_data": meta_data}]
    else:
        return "Verification failed. Please check your phone number and support PIN.", {}

# SWAIG endpoint to get account info
@swaig.endpoint("Get account information",
    phone_number=SWAIGArgument("string", "Customer's digit phone number in e.164 format.", required=True))
def get_account_info(phone_number, meta_data_token=None, meta_data=None):
    if meta_data is None or not meta_data.get('verified'):
        return "Please verify your account first using your phone number and support PIN.", {}
    customer = customers.get(phone_number)
    if customer:
        info = f"Name: {customer['name']}\nService Type: {customer['service_type']}\nAccount Status: {customer['account_status']}"
        return info
    else:
        return "Account not found.", {}

# SWAIG endpoint to check line status
@swaig.endpoint("Check line status",
    phone_number=SWAIGArgument("string", "Customer's digit phone number in e.164 format.", required=True))
def check_line_status(phone_number, meta_data_token=None, meta_data=None):
    if meta_data is None or not meta_data.get('verified'):
        return "Please verify your account first using your phone number and support PIN.", {}
    print(phone_number)
    customer = customers.get(phone_number)
    if customer:
        status = f"Your line status is: {customer['line_status']}."
        return status, {}
    else:
        return "Account not found.", {}

# SWAIG endpoint to open a support ticket
@swaig.endpoint("Open a support ticket",
    phone_number=SWAIGArgument("string", "Customer's digit phone number in e.164 format.", required=True),
    issue_description=SWAIGArgument("string", "Description of the issue.", required=True))
def open_ticket(phone_number, issue_description, meta_data_token=None, meta_data=None):
    if meta_data is None or not meta_data.get('verified'):
        return "Please verify your account first using your phone number and support PIN.", {}
    ticket_id = len(tickets) + 1
    new_ticket = {
        "ticket_id": ticket_id,
        "phone_number": phone_number,
        "issue_description": issue_description,
        "status": "Open"
    }
    tickets.append(new_ticket)
    return f"Ticket #{ticket_id} has been opened for your issue.", {}

# SWAIG endpoint to check ticket status
@swaig.endpoint("Check ticket status",
    ticket_id=SWAIGArgument("integer", "Support ticket ID.", required=True))
def check_ticket_status(ticket_id, meta_data_token=None, meta_data=None):
    ticket = next((t for t in tickets if t['ticket_id'] == ticket_id), None)
    if ticket:
        status = f"Ticket #{ticket_id} is currently {ticket['status']}.", {}
        return status
    else:
        return f"Ticket #{ticket_id} not found.", {}

# SWAIG endpoint to close a support ticket
@swaig.endpoint("Close a support ticket",
    ticket_id=SWAIGArgument("integer", "Support ticket ID.", required=True))
def close_ticket(ticket_id, meta_data_token=None, meta_data=None):
    ticket = next((t for t in tickets if t['ticket_id'] == ticket_id), None)
    if ticket:
        ticket['status'] = 'Closed'
        return f"Ticket #{ticket_id} has been closed.", {}
    else:
        return f"Ticket #{ticket_id} not found.", {}

# SWAIG endpoint to transfer to a live agent
@swaig.endpoint("Transfer to human agent",
    phone_number=SWAIGArgument("string", "Customer's digit phone number in e.164 format.", required=True))
def transfer_to_agent(phone_number, meta_data_token=None, meta_data=None):
    # TODO: Implement transfer to human agent, simple return of some swml
    return "Transferring you to a live agent. Please wait.", {}

@app.route('/swaig', methods=['GET'])
@app.route('/', methods=['GET'])
def dump():
    customer_data_html = "<h1>Customer Data</h1><ul>"
    for phone_number, customer in customers.items():
        customer_data_html += "<li>"
        customer_data_html += f"Phone Number: {phone_number}, "
        for key, value in customer.items():
            customer_data_html += f"{key}: {value}, "
        customer_data_html = customer_data_html.rstrip(", ")  # Remove trailing comma and space
        customer_data_html += "</li>"
    customer_data_html += "</ul>"

    tickets_html = "<h1>Tickets</h1><ul>"
    for ticket in tickets:
        tickets_html += f"<li>Ticket ID: {ticket['ticket_id']}, Phone: {ticket['phone_number']}, Issue: {ticket['issue_description']}, Status: {ticket['status']}</li>"
    tickets_html += "</ul>"

    return f"<html><body>{customer_data_html}{tickets_html}</body></html>"
# Run the Flask application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.getenv('PORT', 5000), debug=os.getenv('DEBUG', False))
