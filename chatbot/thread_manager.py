# chatbot/thread_manager.py
class ThreadManager:
    def __init__(self):
        self.threads = {}

    def get_thread(self, user_id):
        return self.threads.get(user_id)

    def create_thread(self, user_id):
        self.threads[user_id] = UserThread()

    def delete_thread(self, user_id):
        if user_id in self.threads:
            del self.threads[user_id]

class UserThread:
    def __init__(self):
        self.active_llm = 'rag'  # Default LLM

    def set_active_llm(self, llm_type):
        self.active_llm = llm_type

    def get_active_llm(self):
        return self.active_llm

thread_manager = ThreadManager()
