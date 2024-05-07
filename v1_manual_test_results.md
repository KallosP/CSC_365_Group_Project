# Example workflow
<Alice is a new project manager for a retail website. Naturally, she wants to keep organized and decides she wants to start by creating three tasks. Initially she calls POST /user/create to create an account with the Task Manager API, setting her username to "Alice" and her password to "password123". After succesfully being stored in the system and receiving her unique ID (response from POST /user/create), she calls POST /crud/create and fills in the fields for her first task "Design and Prototype". After receiving an "OK" response, she successfully inserts her other tasks, "Documentation" and "Testing/Debugging", the same way.>

# Testing results
<Repeated for each step of the workflow>
1. The curl statement called. You can find this in the /docs site for your 
API under each endpoint. For example, for my site the /catalogs/ endpoint 
curl call looks like:
curl -X 'GET' \
  'https://centralcoastcauldrons.vercel.app/catalog/' \
  -H 'accept: application/json'
2. The response you received in executing the curl statement.
