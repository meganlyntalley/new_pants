import json
import logging
import boto3
import requests

# This is a sample AWS Lambda function to check if a requested pair of pants are
# in stock at Eddie Bauer. It requires an input event with the following fields:
# {
# "size": "12",
# "sizeType": "Tall",
# "color": "Black"
# }
#

# Initialize logger and set default logging level
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Check whether product is in stock
def check_stock(event):
    logger.info("Checking stock for product matching: " + json.dumps(event, indent=2))
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"}
    url = "https://www.eddiebauer.com/p/prod2650019/womens-guide-pro-flex-lined-jogger-pants"
    logger.debug("Beginning http request to url {} with headers {}.".format(url, headers))
    r = requests.get(url, headers = headers)
    logger.debug("Processing event text:".format(r.text))
    # Here is where I'd implement the functionality to check whether the exact product requested
    # is in stock, but unfortunately the product sold out before I could!
    result = {
        "in_stock": "true",
        "url": url
    }
    return result

# Main function
def lambda_handler(event, context):
    logger.info("Received event: " + json.dumps(event, indent=2))

    # Check that the incoming event has required parameters
    if "size" in event and "sizeType" in event and "color" in event:
        logger.info("Received event has all required fields.")
    else:
        raise Exception('Received event does not have all required fields')

    # Check product stock
    stock_info = check_stock(event)

    # Create event bus entries
    entries = {
        'Source': 'stock.info',
        'DetailType': 'string',
        'Detail': json.dumps(stock_info, separators=(',', ':')),
        'EventBusName': 'NewPantsEventBus'
    }

    # Send event to event bus
    logger.info("Sending the following events to the event bus: " + json.dumps(entries))
    client = boto3.client('events')
    response = client.put_events(
        Entries=[entries]
    )
    logger.info("Sent events to the event bus with result {}.".format(response))
