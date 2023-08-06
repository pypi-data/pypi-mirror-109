#!/usr/bin/env python

import mapel
import math

# from voting import development as dev


if __name__ == "__main__":
    #import sys
    #p#rint(sys.executable)
    #"""
    experiment_id = "_tests/all_election_models"

    mapel.prepare_elections(experiment_id)


    # mapel.prepare_elections(experiment_id)

    # mapel.compute_winners(experiment_id, method='hb', algorithm='exact')
    # mapel.compute_winners(experiment_id, method='hb', algorithm='greedy')
    # tmp.compute_statistics(experiment_id, method='hb', algorithm='greedy')
    # tmp.print_statistics(experiment_id, method='hb', algorithm='greedy')


    # mapel.compute_winners(experiment_id, method='borda', num_winners=1)
    # mapel.compute_winners(experiment_id, method='plurality', num_winners=1)
    #

    # tmp.compute_overlapping_of_winners(experiment_id, num_winners=1)
    # tmp.print_chart_overlapping_of_winners(experiment_id, num_winners=1)

    # mapel.compute_condorcet_existence(experiment_id)
    # dev.print_chart_condorcet_existence(experiment_id)


    # mapel.compute_distances(experiment_id, distance_name='discrete', metric_name='0', num_threads=1, testing=False)

    # mapel.convert_xd_to_2d(experiment_id, distance_name='positionwise', metric_name='emd', attraction_factor=1,
    #                             num_iterations=10000)
    # mapel.print_2d(experiment_id, distance_name='positionwise', metric_name='emd', attraction_factor=1, mixed=True,
    #                   saveas=experiment_id, angle=0.8*math.pi, update=True)


