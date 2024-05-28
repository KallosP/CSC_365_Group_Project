# API Specification for Task Manager

## 1. Task CRUD

### 1.1. New Task - `/crud/create` (POST)

Create a new task.

**Request**:

```json
{
    "user_id": "int",
    "name": "string",
    "description": "string",   /* optional */
    "priority": "string",      /* optional, "high", "medium", or "low" */
    "status": "string",        /* optional, "complete", "not started", "in progress" */
    "start_date": "timestamp", /* optional, ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ) */
    "due_date": "timestamp",   /* optional, ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ) */
    "end_date": "timestamp",   /* optional, ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ) */
    "estimated_time": "number" /* optional, estimated time to complete task (in hours) */
}
```

**Response**:

```json
{
  "task_id": "int"
}
```

### 1.2. Read Task - `/crud/read` (GET)

Gets the informaiton associated with an existing task.

**Request**:

```
GET /tags/get?user_id=int&task_id=int
```

**Response**:

```json
{
  "name": "string",
  "description": "string",
  "priority": "string" /* "high", "medium", or "low" */,
  "status": "string" /* "complete", "not started", "in progress" */,
  "start_date": "timestamp" /* iso 8601 format (yyyy-mm-ddthh:mm:ssz) */,
  "due_date": "timestamp" /* iso 8601 format (yyyy-mm-ddthh:mm:ssz) */,
  "end_date": "timestamp" /* iso 8601 format (yyyy-mm-ddthh:mm:ssz) */
}
```

### 1.3. Update Task - `/crud/update/{task_id}` (PUT)

Update an existing task.

**Request**:

```json
{
  "user_id": "int",
  "task_id": "int",
  "name": "string" /* optional */,
  "description": "string" /* optional */,
  "priority": "string" /* optional, "high", "medium", or "low" */,
  "status": "string" /* optional, "complete", "not started", "in progress" */,
  "start_date": "timestamp" /* optional, ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ) */,
  "due_date": "timestamp" /* optional, ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ) */,
  "end_date": "timestamp" /* optional, ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ) */
}
```

**Response**:

```json
{
  "OK: Task successfully updated"
}
```

### 1.4. Delete Task - `/crud/delete/{task_id}` (DELETE)

Delete an existing task (and its tags.)

**Request**:

```json
{
  "user_id": "int",
  "task_id": "int"
}
```

**Response**:

```json
{
    "OK: Task and associated tags successfully deleted"
}
```

## 2. Task Summary

### 2.1. Get Tasks Summary - `/summary` (GET)

Return a summary of all tasks that have been created.

**Request**:

```
GET /summary/get?user_id=int
```

**Response**:

```json
{
  "number_of_tasks": "number",
  "tasks_completed": "number",
  "tasks_in_progress": "number",
  "tasks_not_started": "number"
}
```

## 3. Tag Modification

### 3.1 Get Tags - `/tags/get` (GET)

Return a list of all tags associated with the task.

**Request**:

```
GET /tags/get?user_id=int&task_id=int
```

**Response**:

```json
{
  "tags": ["string", "string", ...]
}
```

### 3.2 Adding Tags - `/tags/add` (POST)

Adds tags to a task.

**Request**:

```json
{
  "user_id": "int",
  "task_id": "int",
  "tags": ["string", "string", ...]
}
```

**Response**:

```json
{
  "OK: Tag added successfully"
}
```

### 3.3 Removing Tags - `/tags/remove` (DELETE)

Removes tags from a task

**Request**:

```json
{
  "user_id": "int",
  "task_id": "int",
  "tags": ["string", "string", ...]
}
```

**Response**:

```json
{
  "OK: Tag successfully removed"
}
```

## 4. Sort Tasks

### 4.1 Sort Tasks by Field - `/sort` (GET)

Sort tasks by provided field (excluding description)

**Request**:

```
GET /sort?user_id=int&sort_col=string&sort_order=string
```

**Response**:

```json
[

    {
    "task_id": "int",
    "name": "string",
    "description": "string",
    "priority": "string",      /* "high", "medium", or "low" */
    "status": "string",        /* "complete", "not started", "in progress" */
    "start_date": "timestamp", /* iso 8601 format (yyyy-mm-ddthh:mm:ssz) */
    "due_date": "timestamp",   /* iso 8601 format (yyyy-mm-ddthh:mm:ssz) */
    "end_date": "timestamp"    /* iso 8601 format (yyyy-mm-ddthh:mm:ssz) */
    },
    {
        ...
    }
]
```

### 4.2 Sort Tasks by Tag - `/sort/tags` (GET)

Displays all tasks with given tags first

**Request**:

```
GET /sort/tags?user_id=int&tag=string
```

**Response**:

```json
[

    {
    "name": "string",
    "description": "string",
    "priority": "string",      /* "high", "medium", or "low" */
    "status": "string",        /* "complete", "not started", "in progress" */
    "start_date": "timestamp", /* iso 8601 format (yyyy-mm-ddthh:mm:ssz) */
    "due_date": "timestamp",   /* iso 8601 format (yyyy-mm-ddthh:mm:ssz) */
    "end_date": "timestamp"    /* iso 8601 format (yyyy-mm-ddthh:mm:ssz) */

    },
    {
        ...
    }
]
```

## 5. User Account

### 5.1 Account Creation - `/user/create` (POST)

Creating an account also logs the user in.

**Request**:

```json
{
  "user_name": "string",
  "password": "string"
}
```

**Response**:

```json
{
  "user_id": "int"
}
```

### 5.2 Login - `user/get_user_id` (POST)

**Request**:

```json
{
  "user_name": "string",
  "password": "string"
}
```

**Response**:

```json
{
  "OK: Successfully logged in"
}
```

## 6. Scheduler

### 6.1 Suggest - `/scheduler/suggest/{user_id}` (GET)

Suggests the order in which all the user's tasks should be completed. Based on tasks' due date, priority, and user availability.

**Request**:

```json
{
  "user_id": "number"
}
```

**Response**:

```json
{
  "Suggested completion order": [
    {
      "task_id": "number",
      "name": "string",
      "priority": "string",
      "due_date": "timestamp",
      "estimated_time": "number",
      "weight": "number",
      "day": "number",
      "free_time_range": [
        "time",
        "time"
      ]
    },
    {
      ...
    }
  ]
} 

```

### 6.2 Availability - `/scheduler/set_free_time/{user_id}` (POST)

Records time ranges that tasks can be worked on.
**Request**:

```json
{
  "free_time": [
    [
      "HH:MM", /* 24-hour clock format. Must be a list of tuples, representing a list of time ranges. */
      "HH:MM"
    ],
    ...
  ]
}
```

**Response**:

```json
"Successfully stored free time"
```
