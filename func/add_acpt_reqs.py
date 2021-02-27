"""
1. Add request and acceptance info to each node.
(The acceptance rate of user j and receive request rate of user j)
2. assume label users follow others, unlabel users follow by themsleves

## How about misappropriation？
"""


def add_request_info(request_graph, confidence_prior):
    """Add request info to request_graph

    Args:
        request_graph (nx.graph): request graph, with 
            node: {label: str},
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
        A networkx graph
    """
    for node, label in request_graph.nodes.data('label'):
        if label != 'None':
            reqs_cnt = _request_count(node, request_graph, 'None')  # rho_j
            reqs_all_cnt = _request_count(None, request_graph, 'None')  # rho_L
            sybil_reqs_cnt = _request_count(
                node, request_graph, 'fake'
            )  # rho^S_j
            sybil_reqs_all_cnt = _request_count(
                None, request_graph, 'fake'
            )  # rho_{L^S}
            real_reqs_cnt = _request_count(
                node, request_graph, 'real'
            )  # rho^B_j
            real_reqs_all_cnt = _request_count(
                None, request_graph, 'real'
            )  # rho_{L^B}
            sigma = confidence_prior[node]['sigma']
            s_reqs_prob = fake_request_prob(
                sybil_reqs_cnt,
                sybil_reqs_all_cnt,
                reqs_cnt,
                reqs_all_cnt,
                sigma,
            )
            r_reqs_prob = fake_request_prob(
                real_reqs_cnt, real_reqs_all_cnt, reqs_cnt, reqs_all_cnt, sigma
            )
            request_graph.nodes[node]['sybil_request_prob'] = s_reqs_prob
            request_graph.nodes[node]['real_request_prob'] = r_reqs_prob
        else:
            # need to check
            request_graph.nodes[node]['sybil_request_prob'] = (
                sybil_reqs_cnt / sybil_reqs_all_cnt
            )
            request_graph.nodes[node]['real_request_prob'] = (
                real_reqs_cnt / real_reqs_all_cnt
            )
    return request_graph


def add_accept_info(request_graph, confidence_prior):
    """Add acceptance info to request_graph

    Args:
        request_graph (nx.graph): request graph, with 
            node: {label: str},
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
        A networkx graph
    """
    for node, label in request_graph.nodes.data('label'):
        if label != 'None':
            acpt_cnt = _accept_count(node, request_graph, 'None')  # f_j
            reqs_cnt = _request_count(node, request_graph, 'None')  # rho_j
            sybil_acpt_cnt = _accept_count(
                node, request_graph, 'fake'
            )  # f^S_j
            sybil_reqs_cnt = _request_count(
                node, request_graph, 'fake'
            )  # rho^S_j
            real_acpt_cnt = _accept_count(node, request_graph, 'real')  # f_B_j
            real_reqs_cnt = _request_count(
                node, request_graph, 'real'
            )  # rho^S_j
            phi = confidence_prior[node]['phi']
            s_acpt_prob = fake_accept_prob(
                sybil_acpt_cnt, sybil_reqs_cnt, acpt_cnt, reqs_cnt, phi
            )
            r_acpt_prob = fake_accept_prob(
                real_acpt_cnt, real_reqs_cnt, acpt_cnt, reqs_cnt, phi
            )
            request_graph.nodes[node]['sybil_accept_prob'] = s_acpt_prob
            request_graph.nodes[node]['real_accept_prob'] = r_acpt_prob
        else:
            # need to check
            request_graph.nodes[node]['sybil_accept_prob'] = (
                sybil_acpt_cnt / sybil_reqs_cnt if sybil_reqs_cnt != 0 else 0
            )
            request_graph.nodes[node]['real_accept_prob'] = (
                real_acpt_cnt / real_reqs_cnt if real_reqs_cnt != 0 else 0
            )
    return request_graph


def _accept_count(node, request_graph, label_status):
    assert label_status in [
        'real',
        'fake',
        'None',
    ], "Label_status only have 'real', 'fake', 'None'!"
    if label_status == 'None':
        acpt_cnt = [
            edge
            for edge in request_graph.in_edges(node)
            if request_graph.edges[edge]['accept'] == 1
        ]
    elif label_status == 'fake':
        acpt_cnt = [
            edge
            for edge in request_graph.in_edges(node)
            if (request_graph.edges[edge]['accept'] == 1)
            and (request_graph.nodes[edge[0]]['label'] == 'fake')
        ]
    else:
        acpt_cnt = [
            edge
            for edge in request_graph.in_edges(node)
            if (request_graph.edges[edge]['accept'] == 1)
            and (request_graph.nodes[edge[0]]['label'] == 'real')
        ]
    return float(len(acpt_cnt))


def _request_count(node, request_graph, label_status):
    """If node is 'None', count all request in the graph"""
    assert label_status in [
        'real',
        'fake',
        'None',
    ], "Label_status only have 'real', 'fake', 'None'!"
    if node is None:
        if label_status == 'None':
            reqs_cnt = [edge for edge in request_graph.in_edges(node)]
        elif label_status == 'fake':
            reqs_cnt = [
                edge
                for edge in request_graph.in_edges(node)
                if (request_graph.nodes[edge[0]]['label'] == 'fake')
            ]
        else:
            reqs_cnt = [
                edge
                for edge in request_graph.in_edges(node)
                if (request_graph.nodes[edge[0]]['label'] == 'real')
            ]
    else:
        if label_status == 'None':
            reqs_cnt = [edge for edge in request_graph.in_edges()]
        elif label_status == 'fake':
            reqs_cnt = [
                edge
                for edge in request_graph.in_edges()
                if (request_graph.nodes[edge[0]]['label'] == 'fake')
            ]
        else:
            reqs_cnt = [
                edge
                for edge in request_graph.in_edges()
                if (request_graph.nodes[edge[0]]['label'] == 'real')
            ]
    return float(len(reqs_cnt))


# calculate acceptance------
def fake_accept_prob(sybil_acpt_cnt, sybil_reqs_cnt, acpt_cnt, reqs_cnt, phi):
    """
    sybil_acpt_cnt: # user j's acceptances of friend requests from users with known 'fake' labels
    sybil_reqs_cnt: # all 'fake' friend requests that known users sent to user j
    acpt_cnt: # user j's accept of friend requests
    reqs_cnt: # user j's friend requests
    phi: confidence prior on user (target) j
    """
    acpt_prob = acpt_cnt / reqs_cnt if reqs_cnt != 0 else 0
    return (sybil_acpt_cnt + phi * acpt_prob) / (sybil_reqs_cnt + phi)


def real_accept_prob(real_acpt_cnt, real_reqs_cnt, acpt_cnt, reqs_cnt, phi):
    """
    real_acpt_cnt: # user j's acceptances of friend requests from users with known 'real' labels
    real_reqs_cnt: # all 'real' friend requests that known users sent to user j
    acpt_cnt: # user j's accept of friend requests
    reqs_cnt: # user j's friend requests
    phi: confidence prior on user (target) j
    """
    acpt_prob = acpt_cnt / reqs_cnt if reqs_cnt != 0 else 0
    return (real_acpt_cnt + phi * acpt_prob) / (real_reqs_cnt + phi)


# --------------------------

# calculate request--------
def fake_request_prob(
    sybil_reqs_cnt, sybil_reqs_all_cnt, reqs_cnt, reqs_all_cnt, sigma
):
    """
    sybil_reqs_cnt: # all 'fake' friend requests that known users sent to user j
    sybil_reqs_all_cnt: # all 'fake' friend requests that sent by known users
    reqs_cnt: # user j's friend requests
    reqs_all_cnt: # all users friend requests
    sigma: confidence prior on target j for the target selection
    """
    reqs_prob = reqs_cnt / reqs_all_cnt  # 可能不是好的算法, 如果網絡太大連線太稀疏, 可能會讓值趨近於 0
    return (sybil_reqs_cnt + sigma * reqs_prob) / (sybil_reqs_all_cnt + sigma)


def real_request_prob(
    real_reqs_cnt, real_reqs_all_cnt, reqs_cnt, reqs_all_cnt, sigma
):
    """
    real_reqs_cnt: # all 'real' friend requests that known users sent to user j
    real_reqs_all_cnt: # all 'real' friend requests that sent by known users
    reqs_cnt: # user j's friend requests
    reqs_all_cnt: # all users friend requests
    sigma: confidence prior on target j for the target selection
    """
    reqs_prob = reqs_cnt / reqs_all_cnt  # 可能不是好的算法, 如果網絡太大連線太稀疏, 可能會讓值趨近於 0
    return (real_reqs_cnt + sigma * reqs_prob) / (real_reqs_all_cnt + sigma)


# ---------------------------
