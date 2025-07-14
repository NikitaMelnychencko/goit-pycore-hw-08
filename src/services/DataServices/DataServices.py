from pathlib import Path
import pickle

class DataServices:
    def __init__(self):
        self.name = "contacts.pkl"
        self.path = Path("./data/" + self.name)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def get_init_data(self):
        if not self.path.exists():
            return {}
        try:
            with open(self.path, "rb") as file:
                return pickle.load(file)
        except (pickle.UnpicklingError, EOFError, FileNotFoundError):
            return {}

    def save_data(self, data):
        with open(self.path, "wb") as file:
            pickle.dump(data, file)
