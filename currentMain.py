"""
A flashcards PowerPoint builder
"""

from knowyourprofessor import tag_iterator4
from professor import Professor

# import knowyourprofessor
# from knowyourprofessor import *
# from room import Room
# from professor import Professor

RELIGION_DIR_URL = 'https://religion.byu.edu/directory'

# def get_items(funcs: iter):
#     return [tuple(call_each(funcs, tag)) for tag in tag_iterator3()]


if __name__ == "__main__":
    all_profs = [Professor.from_html_tag(tag) for tag in tag_iterator4(RELIGION_DIR_URL)]
    a = '\n'.join(tuple(str(x) for x in all_profs))
    print(a)
    Professor.to_csv('testing.csv', all_profs)

    csv = Professor.from_csv('testing.csv')
    b = '\n'.join(tuple(str(x) for x in csv))
    print(b)
    print(a == b)

    # items = '\n'.join('###'.join((str(y) for y in x)) for x in get_items((process_first_name, process_last_name,
    #                                                                       process_job_title, process_room)))
    # print(items)

    # b = Room('JSB', '3', '364')
    # print(b)
    #
    # c = Professor("John Doe", b)
    # print(c)
    #
    # a = create_professor2(RELED_DIR_URL)
    # print(next(a))
    #
    # d = professor_iterator(RELED_DIR_URL)
    # print(next(d))
