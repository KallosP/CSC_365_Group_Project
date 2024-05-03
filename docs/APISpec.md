# API Specification for Task Manager

## 1. Task CRUD

### 1.1. New Task - `/crud/create` (POST)

Create a new task.

**Request**:
```json
{
    "task_id": "int",
    "name": "string",
    "description": "string",
    "priority": "string", /* "high", "medium", or "low" */
    "status": "string", /* "complete", "not started", "in progress" */
    "start_date": "timestamp", /* ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ) */
    "due_date": "timestamp", /* ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ) */
    "end_date": "timestamp" /* ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ) */
}
```

**Response**:
```json
{
    "success": "boolean"
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
    "priority": "string", /* "high", "medium", or "low" */
    "status": "string", /* "complete", "not started", "in progress" */
    "start_date": "timestamp", /* ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ) */
    "due_date": "timestamp", /* ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ) */
    "end_date": "timestamp" /* ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ) */
}
```

### 1.3. Update Task - `/crud/update/{task_id}` ()

Update an existing task.

**Request**:
```json
{
    "task_id": "int",
    "name": "string", /* optional */
    "description": "string", /* optional */
    "priority": "string", /* optional, "high", "medium", or "low" */
    "status": "string", /* optional, "complete", "not started", "in progress" */
    "start_date": "timestamp", /* optional, ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ) */
    "due_date": "timestamp", /* optional, ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ) */
    "end_date": "timestamp" /* optional, ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ) */
}
```

**Response**:
```json
{
    "name": "string",
    "description": "string",
    "priority": "string", /* "high", "medium", or "low" */
    "status": "string", /* "complete", "not started", "in progress" */
    "start_date": "timestamp", /* ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ) */
    "due_date": "timestamp", /* ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ) */
    "end_date": "timestamp" /* ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ) */
}
```

### 1.4. Delete Task - `/crud/delete/{task_id}` (DELETE)

Delete an existing task.

**Request**:
```json
{
    "task_id": "int"
}
```

**Response**:
```json
{
    "success": "boolean"
}
```

## 2. Task Summary

### 2.1. Get Tasks Summary - `/summary` (GET)

Return a summary of total tasks created and number of each status type.

**Response**:
```json
{
  "number_of_tasks": "number",
  "active_tasks": "number",
  "disabled_tasks": "number",
  "suspended_tasks": "number"
}
```

### 2.2. Get Task Info - `/summary/{task_id}` (GET)

Return information about an existing task, it's name, state, and resource utilization.

**Response**:
```json
{
  "name": "string",
  "status": "string",
  "cpu_usage": "number",
  "memory_usage": "number"
}
```

## 3. Task Modification

### 3.1. End Task - `/remove/{task_id}` (POST)

Stops and removes a task from task manager table.

**Response**:
```json
{
  "success": "boolean"
}
```

### 3.2. Suspend Task - `/suspend/{task_id}` (POST)

Suspends a running task temporarily and frees resources.

**Response**:
```json
{
  "success": "boolean"
}
```

### 3.3. Enable Task - `/enable/{task_id}` (POST)

Starts a suspended task and reallocates resources.

**Response**:
```json
{
  "success": "boolean"
}
```

## 4. Utilization

### 4.1. Get Usage - `/utilization` (GET)

Get CPU and memory percent usage.

**Response**:
```json
{
  "cpu_usage": "number",
  "memory_usage": "number"
}
```

## 5. Tag Modification

### 5.1 Gets Tags - `/tags/{task_id}` (GET)

Return a list of all tags associated with the task.

**Response**:
```json
{
  "tags": ["string", "string", ...]
}
```

### 5.2 Adding Tags - `tags/{task_id}/add` (POST)

**Request**:
```json
{
  "tags": ["string", "string", ...]
}
```

Adds tags to a task.


**Response**:
```json
{
  "success": "boolean"
}
```

### 5.3 Removing Tags - `tags/{task_id}/remove` (POST)

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
  "success": "boolean"
}
```

## 6. Sort Tasks

### 6.1 Sort Tasks by Tag - `sort/tags` (POST)

Displays all tasks with given tags first

**Request**:
```json
{
  "tags": ["string", "string", ...]
}
```

 **Response**:
```json
[
 {
  "name": "string",
  "status": "string",
  "cpu_usage": "number",
  "memory_usage": "number"
  "tags": ["string", "string", ...]
 }
] 
```

### 6.2 Sort Tasks by field - `sort/{field}` (POST)
 **Response**:
```json
[
 {
  "name": "string",
  "status": "string",
  "cpu_usage": "number",
  "memory_usage": "number"
  "tags": ["string", "string", ...]
 }
] 
```
