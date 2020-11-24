import click
import operator
from click_default_group import DefaultGroup

from etna_cli import config
from etna_cli.utils import print_table


@click.group(
    name="rank",
    cls=DefaultGroup,
    default="get-student-rank",
    default_if_no_args=True
)
def main():
    """Rank by promotion."""


@main.command()
@click.argument("student", type=click.STRING, required=False)
@click.option("-p", "--promo", help="specify promo ID")
@click.option("-a", "--activity", help="specify activity (eg: Projet DAT)")
def get_student_rank(student: str = None, promo: str = None,
                     activity: str = None):
    """Get student rank."""
    wrapper = config.setup_api()

    if promo is None and student is None:
        student_info = wrapper.get_user_info()
        login = student_info['login']
        promo = wrapper.get_user_promotion(login)[0]['id']
    elif student is not None and promo is None:
        promo = wrapper.get_user_promotion(student)[0]['id']
    elif student is None and promo is not None:
        student_info = wrapper.get_user_info()
        login = student_info['login']
    else:
        return

    promo_list = get_students_by_promo(wrapper, int(promo))
    if promo_list is None:
        return

    student_marks = {}

    for student in promo_list:
        print(f"grabing grades for {student}", end='\r')
        student_grades = wrapper.get_grades(login=student, promotion_id=promo)

        student_marks[student] = 0
        cnt = 0

        for student_grade in student_grades:
            if activity is not None:
                if activity == student_grade['activity_name']:
                    student_marks[student] = student_grade['student_mark']
                    cnt = 1
                    break
            else:
                # Some users have 'Null' instead of a real mark
                if student_grade['student_mark'] is not None:
                    student_marks[student] += int(student_grade['student_mark'])
                    cnt += 1
                else:
                    pass
    sorted_students = sorted(student_marks.items(),
                             key=operator.itemgetter(1),
                             reverse=True)

    header = ('rank', 'student', 'average')
    final_list = []
    for i in range(0, len(sorted_students)):
        student_list = []
        try:
            average = sorted_students[i][1] / cnt
        except ZeroDivisionError:
            average = 0
        student_list.append(i + 1)
        student_list.append(sorted_students[i][0])
        student_list.append(round(average, 2))
        final_list.append(student_list)
    print_table(final_list, header)


def get_students_by_promo(wrapper, promo: int) -> list:
    """Get list of student by promo."""
    student_list = []
    students = wrapper.get_students(promotion_id=promo)

    if "does not exist" in students:
        print("Promo ID does not exist")
        return None

    for student in students['students']:
        student_list.append(student['login'])

    return student_list
