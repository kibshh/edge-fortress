import os 
import sys

# Add the backend root directory to sys.path so "app" can be imported.
# backend/
#   app/
#     __init__.py
#     main.py
#   tests/
#     test_health.py
backend_root = os.path.dirname(os.path.abspath(__file__))  # .../backend/tests
backend_root = os.path.dirname(backend_root)               # .../backend

if backend_root not in sys.path:
    sys.path.insert(0, backend_root)
