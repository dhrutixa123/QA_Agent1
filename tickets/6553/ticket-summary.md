# Summary: 6553

## Feature Summary

This ticket describes the implementation of user login functionality, allowing registered users to access their accounts by providing valid email and password credentials. It includes the design of the login form, input validation, handling of invalid credentials, successful login redirection, password reset link, and user session management.

## Key Flows

* User navigates to the Login page.
* User enters valid email and password.
* User clicks the Login button.
* System authenticates user and redirects to the Dashboard/Home page.
* User enters invalid email or password.
* System displays an error message for invalid credentials.
* User attempts to log in with empty email or password fields.
* System displays an error message for mandatory fields.
* User enters an invalid email format.
* System displays an error message for invalid email format.
* User clicks the "Forgot Password" link.
* System redirects user to the Password Reset page.

## Acceptance Criteria

* The Login page must contain fields for Email Address, Password, a Login Button, and a Forgot Password link.
* Email and Password fields must be mandatory; an error message must be displayed if they are empty.
* The system must validate the email format and display an error message for invalid formats.
* Entering incorrect email or password must display the message "Invalid email or password."
* Upon successful authentication with valid credentials, the user must be redirected to the Dashboard/Home page.
* Clicking the "Forgot Password" link must redirect the user to the Password Reset page.
* A user session must be created after successful login, keeping the user logged in until logout or session expiration.

## Edge Cases

* Empty email field submission.
* Empty password field submission.
* Invalid email format (e.g., missing '@', '.com').
* Incorrect email and password combination.
* User attempting to log in with a non-existent account.
* Session expiration while the user is active.
* User attempting to access protected pages without an active session.