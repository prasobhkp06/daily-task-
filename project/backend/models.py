class user:
    def __init__(
        self,
        id,
        username,
        email,
        password
    ):
        self.id = id
        self.username = username
        self.email = email
        self.password = password
class task:
    def __init__(
        self,
        id,
        title,
        description,
        priority,
        due_date,
        completed=False,
        user_id=None
    ):
        self.id = id
        self.title = title
        self.description = description
        self.priority = priority
        self.due_date = due_date
        self.completed = completed
        self.user_id = user_id       
