# S2 Shared Context Chat

Multiple chat interfaces sharing context via s2 streams and OpenAI API.

## Setup

1. Create a basin at [s2.dev/dashboard](https://s2.dev/dashboard) and get your access token

2. Configure environment:
```bash
uv sync
cp env-template .env
# Edit .env with your credentials
```

## Text-based Chat (Chat Completions API)

Run multiple terminals sharing conversation history:

Terminal 1:
```bash
uv run --env-file .env main.py
```

Terminal 2:
```bash
uv run --env-file .env main.py
```

All sessions share conversation history via the same s2 stream.

## Voice/Realtime Agents (Realtime API)

Run multiple developers debugging together with shared context:

Terminal 1:
```bash
uv run --env-file .env voice_main.py
```

Terminal 2:
```bash
uv run --env-file .env voice_main.py
```

The Realtime API implementation:
- Stores complete conversation items (not just messages) in S2
- Supports multi-modal interactions (currently configured for text, extensible to audio)
- Multiple users share full conversation context via S2 streams
- Uses `gpt-realtime-mini` by default (cost-effective)
- Set `REALTIME_MODEL=gpt-realtime` in `.env` for the most advanced model

