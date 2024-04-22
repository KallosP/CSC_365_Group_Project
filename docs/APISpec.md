# API Specification for Task Manager

 
 ### TODO: 
#### Implement these attributes in some of the endpoints:
- "tags": ["string"] -> can be used in a filter endpoint
- "creation_time": "string" (Format: YYYY-MM-DD HH:MM:SS) -> GET request
  
### NOTE: the idea is for the API to be similar to Windows Task Manager

## 1. Task Creation

### 1.1. New Task - `/create` (POST)

Create a new task.

**Response**:
```json
{
    "task_id": "string",
    "name": "string",
    "description": "string",
    "priority": "string", /* "high", "medium", or "low" */
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

## 5.
## 6.
## 7.
## 8.
