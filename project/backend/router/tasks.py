from fastapi import APIRouter, HTTPException, Query, status
from database import conn, cursor, row_to_dict
from schemas import TaskCreate, TaskUpdate, TaskComplete

router = APIRouter(prefix="/tasks", tags=["Tasks"])

VALID_PRIORITIES = {"Low", "Medium", "High"}


def validate_priority(priority: str) -> None:
    if priority not in VALID_PRIORITIES:
        raise HTTPException(status_code=400, detail="Priority must be Low, Medium, or High")


def get_task_or_404(task_id: int):
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    task = cursor.fetchone()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.get("/")
def get_tasks(
    username: str | None = None,
    status_filter: str | None = Query(default=None, alias="status"),
    priority: str | None = None,
    search: str | None = None,
):
    query = "SELECT * FROM tasks WHERE 1=1"
    params = []

    if username:
        query += " AND username = ?"
        params.append(username)

    if status_filter:
        if status_filter.lower() == "completed":
            query += " AND completed = 1"
        elif status_filter.lower() == "pending":
            query += " AND completed = 0"
        else:
            raise HTTPException(status_code=400, detail="Status must be pending or completed")

    if priority:
        validate_priority(priority)
        query += " AND priority = ?"
        params.append(priority)

    if search:
        query += " AND (title LIKE ? OR description LIKE ? OR category LIKE ?)"
        keyword = f"%{search}%"
        params.extend([keyword, keyword, keyword])

    query += " ORDER BY completed ASC, due_date ASC, id DESC"
    cursor.execute(query, params)
    return [row_to_dict(row) for row in cursor.fetchall()]


@router.get("/summary")
def task_summary(username: str | None = None):
    query = "SELECT * FROM tasks"
    params = []
    if username:
        query += " WHERE username = ?"
        params.append(username)

    cursor.execute(query, params)
    tasks = [row_to_dict(row) for row in cursor.fetchall()]
    total = len(tasks)
    completed = len([task for task in tasks if task["completed"]])
    pending = total - completed
    high_priority = len([task for task in tasks if task["priority"] == "High"])

    return {
        "total": total,
        "completed": completed,
        "pending": pending,
        "high_priority": high_priority,
        "progress": round((completed / total) * 100, 2) if total else 0,
    }


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreate):
    validate_priority(task.priority)
    cursor.execute("SELECT * FROM users WHERE username = ?", (task.username,))
    if not cursor.fetchone():
        raise HTTPException(status_code=404, detail="User not found. Please register first")

    cursor.execute(
        """
        INSERT INTO tasks (username, title, description, priority, due_date, completed, category)
        VALUES (?, ?, ?, ?, ?, 0, ?)
        """,
        (task.username, task.title, task.description, task.priority, task.due_date, task.category),
    )
    conn.commit()
    task_id = cursor.lastrowid
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    return {"message": "Task created successfully", "task": row_to_dict(cursor.fetchone())}


@router.get("/{task_id}")
def get_task(task_id: int):
    return row_to_dict(get_task_or_404(task_id))


@router.put("/{task_id}")
def update_task(task_id: int, updated_task: TaskUpdate):
    validate_priority(updated_task.priority)
    get_task_or_404(task_id)
    cursor.execute(
        """
        UPDATE tasks
        SET title = ?, description = ?, priority = ?, due_date = ?, completed = ?, category = ?
        WHERE id = ?
        """,
        (
            updated_task.title,
            updated_task.description,
            updated_task.priority,
            updated_task.due_date,
            int(updated_task.completed),
            updated_task.category,
            task_id,
        ),
    )
    conn.commit()
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    return {"message": "Task updated successfully", "task": row_to_dict(cursor.fetchone())}


@router.patch("/{task_id}/complete")
def complete_task(task_id: int, data: TaskComplete = TaskComplete()):
    get_task_or_404(task_id)
    cursor.execute("UPDATE tasks SET completed = ? WHERE id = ?", (int(data.completed), task_id))
    conn.commit()
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    return {"message": "Task status updated", "task": row_to_dict(cursor.fetchone())}


@router.delete("/{task_id}")
def delete_task(task_id: int):
    get_task_or_404(task_id)
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    return {"message": "Task deleted successfully"}
