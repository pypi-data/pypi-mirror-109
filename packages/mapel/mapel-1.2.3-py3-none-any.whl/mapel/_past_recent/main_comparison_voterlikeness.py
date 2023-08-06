#!/usr/bin/env python

import mapel
import math

if __name__ == "__main__":

    experiment_id = "comparison/l1-voterlikeness"
    # mapel.prepare_elections(experiment_id, starting_from=288)
    # mapel.compute_distances(experiment_id, distance_name='voterlikeness', metric_name='l1', num_threads=1,
    #                          testing=False, starting_from=288)

    # mapel.convert_xd_to_2d(experiment_id, distance_name='voterlikeness', metric_name='l1', attraction_factor=1,
    #                         num_iterations=10000)
    mapel.print_2d(experiment_id, distance_name='voterlikeness', metric_name='l1', attraction_factor=1, mixed=True,
                   saveas=experiment_id, angle=0.3*math.pi)
