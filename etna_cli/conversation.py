import click
from typing import Tuple

from etna_cli import config


@click.group(name="conversation")
def main():
    """Conversations on intranet."""


def get_likes(likes_data: list) -> Tuple[int, int]:
    true_val, false_val = 0, 0
    for likes in likes_data:
        for i in likes.keys():
            if likes[i] is True:
                true_val += 1
            else:
                false_val += 1
    return true_val, false_val


@main.command('list')
@click.argument("student", type=click.STRING, required=False)
@click.option("-l", "--latest", is_flag=True, default=None,
              help="print only the latest conversation")
@click.option("-c", "--count", default=None,
              help="number of conversations to list")
@click.option("-s", "--start", default=None,
              help="start conversations at")
def grab_conversations(student: str = None, latest: bool = False,
                       start: int = None, count: int = None):
    wrapper = config.setup_api()
    user_id = wrapper.get_user_info(student)['id']

    convo_data = wrapper.get_conversations(user_id=user_id,
                                           start=start,
                                           size=count)
    for conv in convo_data['hits']:
        date = conv['created_at'].split('T')[0]
        time = conv['created_at'].split('T')[1].split('+')[0]
        likes, dislikes = get_likes(conv['last_message']['likes'])

        print("==============================")
        print("created on {} at {}".format(date, time))
        print("Wall : {}".format(conv['metas']['wall-name']))
        print("Title : {}".format(conv['title']))
        print(conv['last_message']['content'])
        print("views : {}".format(len(conv['last_message']['views'])))
        print("likes : {}   dislikes : {}".format(likes, dislikes))

        if latest is True:
            return
