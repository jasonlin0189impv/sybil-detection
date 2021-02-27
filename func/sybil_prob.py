import numpy as np


def cal_sybil_prob(request_graph, confidence_prior):
    """calculate sybil probability

    Args:
        node (str): observe node name
        request_graph (nx.graph): request graph, with
            node: {label: str,
                   sybil_accept_prob: float,
                   real_accept_prob: float,
                   sybil_request_prob: float,
                   real_request_prob: float},
            edge: {accept: int}
            *source -- request (accept) --> target
        confidence_prior (dict): with info
            {
                node: {
                    pi (float), # prior assumption of users (between 0 to 1)
                    sigma (float), # prior request assumption of users (from zero to infinity)
                    phi (float), # prior acceptance assumption of users (from zero to infinity)
                }
            }
    Return:
        sybil prob dict
    """
    sybil_dict = {}
    for node in request_graph.nodes():
        reqs_edges = [edge for edge in request_graph.out_edges(node)]
        s_acpt, r_acpt, s_reqs, r_reqs = _target_relative_prob(
            reqs_edges, request_graph
        )
        fake_part = float(
            confidence_prior[node]['pi'] * np.prod(s_acpt) * np.prod(s_reqs)
        )
        real_part = float(
            (1 - confidence_prior[node]['pi'])
            * np.prod(r_acpt)
            * np.prod(r_reqs)
        )
        sybil_prob = (
            fake_part / (fake_part + real_part)
            if (fake_part + real_part) != 0
            else 0
        )
        sybil_dict[node] = sybil_prob
    return sybil_dict


def _target_relative_prob(reqs_edges, request_graph):
    accept_s = []
    accept_r = []
    request_s = []
    request_r = []
    for reqs_edge in reqs_edges:
        # accept
        s_acpt_prob = request_graph.nodes[reqs_edge[1]]['sybil_accept_prob']
        r_acpt_prob = request_graph.nodes[reqs_edge[1]]['real_accept_prob']
        if request_graph.edges[reqs_edge]['accept'] == 1:
            accept_s.append(s_acpt_prob)
            accept_r.append(r_acpt_prob)
        else:
            accept_s.append(1 - s_acpt_prob)
            accept_r.append(1 - r_acpt_prob)
        # request
        s_reqs_prob = request_graph.nodes[reqs_edge[1]]['sybil_request_prob']
        r_reqs_prob = request_graph.nodes[reqs_edge[1]]['real_request_prob']
        request_s.append(s_reqs_prob)
        request_r.append(r_reqs_prob)
    return accept_s, accept_r, request_s, request_r
