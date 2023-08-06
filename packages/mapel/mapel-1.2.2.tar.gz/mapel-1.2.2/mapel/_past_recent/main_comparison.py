#!/usr/bin/env python

import mapel
import math


if __name__ == "__main__":

    experiment_id = "comparison/true_spear_10x50"

    # mapel.compute_distances(experiment_id, distance_name='pairwise')
    # mapel.convert_xd_to_2d(experiment_id, distance_name='swap', metric_name='', attraction_factor=1, num_iterations=10000)
    mapel.print_2d(experiment_id, distance_name='spear', metric_name='', attraction_factor=1, saveas="-spear_10x50_a1", mixed=True)
    #mapel.print_3d(experiment_id, distance_name='spear', metric_name='', attraction_factor=2)
