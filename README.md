# openai-api-proxy

This is a proxy for the OpenAI API.

## How to Run

To run this program, you must first install `poetry`:

```
$ pip install poetry
```

Next, install the necessary dependencies:

```
$ poetry shell
$ poetry install
```

Finally, run the program for development:

```
$ poetry run start --reload true
```

To test the program, you can send a request using `curl`:

```
$ curl http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer [OPENAI_API_KEY]" \
  -d '{
    "model": "gpt-3.5-turbo",
    "stream": true,
    "messages": [
      {
        "role": "user",
        "content": "你好"
      }
    ]
  }'

// stream output

data: {"id":"chatcmpl-6ybNRk7dEssqwKBrWKaupEwP1FcmR","object":"chat.completion.chunk","created":1679901377,"model":"gpt-3.5-turbo-0301","choices":[{"delta":{"role":"assistant"},"index":0,"finish_reason":null}]}

data: {"id":"chatcmpl-6ybNRk7dEssqwKBrWKaupEwP1FcmR","object":"chat.completion.chunk","created":1679901377,"model":"gpt-3.5-turbo-0301","choices":[{"delta":{"content":"您"},"index":0,"finish_reason":null}]}

data: {"id":"chatcmpl-6ybNRk7dEssqwKBrWKaupEwP1FcmR","object":"chat.completion.chunk","created":1679901377,"model":"gpt-3.5-turbo-0301","choices":[{"delta":{"content":"好"},"index":0,"finish_reason":null}]}

data: {"id":"chatcmpl-6ybNRk7dEssqwKBrWKaupEwP1FcmR","object":"chat.completion.chunk","created":1679901377,"model":"gpt-3.5-turbo-0301","choices":[{"delta":{"content":"！"},"index":0,"finish_reason":null}]}

data: {"id":"chatcmpl-6ybNRk7dEssqwKBrWKaupEwP1FcmR","object":"chat.completion.chunk","created":1679901377,"model":"gpt-3.5-turbo-0301","choices":[{"delta":{"content":"有"},"index":0,"finish_reason":null}]}

data: {"id":"chatcmpl-6ybNRk7dEssqwKBrWKaupEwP1FcmR","object":"chat.completion.chunk","created":1679901377,"model":"gpt-3.5-turbo-0301","choices":[{"delta":{"content":"什"},"index":0,"finish_reason":null}]}

data: {"id":"chatcmpl-6ybNRk7dEssqwKBrWKaupEwP1FcmR","object":"chat.completion.chunk","created":1679901377,"model":"gpt-3.5-turbo-0301","choices":[{"delta":{"content":"么"},"index":0,"finish_reason":null}]}

data: {"id":"chatcmpl-6ybNRk7dEssqwKBrWKaupEwP1FcmR","object":"chat.completion.chunk","created":1679901377,"model":"gpt-3.5-turbo-0301","choices":[{"delta":{"content":"可以"},"index":0,"finish_reason":null}]}

data: {"id":"chatcmpl-6ybNRk7dEssqwKBrWKaupEwP1FcmR","object":"chat.completion.chunk","created":1679901377,"model":"gpt-3.5-turbo-0301","choices":[{"delta":{"content":"帮"},"index":0,"finish_reason":null}]}

data: {"id":"chatcmpl-6ybNRk7dEssqwKBrWKaupEwP1FcmR","object":"chat.completion.chunk","created":1679901377,"model":"gpt-3.5-turbo-0301","choices":[{"delta":{"content":"助"},"index":0,"finish_reason":null}]}

data: {"id":"chatcmpl-6ybNRk7dEssqwKBrWKaupEwP1FcmR","object":"chat.completion.chunk","created":1679901377,"model":"gpt-3.5-turbo-0301","choices":[{"delta":{"content":"您"},"index":0,"finish_reason":null}]}

data: {"id":"chatcmpl-6ybNRk7dEssqwKBrWKaupEwP1FcmR","object":"chat.completion.chunk","created":1679901377,"model":"gpt-3.5-turbo-0301","choices":[{"delta":{"content":"的"},"index":0,"finish_reason":null}]}

data: {"id":"chatcmpl-6ybNRk7dEssqwKBrWKaupEwP1FcmR","object":"chat.completion.chunk","created":1679901377,"model":"gpt-3.5-turbo-0301","choices":[{"delta":{"content":"吗"},"index":0,"finish_reason":null}]}

data: {"id":"chatcmpl-6ybNRk7dEssqwKBrWKaupEwP1FcmR","object":"chat.completion.chunk","created":1679901377,"model":"gpt-3.5-turbo-0301","choices":[{"delta":{"content":"？"},"index":0,"finish_reason":null}]}

data: {"id":"chatcmpl-6ybNRk7dEssqwKBrWKaupEwP1FcmR","object":"chat.completion.chunk","created":1679901377,"model":"gpt-3.5-turbo-0301","choices":[{"delta":{},"index":0,"finish_reason":"stop"}]}

data: [DONE]
```

Note: Please replace `[OPENAI_API_KEY]` with your actual OpenAI API key.

## Deployment

You can use a Docker image to deploy:

```
$ docker pull ghcr.io/assistantflow/openai-api-proxy:latest
$ docker run -d --name aiproxy ghcr.io/assistantflow/openai-api-proxy:latest sh -c "uvicorn server.main:app --host 0.0.0.0 --port 8080" // default port is 8000, you can change it like this
```
