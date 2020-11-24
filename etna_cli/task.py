import click
from datetime import timedelta, datetime

try:
    from taskw import TaskWarrior
    TASK_INSTALLED = True
except:
    TASK_INSTALLED = False

from etna_cli import config


@click.group(name="task")
def main():
    """Add quests and projects to TaskWarrior."""


def convert_to_unix_tstamp(date: str, simple_quest=False) -> str:
    """
    This function assumes it receives a date like :
    2020-02-07T17:00:00+01:00
    then it returns it as UNIX timestamp
    Also for some reason I can't add timezone
    with strptime that's why I sum 1h to initial date.
    """
    # someone added +02:00 => +01:00
    if simple_quest is False and date[-6:] != "+01:00":
        date = date.replace(date[-6:], "+01:00")

    # check if it is a quest/project without stages
    if simple_quest is False:
        date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S+01:00")
    else:
        date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")

    # add 1h because I couldn't get timezone with strptime
    timestamped_date = datetime.timestamp(date + timedelta(hours=1))
    return str(timestamped_date)


def task_exists(twarrior, task_name: str) -> bool:
    """
    Check if task exists before inserting it
    in Task Warrior.
    """
    tasks = twarrior.load_tasks()
    for key in tasks.keys():
        for task in tasks[key]:
            if task['description'] == task_name:
                return True
    return False


def is_stage_validated(stage: dict) -> bool:
    """
    Check if stage has special validation key
    and is validated.
    """
    for key in stage.keys():
        if key == "validation" and stage['validation']['validation'] == "valid":
            return True
    return False


def add_data_to_taskw(data: dict, module: str, quest: str):
    """
    Insert data to TaskWarrior DB.
    """
    twarrior = TaskWarrior()
    if quest is not None:
        project_data = module + ":" + quest
        timestamp = convert_to_unix_tstamp(data['end'], False)
    else:
        project_data = module
        timestamp = convert_to_unix_tstamp(data['date_end'], True)

    if not task_exists(twarrior, data['name']) and not is_stage_validated(data):
        twarrior.task_add(data['name'], due=timestamp, project=project_data)


@main.command()
def add():
    """
    Add projects and quests to Task Warrior.
    """
    if TASK_INSTALLED is False:
        print("TaskWarrior is not installed.")
        print("Please install it to use this command")
        return

    wrapper = config.setup_api()
    data = wrapper.get_current_activities()

    for module in data.keys():
        for i in range(len(data[module]['project'])):
            print(data[module]['project'][i]['name'], ":", module)
            add_data_to_taskw(data[module]['project'][i], module, None)

        stage_nb = 0
        for i in range(len(data[module]['quest'])):
            for stage in data[module]['quest'][i]['stages']:
                quest = data[module]['quest'][i]['name']
                print("{0} - {1}:{2}".format(module, quest, stage['name']))
                add_data_to_taskw(stage, module, quest)
                stage_nb += 1

            if stage_nb == 0:
                print(data[module]['quest'][i]['name'], module)
                add_data_to_taskw(data[module]['quest'][i], module, None)
