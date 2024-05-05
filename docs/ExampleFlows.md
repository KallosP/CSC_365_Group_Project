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

## 3. Store Owner Categorizing Tasks
Robert owns a computer repair shop and uses the task manager to categorize repairs by their tags. He has tags for "laptop" or "desktop", the operating system "windows", "mac", or "linux", as well as the type of repair "display", "battery", "malware", among others. He recieves an order from a customer with a Windows laptop that won't turn on and he creates a task for it using POST /crud/create which returns an ID of 341. After determining the issue is with the battery, he adds a tag to the task using POST tags/341/add with the request { "tags": ["battery"] }. Before making an order for a new battery, he views all tasks with the tag "battery" using GET sort/tags with the request { "tags": ["battery"] }. 
