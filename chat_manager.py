from collections import deque
from prompt_templates import templates

class ChatSession:
    def __init__(self, max_messages=10, template="default"):
        self.history = deque(maxlen=max_messages)
        self.set_prompt_template(template)

    def set_prompt_template(self, template_name):
        system_prompt = templates.get(template_name, templates["default"])
        self.history.clear()
        self.history.append({
            "role": "system",
            "content": system_prompt
        })

    def load_history(self, history_list):
        self.history.clear()
        for msg in history_list:
            self.history.append(msg)

    def export_history(self):
        return list(self.history)
    
    def add_user_message(self, content):
        self.history.append({"role": "user", "content": content})
    
    def add_assistant_message(self, content):
        self.history.append({"role": "assistant", "content": content})
    
    def get_history(self):
        return list(self.history)