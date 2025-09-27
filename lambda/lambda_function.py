import json
import urllib.request
import urllib.parse

def lambda_handler(event, context):
    city = None
    if "queryStringParameters" in event and event["queryStringParameters"]:
        city = event["queryStringParameters"].get("city")

    if not city:
        return {
            "statusCode": 400,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": "Missing 'city' query parameter"})
        }

    try:
        api_key = "0d13d4b9609bd0c9bab4badb869fd1a2"
        encoded_city = urllib.parse.quote(city.strip())
        url = f"http://api.openweathermap.org/data/2.5/weather?q={encoded_city}&appid={api_key}&units=metric"

        with urllib.request.urlopen(url) as response:
            data = response.read()
            weather = json.loads(data)

        result = {
            "city": weather.get("name", city),
            "temperature": weather["main"]["temp"],
            "description": weather["weather"][0]["description"]
        }

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"  # allow browser calls
            },
            "body": json.dumps(result)
        }

    except urllib.error.HTTPError as e:
        error_body = e.read().decode()
        return {
            "statusCode": e.code,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": error_body})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": str(e)})
        }
