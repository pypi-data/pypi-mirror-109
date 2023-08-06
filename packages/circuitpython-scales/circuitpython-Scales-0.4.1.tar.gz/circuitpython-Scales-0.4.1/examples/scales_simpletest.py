# SPDX-FileCopyrightText: Copyright (c) 2021 Jose David M.
#
# SPDX-License-Identifier: Unlicense
#############################
"""
This is a basic demonstration of a Scale Class.
"""

import board
from scales import Scale

display = board.DISPLAY

my_scale = Scale(
    x=50,
    y=220,
    length=200,
    direction="vertical",
    divisions=5,
    limits=(0, 80),
)


display.show(my_scale)


while True:
    pass
