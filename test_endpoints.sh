#!/bin/bash

# Base URL for the SWAIG server
BASE_URL="http://sql:sql@${NGROK_URL}/swaig"

# Test Verify Customer PIN
echo "Testing Verify Customer PIN..."
swaig_cli --url $BASE_URL --function verify_pin --json '{"phone_number": "+19184249378", "support_pin": "1234"}' --meta-data '{"verified": true}'

# Test Get Account Information
echo "Testing Get Account Information..."
swaig_cli --url $BASE_URL --function get_account_info --json '{"phone_number": "+19184249378"}' --meta-data '{"verified": true}'

# Test Check Line Status
echo "Testing Check Line Status..."
swaig_cli --url $BASE_URL --function check_line_status --json '{"phone_number": "+19184249378"}' --meta-data '{"verified": true}'

# Test Open a Support Ticket
echo "Testing Open a Support Ticket..."
swaig_cli --url $BASE_URL --function open_ticket --json '{"phone_number": "+19184249378", "issue_description": "Test issue"}' --meta-data '{"verified": true}'

# Test Check Ticket Status
echo "Testing Check Ticket Status..."
swaig_cli --url $BASE_URL --function check_ticket_status --json '{"ticket_id": 1}' --meta-data '{}'

# Test Close a Support Ticket
echo "Testing Close a Support Ticket..."
swaig_cli --url $BASE_URL --function close_ticket --json '{"ticket_id": 1}' --meta-data '{}'

# Test Transfer to Human Agent
echo "Testing Transfer to Human Agent..."
swaig_cli --url $BASE_URL --function transfer_to_agent --json '{"phone_number": "+19184249378"}' --meta-data '{"verified": true}'

echo "All tests completed."