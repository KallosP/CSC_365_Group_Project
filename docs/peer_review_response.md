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

## Schema/API Design Comments
### (Sophia Chang)
1. Added commnents.
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
1. 
## Product Ideas
