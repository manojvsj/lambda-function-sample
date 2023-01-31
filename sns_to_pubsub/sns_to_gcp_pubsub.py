import json
import os
from google.cloud import pubsub_v1

import boto3
from botocore.exceptions import ClientError

def main(event, context):
    project_id = os.environ['PROJECT_ID']
    topic_name = os.environ['TOPIC_NAME']
    if event.get("Records"):
        message = event['Records'][0]['Sns']['Message']
        print("From SNS to pub/sub: " + message)
        publish_message(project_id, topic_name, message)
        return message
    else:
        return "No Records found in the event"


def publish_message(project_id, topic_name, message):
    """Publishes multiple messages to a Pub/Sub topic."""
    # Location of the service account key that should be bundled with your
    # function.
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "gcp-key.json"
    secret_value = get_secret()
    publisher = pubsub_v1.PublisherClient(credentials = secret_value)
    # The `topic_path` method creates a fully qualified identifier
    # in the form `projects/{project_id}/topics/{topic_name}`
    topic_path = publisher.topic_path(project_id, topic_name)
    # When you publish a message, the client returns a future.
    future = publisher.publish(topic_path, data=message.encode("utf-8"),
            origin='sns')
    print(future.result())

def get_secret():

    secret_name = "gcp_key"
    region_name = "eu-west-1"
    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e
    # Decrypts secret using the associated KMS key.
    secret = get_secret_value_response['SecretString']
    return secret