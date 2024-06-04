# Performance Writeup
## Fake Data Modeling
Python file used to construct million rows: https://github.com/KallosP/Task-Manager-API/blob/peter/populate_tasks.py

Final rows of data for each table:
- `users`: 10,000 rows
- `tasks`: 195,313 rows
- `tags`: 682,716 rows
- `subtasks`: 683,281 rows
- Total: 1,571,310 rows

We believe this distribution makes sense for how our service would scale due to how task managers are normally used. More specifically, 10,000 users creating 195,313 tasks means that every user has around 20 tasks. 682,716 tags equates to around 3-4 tags per task. Our `subtasks` table is slightly different from a traditional subtask in that it splits a single task into several subtasks so they can be completed over the course of a few days. This is based on the amount of free time the user provides, specifying how long they can spend working on tasks in a single day. So, having 683,281 subtask rows reflects the average user's task having to take more than one day to complete. We believe these to be sensible ratios for regular users of our API.

## Performance results of hitting endpoints
In ms:
- `/user/create`:	0.01087212563
- `/user/get_user_id`:	0.006993055344
- `/summary/`:	0.04179143906
- `/task/create`:	0.01151108742
- `/task/read`:	0.006985425949
- `/task/update`:	0.008670330048
- `/task/delete`:	0.2015559673
- `/sort/`:	0.03358507156
- `/sort/tags`:	0.08682632446
- `/tags/add`:	0.07355380058
- `/tags/get`:	0.03960323334
- `/tags/remove`:	0.07008337975
- `/analytics`:	0.1734366417
- `/scheduler/suggest`:	0.1547465324
- `/scheduler/set_free_time`:	0.01400971413

Three slowest endpoints:
1. `/task/delete`
2. `/analytics`
3. `/scheduler/suggest`

## Performance tuning
1. `/task/delete`:
...
2. `/analytics`
...
3. `/scheduler/suggest`:
### Result from `explain`
- `Delete on subtasks  (cost=0.00..17759.60 rows=0 width=0)`: This result means the startup cost for the query was 0, but the total cost (17759.60) seems to be a bit large/the cause of the longer runtime. Adding an index to the user_id column in `subtasks` would most likely increase the speed of the query, since, the reason for the long runtime is due to the volume of records in the table.
- Command for adding index: `create index idx_subtasks_user_id on public.subtasks (user_id);`
- Result of `explain` after adding index was `Delete on subtasks  (cost=0.42..9.63 rows=0 width=0)`: This performance improvement was expected, the cost was drastically reduced from 17759.60 to just 9.63, increasing the peformance by around 90%.
