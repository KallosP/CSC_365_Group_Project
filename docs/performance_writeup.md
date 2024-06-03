# Performance Writeup
## Fake Data Modeling
Python file used to construct million rows: https://github.com/KallosP/Task-Manager-API/blob/peter/populate_tasks.py

Final rows of data for each table:
- users: 10,000 rows
- tasks: 195,313 rows
- tags: 682,716 rows
- subtasks: 683,281 rows
- Total: 1,571,310 rows

We believe this distribution makes sense for how our service would scale due to how task managers are normally used. More specifically, 10,000 users creating 195,313 tasks means that every user has around 20 tasks. 682,716 tags equates to around 3-4 tags per task. Our subtasks table is slightly different from a traditional subtask in that it splits a single task into several subtasks so they can be completed over the course of a few days. This is based on the amount of free time the user provides, specifying how long they can spend working on tasks in a single day. So, having 683,281 subtask rows reflects the average user's task having to take more than one day to complete. We believe these to be sensible ratios for regular users of our API.

## Performance results of hitting endpoints

## Performance tuning
