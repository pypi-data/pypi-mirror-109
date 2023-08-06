
from .voting import _elections as el
from .voting import embedding as emb
from .voting import metrics as metr
from .voting import print as pr
from .voting import development as dev


def hello():
    print("Hello!")


#########################
### PREPARE ELECTIONS ###
#########################


def prepare_elections(experiment_id, **kwargs):
    el.prepare_elections(experiment_id, **kwargs)


def generate_elections(experiment_id, **kwargs):
    el.generate_elections(experiment_id, **kwargs)


###########################
### COMPUTING DISTANCES ###
###########################


def compute_distances(experiment_id, **kwargs):
    metr.compute_distances(experiment_id, **kwargs)


#################
### EMBEDDING ###
#################


def convert_xd_to_2d(experiment, **kwargs):
    emb.convert_xd_to_2d(experiment, **kwargs)


def convert_xd_to_3d(experiment, **kwargs):
    emb.convert_xd_to_3d(experiment, **kwargs)


def convert_using_tsne(experiment, **kwargs):
    emb.convert_using_tsne(experiment, **kwargs)

def convert_using_mds(experiment, **kwargs):
    emb.convert_using_mds(experiment, **kwargs)


################
### PRINTING ###
################


def print_2d(experiment_id, **kwargs):
    pr.print_2d(experiment_id, **kwargs)


def print_3d(experiment_id, **kwargs):
    pr.print_3d(experiment_id, **kwargs)


def print_matrix(experiment_id, **kwargs):
    pr.print_matrix(experiment_id, **kwargs)


def print_param_vs_distance(experiment_id, **kwargs):
    pr.print_param_vs_distance(experiment_id, **kwargs)



######################
### COMPUTE SCORES ###
######################


def compute_highest_plurality(experiment_id):
    dev.compute_highest_plurality(experiment_id)


def compute_highest_borda(experiment_id):
    dev.compute_highest_borda(experiment_id)


def compute_lowest_dodgson(experiment_id):
    dev.compute_lowest_dodgson(experiment_id)


#########################
### SUBELECTIONS ###
#########################


# def voter_subelection(experiment_id):
#     metr.voter_subelection(experiment_id)


#########################
### DEVELOPMENT ###
#########################


def get_distance(election_1, election_2, **kwargs):
    return metr.get_distance(election_1, election_2, **kwargs)


def import_election(experiment_id, election_id):
    return el.import_election(experiment_id, election_id)


def compute_subelection_weird(experiment_id, **kwargs):
    dev.compute_subelection_weird(experiment_id, **kwargs)


def compute_winners(experiment_id, **kwargs):
    dev.compute_winners(experiment_id, **kwargs)


def compute_effective_num_candidates(experiment_id, **kwargs):
    dev.compute_effective_num_candidates(experiment_id, **kwargs)


def compute_condorcet_existence(experiment_id):
    dev.compute_condorcet_existence(experiment_id)


def create_structure(experiment_id):
    dev.create_structure(experiment_id)