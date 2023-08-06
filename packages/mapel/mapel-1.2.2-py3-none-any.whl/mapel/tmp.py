#!/usr/bin/env python

import mapel
from voting import _tmp
import math

if __name__ == "__main__":


    # experiment_id = "ijcai/original+paths"
    experiment_id = "_tests/mix_mallows_3"

    # mapel.prepare_elections(experiment_id, starting_from=329)
    #
    # mapel.compute_distances(experiment_id, starting_from=329, distance_name='positionwise', metric_name='emd', num_threads=1, testing=True)
    #
    # mapel.convert_xd_to_2d(experiment_id, distance_name='positionwise', metric_name='emd', attraction_factor=2,
    #                         num_iterations=10000)

    mapel.print_2d(experiment_id, distance_name='positionwise', metric_name='emd', attraction_factor=2,
                      saveas=experiment_id, mixed=True)




    # mapel.prepare_elections(experiment_id, starting_from=479)
    #
    # mapel.compute_distances(experiment_id, starting_from=479, distance_name='positionwise', metric_name='emd', num_threads=1, testing=True)

    # mapel.convert_xd_to_2d(experiment_id, distance_name='positionwise', metric_name='emd', attraction_factor=2,
    #                         num_iterations=1000)
    #
    # mapel.print_2d(experiment_id, distance_name='positionwise', metric_name='emd', attraction_factor=2,
    #                   saveas=experiment_id, mixed=True)


    # experiment_id = 'diodi'
    # mapel.create_structure(experiment_id)