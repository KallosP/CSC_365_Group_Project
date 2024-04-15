# User Stories
1. As an application debugger, I need an API that tracks my application's various tasks by date, so I know when certain tasks were executed before others.
2. As a game developer, I want to order my application's tasks by level of importance, so I can efficiently allocate my computer's resources and optimize performance.
3. As a developer, I want to categorize tasks based on tags, so I can filter them by their types.
4. As an embedded developer, I want to view CPU and memory usage, so I can decide which hardware to use and which tasks to run.
5. As a parallel programmer, I want to see which threads are running in each program, so I can optimize my code.
6. As someone with a slow computer, I want to see the state of programs, to know if a suspended program should be stopped.
7. As a project manager, I want to create tasks in the system, so that team members can view and complete them.
8. As a team member, I want to update the status of tasks, so that the project manager can track progress.
9. As a QA tester, I want to mark tasks as completed or needing rework, so that quality standards are maintained.
10. 
11. 
12. 

# Exceptions
## 1. Task Doesn't Exist
If the user attempts to access a task that doesn't exist, the API returns a "Task Not Found" error to the application and prompts the user to check the task ID or create a new task.
## 2. Task Duplication 
If the user's application tries to create a task that already exists, the API returns a "Task Already Exists" error and tells the user to instead create a new one.
## 3. Unauthorized Access
If an unauthorized user tries to create, modify, or delete a task, the API returns an "Unauthorized Access" error.
## 4. Default Values
When a user creates a task, task attributes that are not specified should be filled with sensible values for usage statistics, tags, and state.
## 5. Race Conditions
Task attributes that are modified frequently should return the most recent value within a reasonable time frame.
## 6. Invalid Data
If a user modifies an attribute, they must adhere to data type and formatting for that field. If they attempt to change an attribute to something invalid, the API will return a "Data Type" error.
## 7. Database Connection Failure
If the API fails to connect to the database, it should log the error and notify the system administrator while providing a friendly message to the user.
## 8. Task Creation Failure
If a task cannot be created due to a system error, the user should receive a notification to try again or contact support if the issue persists.
## 9. Task Update Failure
If updates to a task fail, users should be prompted to check their network connection or input values and try again.
## 10. 
## 11. 
## 12. 
