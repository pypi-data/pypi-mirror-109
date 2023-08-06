#!/usr/bin/env python

import mapel

if __name__ == "__main__":

    experiment_id = "subelections/voter_subelection_7x50_final"

    #mapel.prepare_elections(experiment_id)
    #mapel.compute_subelection_weird(experiment_id, distance_name="voter_subelection", num_threads=1, precision=10, metric_name=0)

    mapel.print_matrix(experiment_id, distance_name="voter_subelection", metric_name=0, scale=2,
                        saveas=experiment_id, self_distances=True, yticks='left')



    # mapel.prepare_elections(experiment_id)
    # mapel.compute_subelection_weird(experiment_id, distance_name="voter_subelection", num_threads=4, precision=10, metric_name=0)
    # mapel.compute_subelection_weird(experiment_id, distance_name="voter_subelection", num_threads=4, precision=10, metric_name=1)
    # mapel.compute_subelection_weird(experiment_id, distance_name="voter_subelection", num_threads=4, precision=10, metric_name=2)
    #
    #
    # mapel.print_matrix(experiment_id, distance_name="voter_subelection", metric_name=0, scale=10,
    #                    saveas='t0', self_distances=True)
    # mapel.print_matrix(experiment_id, distance_name="voter_subelection", metric_name=1, scale=10,
    #                    saveas='t1', self_distances=True)
    # mapel.print_matrix(experiment_id, distance_name="voter_subelection", metric_name=2, scale=10,
    #                    saveas='t2', self_distances=True)
