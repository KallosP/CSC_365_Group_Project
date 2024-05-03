# User Stories
1. As an application debugger, I need an API that I can use that tracks the various bugs I need to fix, so I can stay organized when debugging.
2. As a dog trainer, I want to store the jobs that were assigned to me, so I can remember what I need to get done.
3. As a developer, I want to categorize tasks based on tags, so I can filter them by their types.
4. As a project manager, I want to create a set of tasks with deadlines for employees, so they know when they should get their tasks done.
5. As a project evaluator, I want to see how long it took certain employees to complete their tasks, so I can gather efficiency data.
6. As a freelancer, I want to keep track of the time spent on each task, so I can bill my clients accurately.
7. As a product owner, I want to prioritize tasks based on their importance and urgency, so I can ensure that critical tasks are completed first.
8. As a team member, I want to update the status of tasks, so that the project manager can track progress.
9. As a QA tester, I want to mark tasks as completed or needing rework, so that quality standards are maintained.
10. As a data analyst, I want to be able to see all task completion times, so I can use the data.
11. As a remote worker, I want to add notes and comments to tasks, so I can share updates and clarifications with my team.
12. As a team lead, I want to assign tasks to my team members, so I can distribute the workload evenly.

# Exceptions
## 1. Task Doesn't Exist
If the user attempts to access a task that doesn't exist, the API returns a "Task Not Found" error to the user and prompts them to check if they entered an existing task.
## 2. Task Duplication 
If the user tries to create a task that already exists, the API returns a "Task Already Exists" error and tells the user to instead create a new one.
## 3. Unauthorized Access
If an unauthorized user tries to create, modify, or delete a task, the API returns an "Unauthorized Access" error.
## 4. Default Values
When a user creates a task, mandatory task attributes that are not specified are filled with default values and a prompt informs the user of this auto-fill.
## 5. Race Conditions
Task attributes that are modified frequently should return the most recent value within a reasonable time frame.
## 6. Invalid Data
If a user modifies an attribute, they must adhere to data type and formatting for that field. If they attempt to change an attribute to something invalid, the API will return a "Data Type" error.
## 7. Database Connection Failure
If the API fails to connect to the database, it should log the error and notify the user of an internal server error.
## 8. Task Creation Failure
If a task cannot be created due to a system error, the user should receive a notification to try again or contact support if the issue persists.
## 9. Task Update Failure
If updates to a task fail, users should be prompted to check their network connection or input values and try again.
## 10. Task Deleting Failure
If a task cannot be deleted due to a system error, the user should recieve a notification to try again or contact support if the issue persists.
## 11. Tag Duplicate Error
If a user attempts to add a tag to a task that already has that tag, the API returns a duplication error, notifying the user the tag is already applied on that task.
## 12. Task Insert Into Group Error
If a task cannot be inserted into a group, an error is returned notifying the user the exact reason why the task could not be added.
