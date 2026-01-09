#!/bin/bash
export OPENAI_API_KEY="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"
cd "$(dirname "$0")"
python3 -m uvicorn agent:app --host 0.0.0.0 --port 8000 --reload
