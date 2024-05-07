# Example workflow
Alice is a new project manager for a retail website. Naturally, she wants to keep organized and decides she wants to start by creating three tasks. Initially she calls POST /user/create to create an account with the Task Manager API, setting her username to "Alice" and her password to "password123". After succesfully being stored in the system and receiving her unique ID (response from POST /user/create), she calls POST /crud/create and fills in the fields for her first task "Design and Prototype". After receiving an "OK" response, she successfully inserts her other tasks, "Documentation" and "Testing/Debugging", the same way.

# Testing results
<Repeated for each step of the workflow>
1. Account Creation:
curl -X 'POST' \
  'http://127.0.0.1:3000/user/create' \
  -H 'accept: application/json' \
  -H 'access_token: taskman' \
  -H 'Content-Type: application/json' \
  -d '{
  "user_name": "Alice",
  "password": "password123"
}'
2. Response:
{
  "user_id": 2
}
  
3. Task 1:
curl -X 'POST' \
  'http://127.0.0.1:3000/crud/create' \
  -H 'accept: application/json' \
  -H 'access_token: taskman' \
  -H 'Content-Type: application/json' \
  -d '{
  "user_id": 2,
  "name": "Design and Prototype",
  "description": "Begin designing and prototyping the product.",
  "priority": "high",
  "status": "not started",
  "start_date": "2024-05-07T04:47:02.715Z",
  "due_date": "2024-12-07T04:47:02.715Z",
  "end_date": "9999-12-31T23:59:59.999Z"
}'
4. Response:
 "OK"
  
5. Task 2:
curl -X 'POST' \
  'http://127.0.0.1:3000/crud/create' \
  -H 'accept: application/json' \
  -H 'access_token: taskman' \
  -H 'Content-Type: application/json' \
  -d '{
  "user_id": 2,
  "name": "Documentation",
  "description": "Begin documentation on representable parts of product.",
  "priority": "medium",
  "status": "not started",
  "start_date": "2024-05-07T04:47:02.715Z",
  "due_date": "2024-24-07T04:47:02.715Z",
  "end_date": "9999-12-31T23:59:59.999Z"
}'
4. Response:
 "OK"

6. Task 3:
curl -X 'POST' \
  'http://127.0.0.1:3000/crud/create' \
  -H 'accept: application/json' \
  -H 'access_token: taskman' \
  -H 'Content-Type: application/json' \
  -d '{
  "user_id": 2,
  "name": "Testing/Debugging",
  "description": "Start thoroughly testing current codebase and debugging existing issues.",
  "priority": "medium",
  "status": "not started",
  "start_date": "2024-05-07T04:47:02.715Z",
  "due_date": "2024-15-07T04:47:02.715Z",
  "end_date": "9999-12-31T23:59:59.999Z"
}'
8. Response:
  "OK"
