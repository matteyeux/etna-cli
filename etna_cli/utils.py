""" Few utilities functions."""
from tabulate import tabulate


def prettify_lists(current_list: list) -> list:
    """Set black background 1/2 times."""
    cnt = 0
    new_lists = []
    for line in current_list:
        row_cnt = 0
        new_list = []
        for row in line:
            if (cnt % 2) != 0:
                new_list.append(f'\x1b[40m{row}')
            else:
                new_list.append(f'{row}')
            row_cnt += 1
        cnt += 1
        new_list[-1] = f"{row}\x1b[0m"
        new_lists.append(new_list)
    return new_lists


def print_table(final_list: list, header: tuple,
                fmt: str = 'simple', prettify: bool = True):
    if prettify:
        pretty_list = prettify_lists(final_list)
    else:
        pretty_list = final_list
    print(tabulate(pretty_list, headers=header, tablefmt=fmt))
