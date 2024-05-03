# Example Flows
## 1. Project Manager Creating a Task
Alice is the project manager for a retail website. She wants to create a high priority task for advertising a new potion product. She calls POST /crud/create with "Adverstise Potion" as the name, fills out a short description, sets the priority to "high", and sets the status to "in progress". The task gets created and the ID is set to 5001.

Later, Alice wants to check the status of all tasks associated with the website. She calls GET /summary and can see there are:
- 312 total tasks
- 65 completed tasks
- 242 in progress tasks
- 5 not started tasks
  
## 2. Employee Sorting and Completing a Task
Bob, an employee of Alice, wants to view his tasks by order of due date to see which tasks he should work on first. He calls POST sort/due_date which returns a list of tasks ordered by the timestamp they are due. He sees a task due today with ID 5001 and finishes working on it. He then calls PATCH /crud/update/5001 and sets the status to "complete".

## 3. 
