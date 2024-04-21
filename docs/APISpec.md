# API Specification for Task Manager

## 1. Task Creation

### 1.1. New Task - `/create` (POST)

Create a new task.

**Response**:

```json
{
    "name": "string",
    "description": "string",
    "priority": "string", /* "high", "medium", or "low" */
    "status": "string", /* "inactive", "active", or "suspended" */
    "tags": ["string"],
    "creation_time": "string" /* Format: YYYY-MM-DD HH:MM:SS */
}
```
## 2. Task Summary

### 2.1. Get Task Summary - `/summary` (GET)

Return a summary of total tasks created and number of each status type.

**Response**:
```json
{
  "number_of_tasks": "number",
  "active_tasks": "number",
  "inactive_tasks": "number",
  "suspended_tasks": "number"
}
```  
## 3.
## 4.
## 5.
## 6.
## 7.
## 8.
