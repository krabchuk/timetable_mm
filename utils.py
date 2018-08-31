def group_valid(group):
    if 100 < group < 113 or 120 < group < 127 or \
            200 < group < 213 or 220 < group < 227 or \
            300 < group < 313 or 320 < group < 327 or 330 < group < 334 or \
            400 < group < 413 or 420 < group < 427 or 430 < group < 434 or \
            500 < group < 513 or 520 < group < 527 or 530 < group < 534 or \
            600 < group < 613 or 620 < group < 627 or 630 < group < 634:
        return True
    else:
        return False