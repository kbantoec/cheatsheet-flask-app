import sqlite3
if __name__ != "__main__":
    from .views import app


class IndexItem:
    def __init__(self, item_label: str, item_id: int = None):
        self.item_label: str = item_label.lower()
        self.item_id: int = item_id

    def __repr__(self):
        return f"<csapp.models.IndexItem object {{item_label: {self.item_label}, item_id: {self.item_id}}}>"


class Example:
    def __init__(self, example_caption: str = None,
                 example_content: str = None,
                 example_id: int = None):
        self.example_caption: str = example_caption
        self.example_content: str = example_content
        self.example_id: int = example_id


class Link:
    def __init__(self, link_label: str = None,
                 link_href: str = None,
                 link_type: str = None,
                 link_id: int = None):
        self.link_label: str = link_label
        self.link_href: str = link_href
        self.link_type: str = link_type
        self.link_id: int = link_id


class Command:
    """
    A command necessarily corresponds to an index item object and can have many examples and/or links.
    """
    def __init__(self, item_label: str,
                 item_id: int = None,
                 index_item: IndexItem = None,
                 command: str = None,
                 description: str = None,
                 syntax: str = None,
                 lang: str = 'py',
                 h1: str = None,
                 command_id: int = None,
                 examples: list = None,
                 links: list = None):
        self.index_item: IndexItem = IndexItem(item_label, item_id=item_id) if index_item is None else index_item
        self.command = command
        self.description = description
        self.syntax = syntax
        self.lang = 'py' if lang is (None or '') else lang
        self.h1 = h1
        self.command_id = command_id
        self.examples: list = list() if examples is None else examples
        self.links: list = list() if links is None else links


if __name__ == "__main__":
    ii = IndexItem('pandas', 1)
    print(ii)
    command1 = Command(ii, command='pandas.DataFrame',
                       description='Create a DataFrame',
                       syntax='pandas.DataFrame(data)',
                       command_id=1, h1='pandas.DataFrame')
    print(command1)

    example1 = Example(example_caption='Example 1', example_content=">>> print('Hello World!')", example_id=1)
    example2 = Example(example_caption='Example 2', example_content=">>> df = pd.DataFrame()", example_id=2)

    command1.examples = [example1, example2]
