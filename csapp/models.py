import sqlite3
if __name__ != "__main__":
    from .views import app


class IndexItem:

    def __init__(self, label: str, id: int = None):
        # Check if all arguments are right
        if not isinstance(label, str):
            raise TypeError(f"'label' should be a 'str', not {type(label)!r}.")

        if (not isinstance(id, int)) and (id is not None):
            raise TypeError(f"'id' should be an 'int' or 'None', not {type(id)!r}.")
        
        # Do assignments
        self.label: str = label
        self.lower_label: str = label.lower()
        self.filename: str = f"{label.lower()}.html"
        self.id = id
    
    def __str__(self):
        return f"{self.__dict__}"
    
    def __repr__(self):
        return f"<IndexItem {self.id!r}>"


class Reminder:
    def __init__(self, label: str = None, h1: str = None, content_cell_1: str = None, content_cell_2: str = None, id: int = None):
        self.label: str = label.lower()
        self.h1: str = h1
        self.content_cell_1: str = content_cell_1
        self.content_cell_2: str = content_cell_2
        self.id = id

    def __str__(self):
        return f"{self.__dict__}"


if __name__ == "__main__":
    item1 = IndexItem('pandas')
    print(item1)