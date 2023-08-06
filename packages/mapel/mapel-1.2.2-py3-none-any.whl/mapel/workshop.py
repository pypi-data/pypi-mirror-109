#!/usr/bin/env python

import mapel
from voting import development as dev
from voting import objects as obj
import numpy as np


if __name__ == "__main__":
    m=10
    my_range = [i for i in range(m)]
    print(my_range)
    reversed_range = [i for i in range(m)]
    reversed_range.reverse()
    print(reversed_range)

    # experiment_id = "_tests/group_separable_2"
    #
    # model = obj.Model_xd(experiment_id)
    #
    # print(model.elections[485].votes_to_positionwise_vectors())





