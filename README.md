# S2 Shared Context Chat

Multiple chat interfaces sharing context via s2 streams and OpenAI Responses API convos.

## Setup

1. Create a basin at [s2.dev/dashboard](https://s2.dev/dashboard) and get your access token

2. Configure environment:
```bash
uv sync
cp env-template .env
# Edit .env with your credentials
```

## Run Multiple Shared Chats

Terminal 1:
```bash
uv run --env-file .env main.py
```

Terminal 2:
```bash
uv run --env-file .env main.py
```

Terminal 3:
```bash
uv run --env-file .env main.py
```

All sessions share conversation history via the same s2 stream.

