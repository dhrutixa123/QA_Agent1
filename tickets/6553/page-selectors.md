| Element | Selector | Notes |
| ------- | -------- | ----- |
| Email Input | `#loginform-email` | id="loginform-email", name="LoginForm[email]" |
| Password Input | `#loginform-password` | id="loginform-password", name="LoginForm[password]" |
| Sign In Button | `button[type="submit"]` | Exact text from DOM: "Sign In" |
| Forgot Password Link | `a[href="/forgot-password"]` | Exact text from DOM: "Forgot password?" |
| Email Empty Error | `.field-loginform-email .invalid-feedback` | "Email cannot be blank." — from DOM scrape, parent_class: 'mb-2 field-loginform-email required' |
| Password Empty Error | `.field-loginform-password .invalid-feedback` | "Password cannot be blank." — from DOM scrape, parent_class: 'mb-3 field-loginform-password required' |
| Invalid Email Format Error | `.field-loginform-email .invalid-feedback` | "Email is not a valid email address." — from DOM scrape, parent_class: 'mb-2 field-loginform-email required' |
| General error message "Invalid email or password." | | Not found in LIVE DOM DATA |