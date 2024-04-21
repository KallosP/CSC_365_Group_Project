# API Specification for Task Manager

 
 ### TODO: 
#### Implement these attributes in some of the endpoints:
- "status": "string"  ("inactive", "active", or "suspended") -> can probably have a POST/GET, one for setting the status and one for getting status
- "tags": ["string"] -> can be used in a filter endpoint
- "creation_time": "string" (Format: YYYY-MM-DD HH:MM:SS) -> GET request

## 1. Task Creation

### 1.1. New Task - `/create` (POST)

Create a new task.

**Response**:

```json
{
    "name": "string",
    "description": "string",
    "priority": "string", /* "high", "medium", or "low" */
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
