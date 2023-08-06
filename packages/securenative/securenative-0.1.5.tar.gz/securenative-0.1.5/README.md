# Python SDK for Secure Native

## How to get it?
the python SDK is published to PyPi so you can just use `pip` to install it:
```bash
pip install securenative
```

## Initialize the SDK
Go to the settings page of your SecureNative account and find your API key, afterwards add this line on your application main module.
```python
import securenative

# Many lines of code ...

if __name__=='__main__':
    # Your bootstrap code
    securenative.init('API_KEY') # Should be called before any other call to secure native
```

## Tracking Events (async)
Once the SDK has been initialized, you can start sending new events with the `track` function:
```python
import securenative
from securenative.event_options import Event, User

def my_login_function():
    # Many lines of code ...
    
    event = Event( # Build the event from the request's context
        event_type=securenative.event_types.login,
        ip='35.199.23.1',
        remote_ip='35.199.23.2',
        user_agent='Mozilla/5.0 (Linux; U; Android 4.4.2; zh-cn; GT-I9500 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko)Version/4.0 MQQBrowser/5.0 QQ-URL-Manager Mobile Safari/537.36',
        sn_cookie_value='eyJjaWQiOiJkYzgyYjdhZS00ODFkLTQyODItYTMyZC0xZTU1Njk2ZjNmZTQiLCJmcCI6Ijk5NGYzZjVjZTRiYWUwODQzMTRhOTFkNzgyN2I1MWYuMjQ3MDBmOWYxOTg2ODAwYWI0ZmNjODgwNTMwZGQwZWQifQ',
        user=User(
            user_id='1',
            user_email='1@example.com',
            user_name='example example'
        )
    )
    
    # Track it:
    securenative.track(event)
    
    # Many lines of code ...

```

## Verification Events (sync)
Once the SDK has been initialized, you can protect sensitive operation by calling the `verify` function, this function will return the risk analysis of the current user.

```python
import securenative
from securenative.event_options import Event, User

def my_change_password_function():
    # Many lines of code...
    
    event = Event( # Build the event from the request's context
            event_type=securenative.event_types.verify,
            ip='35.199.23.1',
            remote_ip='35.199.23.2',
            user_agent='Mozilla/5.0 (Linux; U; Android 4.4.2; zh-cn; GT-I9500 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko)Version/4.0 MQQBrowser/5.0 QQ-URL-Manager Mobile Safari/537.36',
            sn_cookie_value='eyJjaWQiOiJkYzgyYjdhZS00ODFkLTQyODItYTMyZC0xZTU1Njk2ZjNmZTQiLCJmcCI6Ijk5NGYzZjVjZTRiYWUwODQzMTRhOTFkNzgyN2I1MWYuMjQ3MDBmOWYxOTg2ODAwYWI0ZmNjODgwNTMwZGQwZWQifQ',
            user=User(
                user_id='1',
                user_email='1@example.com',
                user_name='example example'
            )
        )
     
    result = securenative.verify(event)
    if result['riskLevel'] == 'high':
        return 'Cannot change password'
    elif result['riskLevel'] == 'medium':
        return 'MFA'
     
     # Many lines of code...
```

## Verifying Incoming Webhooks
You can use the SDK to verify incoming webhooks from Secure Native, just call the `veriy_webhook` function which return a boolean which indicates if the webhook came from Secure Native servers.
```python
import securenative

@post('/sn/webhook')
def sn_webhook_handler(headers, body):
    sig_header = headers["X-SecureNative"]
    if securenative.verify_webhook(sig_header, body):
        # Handle the webhook
        level = body['riskLevel']
        pass
    else:
        # This reqeust wasn't sent from Secure Native servers, you can dismiss/investigate it
        pass
    
```
