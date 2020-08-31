import sqlite3
if __name__ != "__main__":
    from .views import app


class IndexItem:
    def __init__(self, item_label: str, item_id: int = None):
        self.item_label: str = item_label.lower()
        self.item_id: int = item_id


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


# class Command:
#     def __init__(self, index_item: IndexItem,
#                  command: str = None,
#                  description: str = None,
#                  syntax: str = None,
#                  lang: str = 'py',
#                  command_id: int = None):
#         self.index_item: IndexItem = index_item
#         self.command = command
#         self.description = description
#         self.syntax = syntax
#         self.lang = lang
#         self.command_id = command_id


# class CommandExample:
#     def __init__(self, command: Command, example: Example):
#         self.command: Command = command
#         self.example: Example = example

# class Command(IndexItem):
#     def __init__(self, item_label: str,
#                  command: str = None,
#                  description: str = None,
#                  syntax: str = None,
#                  lang: str = 'py',
#                  command_id: int = None,
#                  item_id: int = None):
#         super().__init__(item_label, item_id)
#         self.command = command
#         self.description = description
#         self.syntax = syntax
#         self.lang = lang
#         self.command_id = command_id
#
#
# class Link(Command):
#     def __init__(self, item_label: str,
#                  command: str = None,
#                  description: str = None,
#                  syntax: str = None,
#                  lang: str = 'py',
#                  command_id: int = None,
#                  item_id: int = None,
#                  link_label: str = None,
#                  href: str = None,
#                  type: str = 'code',
#                  link_id: int = None):
#         super().__init__(item_label, command, description, syntax, lang, item_id)
#         self.link_label: str = link_label
#         self.href: str = href
#         self.type: str = type
#         self.link_id: int = link_id
#         self.command_id: int = command_id
#
#
# class Example:
#     def __init__(self, item_label: str,
#                  command: str = None,
#                  description: str = None,
#                  syntax: str = None,
#                  lang: str = 'py',
#                  item_id: int = None,
#                  caption: str = None,
#                  content: str = None,
#                  example_id: int = None,
#                  command_id: int = None):
#         super().__init__(item_label, command, description, syntax, lang, item_id)
#         self.caption: str = caption
#         self.content: str = content
#         self.example_id: int = example_id
#         self.command_id: int = command_id






# class IndexItem:
#
#     def __init__(self, label: str, id: int = None):
#         # Check if all arguments are right
#         if not isinstance(label, str):
#             raise TypeError(f"'label' should be a 'str', not {type(label)!r}.")
#
#         if (not isinstance(id, int)) and (id is not None):
#             raise TypeError(f"'id' should be an 'int' or 'None', not {type(id)!r}.")
#
#         # Do assignments
#         self.label: str = label
#         self.lower_label: str = label.lower()
#         self.filename: str = f"{label.lower()}.html"
#         self.id = id
#
#     def __str__(self):
#         return f"{self.__dict__}"
#
#     def __repr__(self):
#         return f"<IndexItem {self.id!r}>"


# class Reminder:
#     def __init__(self, label: str = None,
#                  h1: str = None,
#                  content_cell_1: str = None,
#                  content_cell_2: str = None,
#                  lang: str = None,
#                  syntax_content: str = None,
#                  example_content: str = None,
#                  example_caption: str = None,
#                  link_text: str = None,
#                  link_href: str = None,
#                  link_type: str = None,
#                  id: int = None):
#         self.label: str = label.lower()
#         self.h1: str = h1
#         self.content_cell_1: str = content_cell_1
#         self.content_cell_2: str = content_cell_2
#         self.lang: str = "py" if lang is (None or "") else lang
#         self.syntax_content: str = syntax_content
#         self.example_content: str = example_content
#         self.example_caption: str = example_caption
#         self.link_text: str = link_text
#         self.link_href: str = link_href
#         self.link_type: str = "code" if link_type is (None or "") else link_type
#         self.id: int = id
#
#     def __str__(self):
#         return f"{self.__dict__}"


if __name__ == "__main__":
    ii = IndexItem('pandas', 1)
    print(ii)
    command1 = Command(ii, command='pandas.DataFrame',
                       description='Create a DataFrame',
                       syntax='pandas.DataFrame(data)',
                       command_id=1, h1='pandas.DataFrame')
    print(command1)

    example1 = Example(caption='Example 1', content=">>> print('Hello World!')", example_id=1)
    example2 = Example(caption='Example 2', content=">>> df = pd.DataFrame()", example_id=2)

    command1.examples = [example1, example2]

    # item1 = IndexItem('pandas')
    # print(item1)
