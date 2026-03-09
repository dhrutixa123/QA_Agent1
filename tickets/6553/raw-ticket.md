# Ticket: 6553 - Login Functionality

## Description
<div><p><strong>Title:</strong> User should be able to log in to the system using valid credentials. </p><p><strong>User Story:</strong><br>
As a <strong>registered user</strong>,<br>
I want to <strong>log in to the system using my email and password</strong>,<br>
So that <strong>I can access my account and use the application features.</strong> </p><br> </div>

## User Story
N/A Points

## Acceptance Criteria
<div><h2>Acceptance Criteria </h2><h3>1. Login Form </h3><p>The system should provide a <strong>Login page</strong> with the following fields: </p><ul><li><p>Email Address </p> </li><li><p>Password </p> </li><li><p>Login Button </p> </li><li><p>Forgot Password link </p> </li> </ul><hr><h3>2. Mandatory Fields Validation </h3><ul><li><p>Email and Password fields must not be empty. </p> </li><li><p>If fields are empty, the system should display an error message. </p> </li> </ul><hr><h3>3. Email Format Validation </h3><ul><li><p>The system should validate the email format. </p> </li><li><p>If the email format is invalid, the system should show an appropriate error message. </p> </li> </ul><hr><h3>4. Invalid Credentials </h3><ul><li><p>If the user enters incorrect email or password, the system should display an error message such as:<br><strong>&quot;Invalid email or password.&quot;</strong> </p> </li> </ul><hr><h3>5. Successful Login </h3><ul><li><p>If valid credentials are entered: </p><ul><li><p>The system should authenticate the user. </p> </li><li><p>The user should be redirected to the <strong>Dashboard / Home page</strong>. </p> </li> </ul> </li> </ul><hr><h3>6. Forgot Password </h3><ul><li><p>Clicking on <strong>Forgot Password</strong> should redirect the user to the <strong>Password Reset page</strong>. </p> </li> </ul><hr><h3>7. Session Management </h3><ul><li><p>After successful login, the system should create a <strong>user session</strong>. </p> </li><li><p>The user should remain logged in until they <strong>log out or the session expires</strong>. </p> </li> </ul><br> </div>
