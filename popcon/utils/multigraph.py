class Multigraph:
    """
    Query-able structure for holding a population of graphs.

    Parameters
    ----------
    participants : pd.DataFrame
        Dataframe containing subject-level information.
    graphs : np.ndarray
        Tensor of graphs, shape (n_subjects, n_vertices, n_vertices)

    Returns
    -------
    self : Multigraph
    """

    def __init__(self, participants, graphs):
        self.df = participants
        self.graphs = graphs

    def query(self, expr):
        """
        Obtain a subset of `graphs` by querying `participants`.

        Parameters
        ----------
        expr : string
            Expression used to query `participants`.

        Returns
        -------
        sub_df : pd.DataFrame
            Subset of `self.participants` identified by the query
        graphs : np.ndarray
            Subset of graphs corresponding to subjects in `sub_df`
        """
        sub_df = self.df.query(expr)
        slices = sub_df["slice"]
        graphs = [self.graphs[int(i)] for i in slices]
        return sub_df, graphs
