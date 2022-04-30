"""
A flashcards PowerPoint builder
"""

import professor.room as rm

# from knowyourprofessor import tag_iterator
# from professor import Professor

# import knowyourprofessor
# from knowyourprofessor import *
# from room import RoomOld
# from professor import Professor

# RELIGION_DIR_URL = 'https://religion.byu.edu/directory'

# def get_items(funcs: iter):
#     return [tuple(call_each(funcs, tag)) for tag in tag_iterator3()]

from professor import Professor

if __name__ == "__main__":
    all_profs = Professor.from_website()
    Professor.download_all_photos(all_profs, 'pics')

    # print(rm.Room('JSB', '3', '125', 'H'))
    pass
    # items = '\n'.join('###'.join((str(y) for y in x)) for x in get_items((process_first_name, process_last_name,
    #                                                                       process_job_title, process_room)))
    # print(items)

    # b = RoomOld('JSB', '3', '364')
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
