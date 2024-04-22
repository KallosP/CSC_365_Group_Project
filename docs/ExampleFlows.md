# Example Flows
## 1. Project Manager Creating a Task
Alice, the system administrator, is monitoring her system’s tasks. She notices a new task that needs to be added for a system update. The task is of high priority. She calls POST /create passing "System Update" as the name, a small description, and "high" as the priority. This new task now has an ID of 5001 and has been saved. 

Later, Alice wants to check the summary of all her tasks after adding "System Update" to ensure that the number of processes that should be running is normal. She calls GET /summary and can see there are:
- 312 total tasks
- 65 active tasks
- 242 disabled tasks
- 5 suspended tasks
  
## 2. Monitoring Hardware Utilization
Bobby is using the task manager to view resource usage while working on a large program. After executing his program by calling POST /create, he wants to see the computer's utilization due to both his program and the rest of the programs running on his computer. 

To do this, he uses his task's ID given in the response of /create to call /summary/{task_id} which tells him his task is using 10% of his CPU usage and 50% of his memory usage. He then compares this to the total usage by calling /utilization and sees his computer is using 23% of his CPU and 70% of his memory. He uses this information to fix a memory leak in his program.

## 3.
