import networkx as nx
import requests

#docstring adapted from ads.Article.build_citation_tree
def build_reference_graph(start_bibcode, token, depth=1, **kwargs):
    """
    Builds a reference tree for a paper with bibcode `start_bibcode`
    :param start_bibcode:
        ADS bibcode of the paper you want the reference tree for.
    :param depth: [optional]
        The number of levels to fetch in the reference tree.
    :type depth:
        int
    :param kwargs: [optional]
        Keyword arguments to pass to ``ads.search``.
    :returns:
        A list of reference to the current article, with pre-loaded
        reference down by ``depth``.
    """
    reference_graph = nx.Graph()
    level = 0
    reference_graph.add_node(start_bibcode)
    bibcodes_to_query = [start_bibcode]
    reference_graph.node[start_bibcode]['pubdate'] = int(start_bibcode[0:4])

    while (level < depth) and (0 < len(bibcodes_to_query)):
        level += 1
        new_bibcodes_to_query = []

        query_string = 'bibcode\n' + '\n'.join(bibcodes_to_query)
        
        r = requests.post("https://api.adsabs.harvard.edu/v1/search/bigquery",\
                         params={"q":"*:*", "fl": "bibcode,title,citation", "rows":2000},
                         headers={'Authorization': 'Bearer ' + token},
                         data=query_string)

        queries_by_bibcode = r.json()['response']['docs']

        for query in queries_by_bibcode:
            if 'citation' in query:
                citing_papers = query['citation']
                qbibcode = query['bibcode']

                for cbibcode in citing_papers:
                    #don't query if paper has already appeared or if the paper has 0 cites
                    if (cbibcode not in citation_graph):
                        new_bibcodes_to_query.append(cbibcode)
                    if cbibcode != start_bibcode:
                        citation_graph.add_edge(cbibcode, qbibcode)
                        citation_graph.node[cbibcode]['pubdate'] = int(cbibcode[0:4])

        bibcodes_to_query = new_bibcodes_to_query

    return citation_graph
