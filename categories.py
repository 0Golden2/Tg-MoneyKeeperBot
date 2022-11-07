from typing import NamedTuple


class Category(NamedTuple):
    id: int or None
    name: str or None
    aliases: list or None


Categories_new = []

with open("category_list.txt", encoding='utf-8') as f:
    for line in f:
        id = int(line.split('. ')[0])
        name = line.split('. ')[1]
        aliases = line.split('. ')[2].split()
        Categories_new.append(Category(id=id, name=name, aliases=aliases))


def show_categ_list():
    with open("category_list.txt", encoding='utf-8') as f:
        return [l.split('. ')[1] for l in f]



