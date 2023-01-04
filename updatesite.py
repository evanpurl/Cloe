import requests
import base64
import datetime


wordpress_user = "EvanPurl"
wordpress_password = "2e1U CUkP nWQ4 aDc5 5bOh l4HP"
wordpress_credentials = wordpress_user + ":" + wordpress_password
wordpress_token = base64.b64encode(wordpress_credentials.encode())
wordpress_header = {'Authorization': 'Basic ' + wordpress_token.decode('utf-8')}


async def update_wordpress_post():
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M")
    twelve = datetime.datetime.strptime(current_time, "%H:%M")

    api_url = 'https://nitelifesoftware.com/wp-json/wp/v2/posts/'
    post_id = '627'
    data = {
        'status': 'publish',
        'content': f"Last Ping: {twelve.strftime('%r')} CST"
    }
    requests.post(api_url + post_id, headers=wordpress_header, json=data)  # Posts the update here.
