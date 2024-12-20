import json
import boto3
import json
import base64
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    print("Received event: " + json.dumps(event["body"]))

    client = boto3.client("bedrock-runtime", region_name="us-east-1")
    model_id = "amazon.titan-text-premier-v1:0"
    systemPrompt = "Resuma em palavras elegantes os seguintes comentários sobre um produto e responda em português"
    prompt = json.dumps(base64.b64decode(event["body"]))["comments"]

    native_request = {
        "inputText": f"{systemPrompt}:{prompt}",
        "textGenerationConfig": {
            "maxTokenCount": 512,
            "temperature": 0.5,
        },
    }

    request = json.dumps(native_request)

    try:
        response = client.invoke_model(modelId=model_id, body=request)
    except (ClientError, Exception) as e:
        print(f"ERROR: Can't invoke '{model_id}'. Reason: {e}")
        exit(1)

    model_response = json.loads(response["body"].read())
    response_text = model_response["results"][0]["outputText"]
    print(response_text)
    return {
        "statusCode": 200,
        "answer": response_text
    }


