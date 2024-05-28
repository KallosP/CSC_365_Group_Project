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

1. The current say of using SQLalchemy is resistant to sql injection and can be used for unknown variables.
2. User login needs to be fixed.
3. TODO is not implemented yet so it is still there.
4. BaseModel is now removed.
5. MetaData is used in sort.py to get the metadata from the tables 'tasks' and 'tags' from our database.
6. This is now fixed, the redundant database connection is gone with all sql statements in one database connection.
7. HTTP execeptions added to task.py and all other endpoints
8. I do not believe that we have to use sqlalchemy.text to prevent injection attacks, using sqlalchemy's orm features should also prevent this
9. Since the user can edit any field, `RETURNING *` must be used to capture all possible edits to a field.
10. API now matches the example flow and outputs the user id
11. The API Spec now matches the API outputs for user/login and user/create
12. The query is done after the connection is opened, it is just constructed beforehand. Variable renamed from json to tasks_list to make things more understandable.
13. Commented out code is now removed.
14. Get tags enpoint updated to GET from POST.

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

### (Emanuel Gonzalez)

1. Not a priority at the moment, but can add later if time allows.
2. The end_date column serves as the date of completion.
3. Will consider.
4. Seems redundant / cluttered if we are to implement a projects table.
5. Good idea, will consider implementing.
6. Would decrease clutter/messiness for `tags` table, though not a priority at the moment. Will consider changing in the future.
7. Will consider, but not a big priority since the user can already customize tags through the tag endpoints.
8. This would be redundant, as the user can already update the tags with the relevant tag endpoints.
9. Great idea, just added it.
10. We are considering adding statistical analysis in a future complex endpoint which would cover this.
11. Will consider adding this.
12. Will consider adding this, but each user should really only be concerned with their own tasks.
13. Done, great idea.
14. Seems like a cool idea, but we don't have anything at the moment needing additional user auth. Will keep in mind.

### (Srish Maulik)

1. This defenitly needs to be implemented and will be when we update our login system to be stateless.
2. This could be a good idea but for our api we decided to just have these three levels.
3. This makes sense and we will consider adding this, for a small amount of data it doesn't matter too much. It is redundant because every tag refers to a task.
4. task/read switched from POST to GET.
5. task/read API and API spec now line up
6. responses are now more descriptive and have 400 level codes if they are errors
7. log out is now an endpoint
8. task/read switched from POST to PATCH
9. user/create now returns a unique ID in API and API spec
10. responses are more consistent now.
11. This is a good idea but we basically have that functionality through the sorting feature since you can filter by due date.
12. User Name now cannot be an empty string. Priority is now set by default to low.
13. get tags now is GET instead of POST

## Test Results

### (Sophia Chang)

All tests work as intended/no errors found.

### (Emanuel Gonzalez)

All tests work as intended/no errors found.

### (Srish Maulik)

All tests work as intended/no errors found. (More detailed responses have been added since tests were ran)

### (Sri Bala)

## Product Ideas

### (Sophia Chang)

1. Though a fun suggestion, this API is not intended to be gamified. Rather, it's moreso meant to be a practical tool used for organizing tasks. However, the idea of the user having/setting a goal and checking it off sounds like a good feature. Will consider this as a feature for the complex endpoint.
2. This idea sounds interesting. Incorporating shared tasks between users could be useful in the case that a group/team is using the API. Something that we'd have to consider in implementing this would be handling concurrency issues, such as when two users update a task at the same time. Additionally, this can be expanded to allow users to create groups/organizations where they can invite other users to join/work on shared tasks.

### (Emanuel Gonzalez)

1. Task sharing is a great suggestion, but I'm not sure how "complex" it could be.
2. This is a good idea, although it might be more intuitive to relate dependent tasks through a "projects" table if we were to go this route.

### (Srish Maulik)

1. A reminder system seems like a good idea for a task managing service to provide. However, since we are making an API we do not have a good way to communicate to the user to remind them of anything.
2. We have implemented a scheduler endpoint which does what you are suggesting here.
3. Sharing tasks does seem like a good idea to implement as it has many practical use cases

### (Sri Bala)
