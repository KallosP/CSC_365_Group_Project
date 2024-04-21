# Example Flows
## 1. Project Manager Creating a Task
Alice, the system administrator, is monitoring her system’s tasks. She notices a new task that needs to be added for a system update. The task is of high priority. She calls POST /create passing "System Update" as the name, a small description, and "high" as the priority. This new task now has an ID of 5001 and has been saved. 

Later, Alice wants to check the summary of all her tasks after adding "System Update" to ensure that the number of processes that should be running is normal. She calls GET /summary and can see there are:
- 312 total tasks
- 65 active tasks
- 242 disabled tasks
- 5 suspended tasks
  
## 2.
## 3.
