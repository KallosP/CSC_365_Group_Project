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
# Case 2

# Case 3
