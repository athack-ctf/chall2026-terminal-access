# How to Solve the Challenge?

- Start Burpsuite, and open the website on the burp browser
- Register a user, e.g. user:pass
- Enable the intercept option and go to the Login page to enter your registered credentials
- After clicking login, two requests will be captured (one to verify and  to session), send "session" request to the repeater
- In the repeater, the session request will have a user_id parameter, change the value of this parameter to 1, and click send
- The flag will be present in the response

Run solution.py to solve it instantly to ensure flag can be obtained with the intended path
