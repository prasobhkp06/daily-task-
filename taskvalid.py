import requests
from pydantic import BaseModel
from typing import Optional
import json

class TaskModel(BaseModel):
    title: str
    priority: str = "low"
    completed: bool = False

def create_task(data: dict):
    try:
        return TaskModel(**data)
    except Exception as e:
        print(f"Error: {e.errors()[0]['msg']}")
        return None

def tasks_to_json(tasks):
    return json.dumps([t.model_dump() for t in tasks], indent=2)

# Create tasks
tasks = []
tasks.append(create_task({"title": "Buy milk", "priority": "high"}))
tasks.append(create_task({"title": "Read book"}))
tasks.append(create_task({"priority": "high"}))

tasks = [t for t in tasks if t]  # remove failed ones

# Fetch from API
response = requests.get("https://jsonplaceholder.typicode.com/todos/1")
data = response.json()
api_task = create_task({"title": data["title"], "completed": data["completed"]})
if api_task:
    tasks.append(api_task)

print(tasks_to_json(tasks))