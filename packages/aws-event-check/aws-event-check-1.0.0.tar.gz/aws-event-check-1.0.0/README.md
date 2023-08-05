# AWS Event Check

* Annotation based library to check aws event.
* Checking event to avoid internal call by lambda function.
* Supporting AWS Cloud Watch trigger events.
* Supporting AWS S3 trigger event.
* Supporting AWS API Gateway event.


### Examples 

* S3 trigger check :
    * Checking for event Records.

```
from aws.event import s3_trigger_event_check


@s3_trigger_event_check
def handler(event, context):
    try:
        pass
    except Exception as e:
        raise e
```

* Cloud Watch Event :
    * Checking for event id.

```
from aws.event import cloud_watch_trigger_event_check


@cloud_watch_trigger_event_check
def handler(event, context):
    try:
        pass
    except Exception as e:
        raise e
```

* API Gateway Event :

    * Checking only http method.

```
from aws.event import api_gateway_trigger_event_check


@api_gateway_trigger_event_check
def handler(event, context):
    try:
        pass
    except Exception as e:
        raise e
```
