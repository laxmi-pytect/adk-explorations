Cricket_agent
# call specific agent - adk run <agnet_name>
# run adk local server - adk run
# run adk as api server - adk run api_server -terminal (cloud run service), other agent can call the service
1. start the session- vscode window : curl -Method  POST http://127.0.0.1:8000/app
s/cricket_agent/users/test_user/sessions/test_session
other linus systems : curl -X  POST http://127.0.0.1:8000/app
s/cricket_agent/users/test_user/sessions/test_session
2. Send the post call: 
$jsonPayload = '{
    "app_name": "cricket_agent",
    "user_id": "test_user",
    "session_id": "test_session",
    "new_message": {
        "role": "user",
        "parts": [{"text": "Who won the last cricket world cup?"}]
    }
}'

Invoke-RestMethod -Uri "http://127.0.0.1:8000/run_sse" `
  -Method Post `
  -Headers @{"Content-Type"="application/json"} `
  -Body $jsonPayload

  
