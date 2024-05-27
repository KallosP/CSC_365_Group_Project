# API Specification for Task Manager

## 1. Task CRUD

### 1.1. New Task - `/crud/create` (POST)

Create a new task.

**Request**:
```json
{
    "name": "string",
    "description": "string",   /* optional */
    "priority": "string",      /* optional, "high", "medium", or "low" */
    "status": "string",        /* optional, "complete", "not started", "in progress" */
    "start_date": "timestamp", /* optional, ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ) */
    "due_date": "timestamp",   /* optional, ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ) */
    "end_date": "timestamp"    /* optional, ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ) */
}
```

**Response**:
```json
{
    "task_id": "int"
}
```

### 1.2. Read Task - `/crud/read/{task_id}` (GET)

Gets the informaiton associated with an existing task.

**Request**:
```json
{
    "task_id": "int"
}
```

**Response**:
```json
{
    "name": "string",
    "description": "string",
    "priority": "string",      /* "high", "medium", or "low" */
    "status": "string",        /* "complete", "not started", "in progress" */
    "start_date": "timestamp", /* iso 8601 format (yyyy-mm-ddthh:mm:ssz) */
    "due_date": "timestamp",   /* iso 8601 format (yyyy-mm-ddthh:mm:ssz) */
    "end_date": "timestamp"    /* iso 8601 format (yyyy-mm-ddthh:mm:ssz) */
}
```

### 1.3. Update Task - `/crud/update/{task_id}` (POST)

Update an existing task.

**Request**:
```json
{
    "task_id": "int",
    "name": "string",          /* optional */
    "description": "string",   /* optional */
    "priority": "string",      /* optional, "high", "medium", or "low" */
    "status": "string",        /* optional, "complete", "not started", "in progress" */
    "start_date": "timestamp", /* optional, ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ) */
    "due_date": "timestamp",   /* optional, ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ) */
    "end_date": "timestamp"    /* optional, ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ) */
}
```

**Response**:
```json
{
  "OK"
}
```

### 1.4. Delete Task - `/crud/delete/{task_id}` (DELETE)

Delete an existing task (and its tags.)

**Request**:
```json
{
    "task_id": "int"
}
```

**Response**:
```json
{
    "OK"
}
```

## 2. Task Summary

### 2.1. Get Tasks Summary - `/summary` (GET)

Return a summary of all tasks that have been created.

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

### 3.1 Get Tags - `/tags/{task_id}` (GET)

Return a list of all tags associated with the task.

**Response**:
```json
{
  "tags": ["string", "string", ...]
}
```

### 3.2 Adding Tags - `/tags/add/{task_id}` (POST)

Adds tags to a task.

**Request**:
```json
{
  "tags": ["string", "string", ...]
}
```

**Response**:
```json
{
  "OK"
}
```

### 3.3 Removing Tags - `/tags/remove/{task_id}` (POST)

Removes tags from a task

**Request**:
```json
{
  "tags": ["string", "string", ...]
}
```

**Response**:
```json
{
  "OK"
}
```

## 4. Sort Tasks

### 4.1 Sort Tasks by Field - `/sort` (GET)

Sort tasks by provided field (excluding description)  

**Request**:
```
GET /sort?sort_col=string&sort_order=string
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

### 4.2 Sort Tasks by Tag - `/sort/tags` (GET)

Displays all tasks with given tags first

**Request**:
```
GET /sort/tags?tag=string
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
  "OK"
}
```
### 5.2 Login - `user/login` (POST)
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
  "OK"
}
```

