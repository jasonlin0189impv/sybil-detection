'''Transform dataframe to graph'''

import pandas as pd
import networkx as nx


def data2graph(df):
    """Transform dataframe to graph

    Args:
        df (dataframe): (spark) dataframe, with columns {source, target, (edge_attr)}

    Return:
        A networkx directed graph (make sure users' acceptance and request) 
    """
    if len(df.columns) > 2:
        graph = nx.from_pandas_edgelist(
            df,
            source='source',
            target='target',
            edge_attr=df.columns[2],
            create_using=nx.DiGraph(),
        )
    else:
        graph = nx.from_pandas_edgelist(
            df, source='source', target='target', create_using=nx.DiGraph()
        )

    return graph


def add_node_attrs(graph, node_attr_df):
    """Add node attributes

    Args:
        graph (nx.graph): graph info
        node_attr_df (dataframe): node attributes datafame, with columns {node, attr1, attr2, ...}

    Return:
        A networkx graph
    """
    attrs = list(node_attr_df.columns)
    attrs.remove('node')
    for attr in attrs:
        nx.set_node_attributes(
            graph,
            pd.Series(
                node_attr_df[attr].values, index=node_attr_df['node']
            ).to_dict(),
            attr,
        )

    return graph
