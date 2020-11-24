import click
from etna_cli import config
from etna_cli.utils import print_table


def roundify(average: str = None) -> float:
    if average is None:
        return None
    else:
        return round(float(average), 2)


@click.group(name="student")
def main():
    """Student stuff."""


@main.command()
@click.argument("student", type=click.STRING, required=False)
def info(student: str = None):
    """Get student's info."""
    wrapper = config.setup_api()
    user_data = wrapper.get_user_info(student)

    if "not found" in user_data:
        print("user not found")
        return

    for i in user_data.keys():
        # older users have roles instead of groups
        if i in ("roles", "groups"):
            print("groups : ", end="")
            [print(group, end=" ") for group in user_data[i]]
            print(end="\n")
        else:
            print("{} : {}".format(i, user_data[i]))


@main.command()
@click.argument("student", type=click.STRING, required=False)
@click.option("-p", "--promo", help="specify student's promotion")
@click.option("-a", "--activity", help="marks for a specific activity")
def grades(student: str = None, promo: int = None, activity: str = None):
    """Get student's grades."""
    wrapper = config.setup_api()
    if promo is None:
        promo = wrapper.get_user_promotion(student)[0]['id']
    grades_data = wrapper.get_grades(login=student, promotion_id=promo)
    header = ('activity', 'type', "UV name", 'mark', 'average', 'max', 'min')
    final_list = []

    for mark in grades_data:
        mark_list = []
        mark_list.append(mark['activity_name'])
        mark_list.append(mark['activity_type'])
        mark_list.append(mark['uv_name'])
        mark_list.append(mark['student_mark'])
        mark_list.append(roundify(mark['average']))
        mark_list.append(mark['maximal'])
        mark_list.append(mark['minimal'])
        final_list.append(mark_list)

    print_table(final_list, header)


@main.command()
@click.argument("student", type=click.STRING, required=False)
def promo(student: str = None):
    """Get student's promotions."""
    wrapper = config.setup_api()
    promo_data = wrapper.get_user_promotion(student)
    header = ('ID', 'promotion', 'name', 'start', 'end', 'spe')
    final_list = []
    for i, _ in enumerate(promo_data):
        promo_list = []
        promo_list.append(promo_data[i]['id'])
        promo_list.append(promo_data[i]['promo'])
        promo_list.append(promo_data[i]['wall_name'])
        promo_list.append(promo_data[i]['learning_start'])
        promo_list.append(promo_data[i]['learning_end'])
        promo_list.append(promo_data[i]['spe'])
        final_list.append(promo_list)

    print_table(final_list, header)
