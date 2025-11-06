#!/bin/bash
exec uvicorn app.main:create_app --factory --host 127.0.0.1 --port 5000

