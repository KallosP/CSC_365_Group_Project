# Peer Review Responses
## Code Review Comments
### (Sophia Chang)
1. Removed unused files.
2. Not a priority at the moment, can add later if more time.
3. Removed potion shop code.
4. Moved V1, V2, and peer review to `/docs`.
5. Removed unused imports from `/api` python files.
6. Since the user can edit any field, `RETURNING *` must be used to capture all possible edits to a field.
7. Added clarifying comments where needed.
8. This feature is not finished.
9. Removed redundant engine creation.
10. Changed spec responses to match.
11. Changed return to `user_id` from `OK`
12. Creating an account also logs the user in; added clarifying comment in spec.
13. Updated `ExampleFlows.md`.
14. Works well enough for now, will consider for future.
### (Emanuel Gonzalez)
1. Updated the API specification to match the code for each endpoint path.
2. Updated the API specification to use query parameters for sort endpoints instead of request bodies.
3. Updated spec responses.
4. Comments added in previous code review response.
5. Endpoint paths are consistent.
6. Updated the response format.
7. Adding, getting, and removing tags are in separate routes.
8. Adjusted the API spec for consistency.
9. Since the user can edit any field, `RETURNING *` must be used to capture all possible edits to a field.
10. Adjusted the API spec for consistency.
11. Docstrings and comments have been added.
12. All queries already use parameterized input.
13. Combined SQL queries.
14. Removed unused imports and commented-out code.
### (Srish Maulik)
### (Sri Bala)

## Schema/API Design Comments
### (Sophia Chang)
1. Added comments.
2. Reversed ID in URL
3. Changed to return consistent `OK` responses and added more descriptive messages. 
4. Added a logout function.
5. Creating tags allows for more freedom on the user's part, will consider implementing a used tags function.
6. Changed to `POST` in spec.
7. Would decrease clutter/messiness for `tags` table, though not a priority at the moment. Will consider changing in the future.
8. Removed extra wording.
9. This would result in unnecessary entries on the user's part. The spec specifies those fields (apart from name) as optional, so they can simply be excluded if the user does not need them.
10. Fixed so that name is required.
11. Similar to `9`, if the user doesn't want to use those fields, then they exclude them from the request. All excluded information is set to `NULL`.
12. Will consider this for a future endpoint.

## Test Results
### (Sophia Chang)
All tests work as intended/no errors found.
### (Emanuel Gonzalez)
### (Srish Maulik)
### (Sri Bala)

## Product Ideas
### (Sophia Chang)
1. Though a fun suggestion, this API is not intended to be gamified. Rather, it's moreso meant to be a practical tool used for organizing tasks. However, the idea of the user having/setting a goal and checking it off sounds like a good feature. Will consider this as a feature for the complex endpoint.
2. This idea sounds interesting. Incorporating shared tasks between users could be useful in the case that a group/team is using the API. Something that we'd have to consider in implementing this would be handling concurrency issues, such as when two users update a task at the same time. Additionally, this can be expanded to allow users to create groups/organizations where they can invite other users to join/work on shared tasks.
### (Emanuel Gonzalez)

### (Srish Maulik)
### (Sri Bala)
