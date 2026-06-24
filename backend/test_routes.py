import sys
import os

# Add backend directory to path
sys.path.insert(0, os.path.abspath('.'))

from app import create_app

app = create_app("development")

print("--- REGISTERED ADMIN ROUTES ---")
for rule in app.url_map.iter_rules():
    if "admin" in rule.rule:
        print(rule.rule)
print("-------------------------------")
