# User Stories
1. As an application debugger, I need an API that I can use that tracks the various bugs I need to fix, so I can stay organized when debugging.
2. As a dog trainer, I want to store the jobs that were assigned to me, so I can remember what I need to get done.
3. As a developer, I want to categorize tasks based on tags, so I can filter them by their types.
4. As a project manager, I want to create a set of tasks with deadlines for employees, so they know when they should get their tasks done.
5. As a project evaluator, I want to see how long it took certain employees to complete their tasks, so I can gather efficiency data.
6. 
7. 
8. As a team member, I want to update the status of tasks, so that the project manager can track progress.
9. As a QA tester, I want to mark tasks as completed or needing rework, so that quality standards are maintained.
10. As a data analyst, I want to be able to see all task completion times, so I can use the data.
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
## 10. Task Deleting Failure
If a task cannot be deleted due to a system error, the user should recieve a notification to try again or contact support if the issue persists.
## 11. Invalid Transition
If the transition of the state of a task happens in an invalid order notify the user that it is an invalid transition.
## 12. Dependency Error
If there is an invalid dependency ie. a circular dependency notify the user and suggest a fix for the dependency issue.
