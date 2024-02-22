from __future__ import annotations
from typing import Callable


class MenuItem:
    def __init__(self, item: tuple):
        self.__index = item[0].replace(' ', '')
        self.__path: list[str] = self.__index.split('.')
        self.__parent: MenuItem | None = None
        self.__name: str = item[1].strip()
        self.__command: Callable | None = item[2]
        self.__items: list[MenuItem] = []

    def get_index(self):
        return self.__index

    def parent_index(self) -> str:
        return '.'.join(self.__path[:-1])

    def set_parent(self, item: MenuItem):
        self.__parent = item

    def get_items(self) -> list[MenuItem]:
        return self.__items

    def add_item(self, item: MenuItem):
        self.__items.append(item)

    def eq_text(self, text: str):
        return self.__path[-1] == text

    def is_command(self):
        return self.__command is not None

    def title(self):
        return self.__name

    def full_title(self):
        i = self
        result = f'{i.title()}'
        while i.__parent:
            i = i.__parent
            result = f'{i.title()} \\ {result}'
        return result

    def do(self):
        if callable(self.__command):
            self.__command()

    def __repr__(self):
        return f'{self.__index} - {self.__name}'

    def __str__(self):
        return f'{self.__path[-1]} : {self.__name}{" ..." if self.__items else ""}'

    def __eq__(self, other):
        if not isinstance(other, MenuItem):
            raise TypeError(f"{other} is not MenuItem type")
        return self.__index == other.__index


def create_menu(description: list, title: str) -> MenuItem:
    root_menu = MenuItem(('', title, None))
    list_items = []
    s_description = sorted(description, key=lambda i: i[0])
    for item in s_description:
        new_menu = MenuItem(item)
        if new_menu in list_items:
            continue
        list_items.append(new_menu)

        parent = root_menu
        for i in list_items:
            if i.get_index() == new_menu.parent_index():
                parent = i
                break
        new_menu.set_parent(parent)
        parent.add_item(new_menu)
    return root_menu


def run_menu(menu: MenuItem):
    while True:
        print()
        print(f'{menu.full_title()}:')
        for item in menu.get_items():
            print(item)
        sel = input('Выбор: ')
        for item in menu.get_items():
            if not item.eq_text(sel):
                continue
            if item.is_command():
                # Команда не пуста - выполняем
                print()
                item.do()
            else:
                # Команда пуста, значит если есть дети, то это подменю
                # а если детей нет то возврат наверх
                if len(item.get_items()):
                    run_menu(item)
                else:
                    return

