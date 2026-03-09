import json
from playwright.sync_api import sync_playwright, expect

# --- Configuration ---
BASE_URL = "https://stellar.annaizu.com"
VALID_EMAIL = "siya@yopmail.com"
VALID_PASSWORD = "Test@123"
INVALID_EMAIL_PROD = "wrong@example.com"
INVALID_PASSWORD_PROD = "wrongpass"

# --- Test Functions ---

def test_TC_001(page, results):
    test_id = "TC-001"
    try:
        page.goto(BASE_URL + "/login")
        page.wait_for_selector("#loginform-email")

        # 2. Leave Email Address field empty
        # 3. Enter a valid password (e.g., "password123")
        page.fill("#loginform-password", "password123")
        
        # 4. Click Login button
        page.click("button[type=\"submit\"]")

        # Expected Result: An error message "Email cannot be blank." appears below the email field.
        email_error_selector = ".field-loginform-email .invalid-feedback"
        page.wait_for_selector(email_error_selector)
        expect(page.locator(email_error_selector)).to_have_text("Email cannot be blank.")
        
        print(f"[PASS] {test_id}")
        results.append({"id": test_id, "status": "PASS"})
    except Exception as e:
        screenshot_path = f"C:/Users/alwis/OneDrive/Desktop/qa-automation-agents - Copy/qa-automation-agents - Copy/tickets/6553/screenshots/{test_id}-error.png"
        page.screenshot(path=screenshot_path)
        print(f"[FAIL] {test_id} - {str(e)}")
        results.append({"id": test_id, "status": "FAIL", "reason": str(e)})

def test_TC_002(page, results):
    test_id = "TC-002"
    try:
        page.goto(BASE_URL + "/login")
        page.wait_for_selector("#loginform-email")

        # 2. Enter a valid email address (e.g., "test@example.com")
        page.fill("#loginform-email", "test@example.com")
        # 3. Leave Password field empty
        
        # 4. Click Login button
        page.click("button[type=\"submit\"]")

        # Expected Result: An error message "Password cannot be blank." appears below the password field.
        password_error_selector = ".field-loginform-password .invalid-feedback"
        page.wait_for_selector(password_error_selector)
        expect(page.locator(password_error_selector)).to_have_text("Password cannot be blank.")
        
        print(f"[PASS] {test_id}")
        results.append({"id": test_id, "status": "PASS"})
    except Exception as e:
        screenshot_path = f"C:/Users/alwis/OneDrive/Desktop/qa-automation-agents - Copy/qa-automation-agents - Copy/tickets/6553/screenshots/{test_id}-error.png"
        page.screenshot(path=screenshot_path)
        print(f"[FAIL] {test_id} - {str(e)}")
        results.append({"id": test_id, "status": "FAIL", "reason": str(e)})

def test_TC_003(page, results):
    test_id = "TC-003"
    try:
        page.goto(BASE_URL + "/login")
        page.wait_for_selector("#loginform-email")

        # 2. Enter an invalid email format (e.g., "invalid-email")
        page.fill("#loginform-email", "invalid-email")
        # 3. Enter a valid password (e.g., "password123")
        page.fill("#loginform-password", "password123")
        
        # 4. Click Login button
        page.click("button[type=\"submit\"]")

        # Expected Result: An error message "Email is not a valid email address." appears below the email field.
        email_format_error_selector = ".field-loginform-email .invalid-feedback"
        page.wait_for_selector(email_format_error_selector)
        expect(page.locator(email_format_error_selector)).to_have_text("Email is not a valid email address.")
        
        print(f"[PASS] {test_id}")
        results.append({"id": test_id, "status": "PASS"})
    except Exception as e:
        screenshot_path = f"C:/Users/alwis/OneDrive/Desktop/qa-automation-agents - Copy/qa-automation-agents - Copy/tickets/6553/screenshots/{test_id}-error.png"
        page.screenshot(path=screenshot_path)
        print(f"[FAIL] {test_id} - {str(e)}")
        results.append({"id": test_id, "status": "FAIL", "reason": str(e)})

def test_TC_004(page, results):
    test_id = "TC-004"
    try:
        page.goto(BASE_URL + "/login")
        page.wait_for_selector("#loginform-email")

        # 2. Enter a valid registered email address
        page.fill("#loginform-email", VALID_EMAIL)
        # 3. Enter an incorrect password
        page.fill("#loginform-password", INVALID_PASSWORD_PROD)
        
        # 4. Click Login button
        page.click("button[type=\"submit\"]")

        # Expected Result: A general error message "Invalid email or password." appears.
        page.locator('text="Invalid email or password."').wait_for()
        
        print(f"[PASS] {test_id}")
        results.append({"id": test_id, "status": "PASS"})
    except Exception as e:
        screenshot_path = f"C:/Users/alwis/OneDrive/Desktop/qa-automation-agents - Copy/qa-automation-agents - Copy/tickets/6553/screenshots/{test_id}-error.png"
        page.screenshot(path=screenshot_path)
        print(f"[FAIL] {test_id} - {str(e)}")
        results.append({"id": test_id, "status": "FAIL", "reason": str(e)})

def test_TC_005(page, results):
    test_id = "TC-005"
    try:
        page.goto(BASE_URL + "/login")
        page.wait_for_selector("#loginform-email")

        # 2. Enter a non-existent email address
        page.fill("#loginform-email", "nonexistent@example.com")
        # 3. Enter any password
        page.fill("#loginform-password", "anypassword")
        
        # 4. Click Login button
        page.click("button[type=\"submit\"]")

        # Expected Result: A general error message "Invalid email or password." appears.
        page.locator('text="Invalid email or password."').wait_for()
        
        print(f"[PASS] {test_id}")
        results.append({"id": test_id, "status": "PASS"})
    except Exception as e:
        screenshot_path = f"C:/Users/alwis/OneDrive/Desktop/qa-automation-agents - Copy/qa-automation-agents - Copy/tickets/6553/screenshots/{test_id}-error.png"
        page.screenshot(path=screenshot_path)
        print(f"[FAIL] {test_id} - {str(e)}")
        results.append({"id": test_id, "status": "FAIL", "reason": str(e)})

def test_TC_006(page, results):
    test_id = "TC-006"
    try:
        page.goto(BASE_URL + "/login")
        page.wait_for_selector("a[href=\"/forgot-password\"]")

        # 2. Click on the "Forgot Password" link
        page.click("a[href=\"/forgot-password\"]")

        # Expected Result: User is redirected to the Password Reset page.
        expect(page).to_have_url(BASE_URL + "/forgot-password")
        
        print(f"[PASS] {test_id}")
        results.append({"id": test_id, "status": "PASS"})
    except Exception as e:
        screenshot_path = f"C:/Users/alwis/OneDrive/Desktop/qa-automation-agents - Copy/qa-automation-agents - Copy/tickets/6553/screenshots/{test_id}-error.png"
        page.screenshot(path=screenshot_path)
        print(f"[FAIL] {test_id} - {str(e)}")
        results.append({"id": test_id, "status": "FAIL", "reason": str(e)})

def test_TC_007(page, results):
    test_id = "TC-007"
    try:
        # 1. Attempt to navigate directly to a protected page URL (e.g., "/dashboard")
        page.goto(BASE_URL + "/dashboard") 

        # Expected Result: User is redirected to the Login page.
        expect(page).to_have_url(BASE_URL + "/login")
        
        print(f"[PASS] {test_id}")
        results.append({"id": test_id, "status": "PASS"})
    except Exception as e:
        screenshot_path = f"C:/Users/alwis/OneDrive/Desktop/qa-automation-agents - Copy/qa-automation-agents - Copy/tickets/6553/screenshots/{test_id}-error.png"
        page.screenshot(path=screenshot_path)
        print(f"[FAIL] {test_id} - {str(e)}")
        results.append({"id": test_id, "status": "FAIL", "reason": str(e)})

def test_TC_008(page, results):
    test_id = "TC-008"
    try:
        page.goto(BASE_URL + "/login")
        page.wait_for_selector("#loginform-email")

        # 2. Enter a valid registered email address
        page.fill("#loginform-email", VALID_EMAIL)
        # 3. Enter the correct password
        page.fill("#loginform-password", VALID_PASSWORD)
        
        # 4. Click Login button
        page.click("button[type=\"submit\"]")

        # Expected Result: User is successfully authenticated and redirected to the Dashboard/Home page.
        page.wait_for_url(BASE_URL + "/") 
        expect(page).to_have_url(BASE_URL + "/")
        
        print(f"[PASS] {test_id}")
        results.append({"id": test_id, "status": "PASS"})
    except Exception as e:
        screenshot_path = f"C:/Users/alwis/OneDrive/Desktop/qa-automation-agents - Copy/qa-automation-agents - Copy/tickets/6553/screenshots/{test_id}-error.png"
        page.screenshot(path=screenshot_path)
        print(f"[FAIL] {test_id} - {str(e)}")
        results.append({"id": test_id, "status": "FAIL", "reason": str(e)})

# --- Main Execution Block ---
def run_tests():
    results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=500)
        page = browser.new_page()

        # Run test functions here
        test_TC_001(page, results)
        test_TC_002(page, results)
        test_TC_003(page, results)
        test_TC_004(page, results)
        test_TC_005(page, results)
        test_TC_006(page, results)
        test_TC_007(page, results)
        test_TC_008(page, results)

        browser.close()

    print(json.dumps({"results": results}))

if __name__ == "__main__":
    run_tests()