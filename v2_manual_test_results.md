# Example Flow 2
Bob wants to view his tasks by order of due date to see which ones he should work on first. He calls POST user/login and enters his username and password. After getting an "OK" response, he calls GET /sort and sorts by due_date in descending order. This returns a list of tasks in the selected sorting order. He sees a task marked as "in progress" due today with task_id 28 and finishes working on it. He then calls PATCH /crud/update/28 and sets the status to "complete" and recieves an "OK" response, letting him know it succesfully updated.

# Testing results
## 1. Login:
curl -X 'POST' \
  'http://task-manager-api-vitd.onrender.com/user/login' \
  -H 'accept: application/json' \
  -H 'access_token: taskman' \
  -H 'Content-Type: application/json' \
  -d '{
  "user_name": "Bob",
  "password": "mypass"
}'
## 2. Response:
    "OK"
## 3. Sorting:
curl -X 'GET' \
  'http://127.0.0.1:3000/sort/sort?sort_col=due_date&sort_order=desc' \
  -H 'accept: application/json' \
  -H 'access_token: taskman'
## 4. Response:
{
  "results": [
    {
      "task_id": 29,
      "name": "Code Review",
      "description": "Review a pull request",
      "priority": null,
      "status": "complete",
      "start_date": "2024-03-12T00:29:23.435000+00:00",
      "due_date": "2024-03-12T00:29:23.435000+00:00",
      "end_date": null
    },
    {
      "task_id": 28,
      "name": "Documentation",
      "description": "Update docs with new feature",
      "priority": null,
      "status": "in progress",
      "start_date": "2024-02-12T00:29:23.435000+00:00",
      "due_date": "2024-09-12T00:29:23.435000+00:00",
      "end_date": null
    },
    {
      "task_id": 27,
      "name": "Flow Chart",
      "description": "Add necessary additions discussed in meeting",
      "priority": null,
      "status": "not started",
      "start_date": "2024-05-12T00:29:23.435000+00:00",
      "due_date": "2024-10-12T00:29:23.435000+00:00",
      "end_date": null
    }
  ]
}
## 5. Update Status:
curl -X 'POST' \
  'http://task-manager-api-vitd.onrender.com/crud/update/28' \
  -H 'accept: application/json' \
  -H 'access_token: taskman' \
  -H 'Content-Type: application/json' \
  -d '{
  "status": "complete"
}'
## 6. Response:
"OK"

# Example Flow 3
Robert owns a computer repair shop and uses the task manager to categorize repairs by their tags. He has tags for "laptop" or "desktop", the operating system "windows", "mac", or "linux", as well as the type of repair "display", "battery", "malware", among others. He receives an order from a customer with a Windows laptop that won't turn on and he creates a task for it using POST /crud/create which returns an ID of 341. After determining the issue is with the battery, he adds a tag to the task using POST tags/341/add with the request { "tags": ["battery"] }. Before making an order for a new battery, he views all tasks with the tag "battery" using GET sort/tags with the request { "tags": ["battery"] }.

# Testing results
## 1. Login:
curl -X 'POST' \
  'http://task-manager-api-vitd.onrender.com/user/login' \
  -H 'accept: application/json' \
  -H 'access_token: taskman' \
  -H 'Content-Type: application/json' \
  -d '{
  "user_name": "Robert",
  "password": "mypass"
}'
## 2. Response:
    "OK"
## 3. Create:

## 4. Response:
## 5. Add tag:
## 6. Response:
## 7. Sorting:
## 8. Response:
