#!/bin/bash

if [ -z "$ANTHROPIC_API_KEY" ]; then
  echo "❌ ANTHROPIC_API_KEY is missing"
  exit 1
fi

if [ -z "$ANTHROPIC_API_BASE" ]; then
  echo "⚠️ ANTHROPIC_API_BASE not set (using default)"
fi

echo "✅ LLM environment OK"
