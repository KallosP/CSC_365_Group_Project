# Case 1: Concurrent User Availability Updates (Lost Updates)
**Scenario:** A user updates their free time/availability using `/scheduler/set_free_time/{user_id}` in two different sessions at the same time.
```mermaid
sequenceDiagram
    participant S1
    participant DB
    participant S2

    Note over S1, S2: User's (user_id 1) free time is initially set to [8:00, 10:00]
    S1->>DB: User updates free time to [9:00, 11:00]
    S1->>DB: UPDATE users SET free_time = :free_time WHERE user_id = :user_id
    S2->>DB: User updates free time to [13:00, 15:00]
    S2->>DB: UPDATE users SET free_time = :free_time WHERE user_id = :user_id
    Note over S1, S2: Both sessions read initial free time: [8:00, 10:00]
    S1->>DB: Transaction is completed and [8:00, 11:00] is written to DB
    S2->>DB: Transaction is completed and [13:00, 15:00] is written to DB, overwriting S1's transaction
    Note over S1, S2: Final state in database for free time is [13:00, 15:00], losing S1's update    
```
**Solution:** Use pessimistic locking, specifically explicit locking via `FOR UPDATE`, to prevent other sessions from updating free time while the current session is in the middle of updating the `users` table. This approach is appropriate since explicit locking is usually used to ensure exclusive access to records to prevent conflicting updates from other transactions, which is this exact issue.

# Case 2: Concurrent Tag Addition (Race Condition Causing Duplicate Insertion)
**Scenario:** A user updates tags to a task using `/tags/add` in two different sessions at the same time.
```mermaid
sequenceDiagram
    participant S1
    participant DB
    participant S2

    S1->>DB: S1 sends query to check if tag exists
    S2->>DB: S2 sends query to check if tag exists
    Note over S1, S2: Both sessions perform the check concurrently

    alt Tag does not exist for both sessions
        DB->>S1: Tag does not exist (response to S1)
        DB->>S2: Tag does not exist (response to S2)
        S1->>DB: S1 adds the tag
        S2->>DB: S2 adds the tag
        Note over S1, S2: Both sessions add the tag leading to a duplicate
    end

    Note over S1, S2: DB ends up with duplicate tags for the same task    
```
**Solution:** A `FOR_UPDATE` could again be used in this example in order to prevent other sessions from updating the tags table, causing the race condition described above.

# Case 3: Concurrent Task Update (Lost Update)
**Scenario:** User reads a due_date from a task and increments the due_date by 1 day, at the same time as another user is updating the due date.
```mermaid
sequenceDiagram
    participant S1
    participant DB
    participant S2

    S1->>DB: S1 reads due_date for task_id 1
    S2->>DB: S2 updates the due date for task_id 1 and sets it to today
    S1->>DB: S1 increments the due date it read and updates it for task_id 1
    S2->>DB: S2 reads task_id 1 and sees the due date is not set to today
```
**Solution:** Avoid using multiple transactions for updating tasks based on existing values. In this example, the initial read by S1 can be executed in the update query by incrementing the due_date in the SQL statement.