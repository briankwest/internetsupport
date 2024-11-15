# Plan for Internet Support AI Agent with SWAIG Functions

## Table of Contents

1. [Introduction](#introduction)
2. [Overview](#overview)
3. [Mock Data and Database Schema](#mock-data-and-database-schema)
   - [Customer Accounts](#customer-accounts)
   - [Support Tickets](#support-tickets)
4. [OpenAI Tool Spec for Support Functions](#openai-tool-spec-for-support-functions)
   - [Function: `verify_pin`](#function-verify_pin)
   - [Function: `get_account_info`](#function-get_account_info)
   - [Function: `check_line_status`](#function-check_line_status)
   - [Function: `open_ticket`](#function-open_ticket)
   - [Function: `check_ticket_status`](#function-check_ticket_status)
   - [Function: `close_ticket`](#function-close_ticket)
   - [Function: `transfer_to_agent`](#function-transfer_to_agent)
5. [SWAIG Function Schemas](#swaig-function-schemas)
6. [Example API Calls in SWAIG Format](#example-api-calls-in-swaig-format)
7. [Python Code for Internet Support AI Agent](#python-code-for-internet-support-ai-agent)
8. [System Prompt](#system-prompt)
9. [Full Draft Plan and Outline](#full-draft-plan-and-outline)

---

## 1. Introduction

This document outlines the design for an **Internet Support AI Agent** that serves as the front-line support for Cable, Fiber, and DSL services. The agent can verify customers, check account information, assess line status, manage trouble tickets, and transfer calls to a live human agent if needed.

---

## 2. Overview

- **Purpose**: Provide automated front-line support to customers for internet services.
- **Technologies Supported**: Cable, Fiber, DSL.
- **Integration**:
  - Uses SWAIG to define API endpoints for each support function.
  - All functions use mock data for demonstration purposes.
- **Functionality**:
  - **Customer Verification**: Verify customer identity using phone number and support PIN.
  - **Account Information**: Retrieve and display customer account details.
  - **Line Status Check**: Assess the status of the customer's internet line.
  - **Trouble Ticket Management**: Open, check, and close support tickets.
  - **Transfer to Human Agent**: Transfer the call to a live agent when necessary.
- **Implementation**:
  - Flask application using SWAIG for API integration.
  - Mock data stored in Python dictionaries or an in-memory database.

---

## 3. Mock Data and Database Schema

### Customer Accounts

**Schema**:

- **phone_number** (String, Primary Key)
- **support_pin** (String)
- **name** (String)
- **service_type** (String): "Cable", "Fiber", or "DSL"
- **account_status** (String): "Active", "Inactive"
- **line_status** (String): "Online", "Offline", "Intermittent"

**Sample Data**:

```python
customers = {
    "5551234": {
        "support_pin": "1234",
        "name": "John Doe",
        "service_type": "Fiber",
        "account_status": "Active",
        "line_status": "Online"
    },
    "5555678": {
        "support_pin": "5678",
        "name": "Jane Smith",
        "service_type": "DSL",
        "account_status": "Active",
        "line_status": "Offline"
    },
    "5559012": {
        "support_pin": "9012",
        "name": "Bob Johnson",
        "service_type": "Cable",
        "account_status": "Inactive",
        "line_status": "Offline"
    }
}
```

### Support Tickets

**Schema**:

- **ticket_id** (Integer, Primary Key)
- **phone_number** (String, Foreign Key to Customer Accounts)
- **issue_description** (String)
- **status** (String): "Open", "In Progress", "Closed"

**Sample Data**:

```python
tickets = [
    {
        "ticket_id": 1,
        "phone_number": "5555678",
        "issue_description": "Internet connectivity issues.",
        "status": "Open"
    },
    {
        "ticket_id": 2,
        "phone_number": "5551234",
        "issue_description": "Slow internet speed.",
        "status": "Closed"
    }
]
```

---

## 4. OpenAI Tool Spec for Support Functions

### Function: `verify_pin`

- **Description**: Verifies the customer's support PIN using their phone number.
- **Parameters**:

  ```json
  {
    "type": "object",
    "properties": {
      "phone_number": {
        "type": "string",
        "description": "Customer's phone number."
      },
      "support_pin": {
        "type": "string",
        "description": "Customer's support PIN."
      }
    },
    "required": ["phone_number", "support_pin"]
  }
  ```

### Function: `get_account_info`

- **Description**: Retrieves account information for a verified customer.
- **Parameters**:

  ```json
  {
    "type": "object",
    "properties": {
      "phone_number": {
        "type": "string",
        "description": "Customer's phone number."
      }
    },
    "required": ["phone_number"]
  }
  ```

### Function: `check_line_status`

- **Description**: Checks the line status for a verified customer's service.
- **Parameters**:

  ```json
  {
    "type": "object",
    "properties": {
      "phone_number": {
        "type": "string",
        "description": "Customer's phone number."
      }
    },
    "required": ["phone_number"]
  }
  ```

### Function: `open_ticket`

- **Description**: Opens a new support ticket for a customer.
- **Parameters**:

  ```json
  {
    "type": "object",
    "properties": {
      "phone_number": {
        "type": "string",
        "description": "Customer's phone number."
      },
      "issue_description": {
        "type": "string",
        "description": "Description of the issue."
      }
    },
    "required": ["phone_number", "issue_description"]
  }
  ```

### Function: `check_ticket_status`

- **Description**: Checks the status of an existing support ticket.
- **Parameters**:

  ```json
  {
    "type": "object",
    "properties": {
      "ticket_id": {
        "type": "integer",
        "description": "Support ticket ID."
      }
    },
    "required": ["ticket_id"]
  }
  ```

### Function: `close_ticket`

- **Description**: Closes an existing support ticket.
- **Parameters**:

  ```json
  {
    "type": "object",
    "properties": {
      "ticket_id": {
        "type": "integer",
        "description": "Support ticket ID."
      }
    },
    "required": ["ticket_id"]
  }
  ```

### Function: `transfer_to_agent`

- **Description**: Initiates a transfer to a live human agent.
- **Parameters**:

  ```json
  {
    "type": "object",
    "properties": {
      "phone_number": {
        "type": "string",
        "description": "Customer's phone number."
      }
    },
    "required": ["phone_number"]
  }
  ```

---

## 5. SWAIG Function Schemas

For each function, we define the SWAIG schema as follows.

### Function: `verify_pin`

```json
{
  "function": "verify_pin",
  "description": "Verifies the customer's support PIN.",
  "parameters": {
    "type": "object",
    "properties": {
      "phone_number": {
        "type": "string",
        "description": "Customer's phone number."
      },
      "support_pin": {
        "type": "string",
        "description": "Customer's support PIN."
      }
    },
    "required": ["phone_number", "support_pin"]
  }
}
```

### Function: `get_account_info`

```json
{
  "function": "get_account_info",
  "description": "Retrieves account information for the customer.",
  "parameters": {
    "type": "object",
    "properties": {
      "phone_number": {
        "type": "string",
        "description": "Customer's phone number."
      }
    },
    "required": ["phone_number"]
  }
}
```

*(Repeat similar schemas for the other functions.)*

---

## 6. Example API Calls in SWAIG Format

### Example for `verify_pin`

```json
{
  "ai_session_id": "example-session-id",
  "app_name": "internet_support_agent",
  "argument": {
    "parsed": [
      {
        "phone_number": "555-1234",
        "support_pin": "1234"
      }
    ],
    "raw": "{\"phone_number\":\"555-1234\",\"support_pin\":\"1234\"}",
    "substituted": ""
  },
  "parameters": {
    "type": "object",
    "properties": {
      "phone_number": {
        "type": "string",
        "description": "Customer's phone number."
      },
      "support_pin": {
        "type": "string",
        "description": "Customer's support PIN."
      }
    },
    "required": ["phone_number", "support_pin"]
  },
  "function": "verify_pin",
  "description": "Verifies the customer's support PIN.",
  "content_type": "text/swaig",
  "meta_data_token": "example-meta-data-token"
}
```

*(Similar examples can be provided for other functions.)*

---

## 7. Python Code for Internet Support AI Agent

Below is the Python code implementing the Internet Support AI Agent using Flask and SWAIG.

```python
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
    "5551234": {
        "support_pin": "1234",
        "name": "John Doe",
        "service_type": "Fiber",
        "account_status": "Active",
        "line_status": "Online"
    },
    "5555678": {
        "support_pin": "5678",
        "name": "Jane Smith",
        "service_type": "DSL",
        "account_status": "Active",
        "line_status": "Offline"
    },
    "5559012": {
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
        "phone_number": "5555678",
        "issue_description": "Internet connectivity issues.",
        "status": "Open"
    },
    {
        "ticket_id": 2,
        "phone_number": "5551234",
        "issue_description": "Slow internet speed.",
        "status": "Closed"
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
    phone_number=SWAIGArgument("string", "Customer's 7 digit phone number.", required=True),
    support_pin=SWAIGArgument("string", "Customer's support PIN.", required=True))
def verify_pin(phone_number, support_pin, meta_data_token=None, meta_data=None):
    if meta_data is None:
        meta_data = {}
    
    if verify_customer(phone_number, support_pin):
        meta_data = {'verified': True, 'phone_number': phone_number}
        return "Verification successful.", meta_data
    else:
        return "Verification failed. Please check your phone number and support PIN.", {}

# SWAIG endpoint to get account info
@swaig.endpoint("Get account information",
    phone_number=SWAIGArgument("string", "Customer's 7 digit phone number.", required=True))
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
    phone_number=SWAIGArgument("string", "Customer's 7 digit phone number.", required=True))
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
    phone_number=SWAIGArgument("string", "Customer's 7 digit phone number.", required=True),
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
        status = f"Ticket #{ticket_id} is currently {ticket['status']}."
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
        return f"Ticket #{ticket_id} has been closed."
    else:
        return f"Ticket #{ticket_id} not found.", {}

# SWAIG endpoint to transfer to a live agent
@swaig.endpoint("Transfer to human agent",
    phone_number=SWAIGArgument("string", "Customer's 7 digit phone number.", required=True))
def transfer_to_agent(phone_number, meta_data_token=None, meta_data=None):
    return "Transferring you to a live agent. Please wait.", {}

# Run the Flask application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.getenv('PORT', 5000), debug=os.getenv('DEBUG'))
```

**Notes**:

- **Authentication**:
  - Before accessing most functions, the customer must be verified using `verify_pin`.
  - The `meta_data` parameter is used to store verification status across functions.
- **Mock Data**:
  - Data is stored in dictionaries for simplicity.
  - In a production environment, this would be replaced with a database.
- **Error Handling**:
  - Functions check if the customer is verified.
  - Appropriate messages are returned if the customer is not found or verification fails.
- **Security Considerations**:
  - Since this is mock data for demonstration, security measures are minimal.
  - In a real-world application, ensure proper security practices are implemented.

---

## 8. System Prompt

```
You are an AI assistant providing front-line support for internet services, including Cable, Fiber, and DSL. Your role is to assist customers with issues related to their internet service. You can verify customer identity, check account information, assess line status, perform troubleshooting steps, manage support tickets, and transfer customers to a live human agent when necessary.

**Your Capabilities**:

- **Customer Verification**:
  - Verify customers using their phone number and support PIN before providing assistance.
  - **Phone Number Formatting**: Ensure that phone numbers are formatted into E.164 format before calling any functions. If a customer provides a 10-digit US phone number, translate it into E.164 format by adding the '+1' country code prefix.
- **Account Information**: Provide details about the customer's account, including service type and account status.
- **Line Status Check**: Check and inform customers about the status of their internet line.
- **Troubleshooting**: Perform basic troubleshooting steps to resolve common internet issues before opening a support ticket or transferring the call.
- **Support Ticket Management**:
  - **Open Ticket**: Create a new support ticket for the customer's issue if troubleshooting does not resolve it.
  - **Check Ticket Status**: Provide updates on existing support tickets.
  - **Close Ticket**: Close resolved support tickets upon the customer's request.
- **Transfer to Human Agent**: Transfer the customer to a live agent if you are unable to resolve their issue after troubleshooting.

**Interaction Guidelines**:

- **Verification**:
  - Always verify the customer's identity using their phone number and support PIN before providing account-specific information.
  - **Phone Number Handling**: If the customer provides a 10-digit US phone number, format it into E.164 by adding '+1' before proceeding with verification.
- **Troubleshooting Before Escalation**: Attempt to resolve the customer's issue through basic troubleshooting steps before opening a support ticket or transferring them to a live agent.
- **Empathy**: Show understanding and empathy towards the customer's situation.
- **Clarity**: Provide clear and concise information.
- **Professionalism**: Maintain a professional and helpful tone.
- **Limitations**: If you cannot resolve the issue after troubleshooting, offer to transfer the customer to a live human agent.

**Example Workflow**:

1. **Greeting**: Start by greeting the customer and asking for their phone number and support PIN for verification.
2. **Verification**:
   - Use the provided information to verify the customer's identity.
   - **Phone Number Formatting**: Ensure the phone number is in E.164 format before verification.
   - If verification fails, politely inform the customer and ask them to re-enter their details.
3. **Assistance**: Once verified, ask the customer how you can assist them today.
4. **Issue Resolution**:
   - **Troubleshooting**: If the customer reports an issue, perform appropriate troubleshooting steps.
   - **Line Status Check**: Check and inform the customer about the status of their internet line if necessary.
   - **Support Ticket**: If the issue persists after troubleshooting, open a support ticket.
5. **Closure**: After resolving the issue, summarize the actions taken and ask if there's anything else you can help with.
6. **Transfer**: If unable to resolve the issue after troubleshooting, inform the customer and offer to transfer them to a live agent.

**Remember**:

- Use the customer's name when addressing them after verification.
- Keep the conversation focused on resolving the customer's issue efficiently.
- Be patient and provide step-by-step guidance during troubleshooting.
```

---

## 9. Full Draft Plan and Outline

The goal is to create an **Internet Support AI Agent** that serves as front-line support for Cable, Fiber, and DSL services. The agent will interact with customers to resolve issues using various functions implemented through SWAIG.

**Key Components**:

1. **Mock Data Setup**:
   - Define schemas and sample data for customer accounts and support tickets.
   - Use Python dictionaries for simplicity.

2. **API Integration**:
   - Implement functions for customer verification, account info retrieval, line status check, ticket management, and transfer to a human agent.
   - Use SWAIG to define API endpoints for each function.

3. **Function Definitions**:
   - Each function has a clear description, parameters, and expected behavior.
   - Parameters are defined according to the OpenAI Tool Spec.

4. **SWAIG Implementation**:
   - Use SWAIG to create API endpoints that the AI agent can interact with.
   - Implement authentication using basic HTTP authentication.

5. **AI Agent Behavior**:
   - Craft a system prompt that guides the AI assistant's interactions.
   - Include guidelines for verification, assistance, and transfer to human agents.

6. **Session Management**:
   - Use the `meta_data` parameter to maintain session state, such as verification status.

7. **Error Handling**:
   - Implement error messages for failed verification, missing accounts, or invalid ticket IDs.
   - Ensure the assistant provides helpful feedback to the customer.

8. **Security Considerations**:
   - For demonstration purposes, security is minimal.
   - In a real-world application, implement proper security measures.

9. **Testing**:
   - Test each function to ensure it behaves as expected with the mock data.

10. **Deployment Considerations**:
    - Set up environment variables for sensitive information like authentication credentials.
    - Configure logging and debug settings appropriately.

**Implementation Steps**:

- **Step 1**: Set up the Flask application and SWAIG instance.
- **Step 2**: Define the mock data for customers and support tickets.
- **Step 3**: Implement the `verify_pin` function to verify customer identity.
- **Step 4**: Implement other support functions (`get_account_info`, `check_line_status`, etc.).
- **Step 5**: Use the `meta_data` parameter to maintain session state across functions.
- **Step 6**: Write the system prompt to guide the AI assistant's behavior.
- **Step 7**: Test the application thoroughly with various scenarios.
- **Step 8**: Document the API and functions according to the OpenAI Tool Spec.

---

**Final Notes**:

- This plan provides a comprehensive approach to building an AI agent for internet support.
- The use of mock data and SWAIG functions allows for easy testing and demonstration.
- Remember to consider security, scalability, and user experience when moving towards a production environment.
- Feel free to modify and expand upon this plan to suit any additional requirements.
