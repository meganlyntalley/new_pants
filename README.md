# A New Pair of Pants

This was a fun project I started in an effort to get hands-on with AWS's SAM framework, while implementing several AWS services.

While preparing for a winter camping trip, I came across a *fantastic* pair of weatherproof pants that I knew would keep me warm. Unfortunately, production had halted well before the season was over. Thanks to a generous return policy, however, stock continued to fluctuate throughout the winter.

After getting tired of reloading the brand's site dozens of times a day, I turned to AWS to help me out. I set up the following process:

1. An EventBridge rule triggers a Lambda function on a set schedule.
2. That Lambda function then checks the brand's website for available stock, and writes that information to an EventBus.
3. A second EventBridge rule monitors that EventBus, and publishes a message to an SNS topic when an event indicates that stock is available.
4. That SNS topic distributes this message to any endpoint subscribed to it; in this case, me!

Now this project, as most, is still a work in progress. For one thing, the pair of pants I wanted became available while I was testing my stack. So my python script really just assumes the pants are in stock, it doesn't actually check. For another, the message sent to the SNS topic isn't customized; it simply includes a link to the product listing. But this was a fun, hands-on project that encouraged me to get more involved in AWS. And now I can get regular emails with links to a great pair of pants!

## Want to try it for yourself?

First, use pip to download the required python dependencies:
```sh
$ python3 -m pip install --target ./checkStock/ requests
```

Next, build the SAM templates:
```sh
$ sam build -t template.json
```

Now, publish!
```sh
$ sam deploy --guided
```

A couple minutes after answering SAM's questions, you should start receiving regular emails, telling you whether these pants are back in stock!