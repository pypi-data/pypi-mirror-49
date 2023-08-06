"""
Class that contains the results of a MaBoSS simulation.
"""

from __future__ import print_function
from sys import stderr, stdout, version_info
from .figures import make_plot_trajectory, plot_piechart, plot_fix_point, plot_node_prob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from multiprocessing import Pool
if version_info[0] < 3:
    from StringIO import StringIO
else:
    from io import StringIO

class BaseResult(object):
    """
    Class that handles the results of MaBoSS simulation.
    
    :param simul: The simulation object that produce the results.
    :type simul: :py:class:`Simulation`
    :param command: specify a MaBoSS command, default to None for automatic selection
    
    When a Result object is created, two temporary files are written in ``/tmp/``
    these files are the ``.bnd`` and ``.cfg`` file represented by the associated
    Simulation object. MaBoSS is then executed on these to temporary files and
    its output are stored in a temporary folder. 
    The Result object has several attributes to access the contents of the
    folder as pandas dataframe. It also has methods to produce somme plots.

    By default, the cfg, bnd and MaBoSS output are removed from the disk when the
    Result object is destructed. Result object has a method to save cfg, bnd and results
    in the working directory.
    """

    def __init__(self, simul=None, command=None, workdir=None):
        
        self._trajfig = None
        self._piefig = None
        self._fpfig = None
        self._ndtraj = None
        self._err = False
        self.palette = {}
        self.statdist_traj_count = None
        self.thread_count = 1
    
        if simul is not None:
            self.palette = simul.palette
            self.statdist_traj_count = simul.param['statdist_traj_count']
            self.thread_count = simul.param['thread_count']
    
        self.fptable = None
        self.first_state_index = None
        self.states = None
        self.nodes = None
        self.state_probtraj = None
        self.state_probtraj_errors = None
        self.state_probtraj_full = None
        self.last_states_probtraj = None
        self.state_statdist = None
        self.statdist_clusters = None
        self.statdist_clusters_summary = None
        self.statdist_clusters_summary_error = None

        self.nd_probtraj = None
        self.nd_probtraj_error = None
        self._nd_entropytraj = None

        self.raw_probtraj = None
        self.raw_statdist = None
        self.raw_statdist_clusters = None
        self.raw_statdist_clusters_summary = None

    def plot_trajectory(self, legend=True, until=None, error=False, prob_cutoff=0.01):
        """Plot the graph state probability vs time.

        :param float until: plot only up to time=`until`
        :param bool legend: display legend
        """
        if self._err:
            print("Error, plot_trajectory cannot be called because MaBoSS"
                  "returned non 0 value", file=stderr)
            return
        table = self.get_states_probtraj(prob_cutoff=prob_cutoff)
        table_error = None
        if error:
            table_error = self.get_states_probtraj_errors()
            if prob_cutoff is not None:
                table_error = table_error.loc[:, table.columns]

        if until:
            table = table[table.index <= until]
            if error:
                table_error = table_error[table_error.index <= until]

        _, ax = plt.subplots(1,1)
      
        make_plot_trajectory(table, ax, self.palette, legend=legend, error_table=table_error)

    def plot_piechart(self, embed_labels=False, autopct=4, prob_cutoff=0.01):
        """Plot the states probability distribution of last time point.

        :param float prob_cutoff: states with a probability below this cut-off
            are grouped as "Others"
        :param bool embed_labels: if True, the labels are displayed within the
            pie
        :param autopct: display pourcentages greater than `autopct` within the
            pie (defaults to 4 if it is a Boolean)
        :type autopct: float or bool
        """
        if self._err:
            print("Error, plot_piechart cannot be called because MaBoSS"
                  "returned non 0 value", file=stderr)
            return
        self._piefig, self._pieax = plt.subplots(1, 1)
        table = self.get_last_states_probtraj()
        plot_piechart(table, self._pieax, self.palette,
                embed_labels=embed_labels, autopct=autopct,
                prob_cutoff=prob_cutoff)

    def plot_fixpoint(self):
        """Plot the probability distribution of fixed point."""
        if self._err:
            print("Error maboss previously returned non 0 value",
                  file=stderr)
            return
        self._fpfig, self._fpax = plt.subplots(1, 1)
        plot_fix_point(self.get_fptable(), self._fpax, self.palette)

    def plot_node_trajectory(self, until=None, legend=True, error=False, prob_cutoff=0.01):
        """Plot the probability of each node being up over time.

        :param float until: plot only up to time=`until`.
        """
        if self._err:
            print("Error maboss previously returned non 0 value",
                  file=stderr)
            return
        self._ndtraj, self._ndtrajax = plt.subplots(1, 1)
        table = self.get_nodes_probtraj(prob_cutoff=prob_cutoff)
        table_error = None
        if error:
            table_error = self.get_nodes_probtraj_error()
        if until:
            table = table[table.index <= until]
            if error:
                table_error = table_error[table_error.index <= until]

        plot_node_prob(table, self._ndtrajax, self.palette, legend=legend, error_table=table_error)

    def plot_entropy_trajectory(self, until=None):
        """Plot the evolution of the (transition) entropy over time.

        :param float until: plot only up to time=`until`.
        """
        if self._err:
            print("Error maboss previously returned non 0 value",
                  file=stderr)
            return
        table = self.get_entropy_trajectory()
        if until:
            table = table[table.index <= until]
        table.plot()

    def get_fptable(self): 
        """Return the content of fp.csv as a pandas dataframe."""
        if self.fptable is None:
            try:
                self.fptable = pd.read_csv(self.get_fp_file(), "\t", skiprows=[0])

            except pd.errors.EmptyDataError:
                pass

        return self.fptable

    def get_nodes_probtraj(self, prob_cutoff=None):
        if self.nd_probtraj is None:
            
            table = self.get_raw_probtraj()
            self.nd_probtraj = self.make_node_proba_table(table)
        
        if prob_cutoff is not None:
            maxs = self.nd_probtraj.max(axis=0)
            return self.nd_probtraj[maxs[maxs>prob_cutoff].index]
     
        return self.nd_probtraj

    def get_nodes_probtraj_error(self):
        if self.nd_probtraj_error is None:
            table = self.get_raw_probtraj()
            self.nd_probtraj_error = self.make_node_proba_error_table(table)
        return self.nd_probtraj_error

    def get_states_probtraj(self, prob_cutoff=None, nb_cores=1):
        if self.state_probtraj is None:
            table = self.get_raw_probtraj()
            cols = self.get_states_cols(table)
            if self.states is None:
                if nb_cores == 1:
                    self.states = self.get_states(table, cols)
                else:
                    self.states = self.get_states_parallel(table, cols, nb_cores)
            if nb_cores > 1:
                self.state_probtraj = self.make_trajectory_table_parallel(table, self.states, cols, nb_cores)
            else:
                self.state_probtraj = self.make_trajectory_table(table, self.states, cols)
        
        if prob_cutoff is not None:
            maxs = self.state_probtraj.max(axis=0)
            return self.state_probtraj[maxs[maxs>prob_cutoff].index]
            
        return self.state_probtraj

    def get_states_probtraj_errors(self):
        if self.state_probtraj_errors is None:
            table = self.get_raw_probtraj()
            cols = self.get_states_cols(table)
            if self.states is None:
                self.states = self.get_states(table, cols)
            self.state_probtraj_errors = self.make_trajectory_error_table(table, self.states, cols)
        return self.state_probtraj_errors

    def get_states_probtraj_full(self, prob_cutoff=None):
        if self.state_probtraj_full is None:
            table = self.get_raw_probtraj()
            cols = self.get_states_cols(table)
            full_cols = ["TH", "ErrorTH", "H"]

            for col in self.get_states(table, cols):
                full_cols.append("Prob[%s]" % col)
                full_cols.append("ErrProb[%s]" % col)

            self.state_probtraj_full = self.make_trajectory_full_table(table, full_cols, cols)

        if prob_cutoff is not None:
            maxs = self.state_probtraj_full.max(axis=0)
            cols = ["TH", "ErrorTH", "H"]

            for state in maxs[maxs > prob_cutoff].index:
                if state.startswith("Prob["):
                    cols.append(state)
                    cols.append("Err%s" % state)

            return self.state_probtraj_full[cols]            
      
        return self.state_probtraj_full

    def get_last_states_probtraj(self):
        if self.last_states_probtraj is None:
            last_table = self.get_raw_probtraj().tail(1).copy().dropna(axis='columns')
            cols = self.get_states_cols(last_table)
            last_states = self.get_states(last_table, cols, nona=True)
            self.last_states_probtraj = self.make_trajectory_table(last_table, last_states, cols, nona=True)

        return self.last_states_probtraj

    def get_states_statdist(self):
        if self.state_statdist is None:
            table = self.get_raw_statdist()
            cols = range(0, len(table.columns), 2)

            if self.states is None:
                self.states = self.get_states(table, cols)
            self.state_statdist = self.make_statdist_table(table, self.states)
        return self.state_statdist

    def get_entropy_trajectory(self):
        if self._nd_entropytraj is None:
            self._nd_entropytraj = pd.read_csv(
                self.get_probtraj_file(), "\t", usecols=('TH', 'H'), dtype=self.get_probtraj_dtypes()
            )
        return self._nd_entropytraj

    def get_raw_probtraj(self):
        if self.raw_probtraj is None:
            self.raw_probtraj = pd.read_csv(self.get_probtraj_file(), "\t", dtype=self.get_probtraj_dtypes())
        return self.raw_probtraj

    def get_raw_statdist(self):
        if self.raw_statdist is None:
            statdist_traj_count = self.get_statdist_trajcount()

            self.raw_statdist = pd.read_csv(
                self.get_statdist_file(), "\t", 
                nrows=statdist_traj_count, 
                index_col=0,
                dtype=self.get_statdist_dtypes()
            )
        return self.raw_statdist

    def get_statdist_trajcount(self):
        if self.statdist_traj_count is None:
            with open(self.get_statdist_file(), 'r') as t_file:
                for i, line in enumerate(t_file):
                    if len(line) == 0:
                        self.statdist_traj_count = i - 2
                        break
        return self.statdist_traj_count

    def get_raw_statdist_clusters(self):
        if self.raw_statdist_clusters is None:
            self.raw_statdist_clusters = []

            indexes = []
            nb_lines = 0
            nb_cols = []
            nbs_cols = []
            with open(self.get_statdist_file(), 'r') as t_file:
                for i, line in enumerate(t_file):
                    # We look for the line breaks between each cluster
                    if line == '\n':
                        if len(indexes) > 0:
                            nbs_cols.append(max(nb_cols))
                            nb_cols = []

                        indexes.append(i)

                    if len(indexes) > 0:
                        nb_cols.append(len(line.split("\t")))
                nb_lines = i+1

            for i, index in enumerate(indexes):
                if i < len(indexes)-1:
                    start = index+2
                    end = indexes[i+1]-1
                
                    new_columns = ["Trajectory", "State", "Proba"]
                    for i in range(1, nbs_cols[i]//2):
                        new_columns += ["State.%d" % i, "Proba.%d" % i]
                    
                    df = pd.read_csv(
                        self.get_statdist_file(), 
                        skiprows=start, nrows=(end-start+1), 
                        header=None, sep="\t", index_col=0, names=new_columns
                    )

                    self.raw_statdist_clusters.append(df)
        return self.raw_statdist_clusters

    def get_statdist_clusters(self):
        if self.statdist_clusters is None:
            self.statdist_clusters = []

            # Getting all states
            all_states = set()
            for cluster in self.get_raw_statdist_clusters():
                for i_row, (index_row, row) in enumerate(cluster.iterrows()): 
                    t_states = [val for _, val in row[0::2].iteritems() if type(val) is str]
                    all_states.update(t_states)

                t_statdist_cluster = pd.DataFrame(
                    np.zeros((len(cluster.index), len(all_states))), 
                    index=cluster.index, columns=all_states
                )

                for index_row, row in cluster.iterrows():
                    for i_col, (_, state) in enumerate(row[0::2].iteritems()):
                        if type(state) is str:
                            val = row.iloc[(i_col*2)+1]
                            t_statdist_cluster.loc[index_row, state] = val

                self.statdist_clusters.append(t_statdist_cluster)

        return self.statdist_clusters

    def get_raw_statdist_clusters_summary(self):
        if self.raw_statdist_clusters_summary is None:
            start = 0
            with open(self.get_statdist_file(), 'r') as t_file:
                for i, line in enumerate(t_file):
                    if line == '\n':
                        start = i
            max_cols = 0
            lines = []
            with open(self.get_statdist_file(), 'r') as t_file:
                for i, line in enumerate(t_file):
                    if i > start+1: 
                        lines.append(line)
                        if len(line.split("\t")) > max_cols:
                            max_cols = len(line.split("\t"))

            cols = ["Cluster"] + ["State", "Proba", "ErrProba"]*((max_cols-1)//3)
            cols_tabs = "\t".join(cols) + "\n"
            lines.insert(0, cols_tabs)
            self.raw_statdist_clusters_summary = pd.read_csv(StringIO("".join(lines)), sep="\t", index_col=0)

        return self.raw_statdist_clusters_summary

    def get_statdist_clusters_summary(self):
        if self.statdist_clusters_summary is None:
            raw = self.get_raw_statdist_clusters_summary()

            # Getting all states
            all_states = set()
            for i_row, (index_row, row) in enumerate(raw.iterrows()): 
                t_states = [val for _, val in row[0::3].iteritems() if type(val) is str]
                all_states.update(t_states)

            self.statdist_clusters_summary = pd.DataFrame(
                np.zeros((len(raw.index), len(all_states))), 
                index=raw.index, columns=all_states
            )

            for index_row, row in raw.iterrows():
                for i_col, (_, state) in enumerate(row[0::3].iteritems()):
                    if type(state) is str:
                        val = row.iloc[(i_col*3)+1]
                        self.statdist_clusters_summary.loc[index_row, state] = val

            

        return self.statdist_clusters_summary


    def get_statdist_clusters_summary_error(self):
        if self.statdist_clusters_summary_error is None:
            raw = self.get_raw_statdist_clusters_summary()

            # Getting all states
            all_states = set()
            for i_row, (index_row, row) in enumerate(raw.iterrows()): 
                t_states = [val for _, val in row[0::3].iteritems() if type(val) is str]
                all_states.update(t_states)

            self.statdist_clusters_summary_error = pd.DataFrame(
                np.zeros((len(raw.index), len(all_states))), 
                index=raw.index, columns=all_states
            )

            for index_row, row in raw.iterrows():
                for i_col, (_, state) in enumerate(row[0::3].iteritems()):
                    if type(state) is str:
                        val = row.iloc[(i_col*3)+2]
                        self.statdist_clusters_summary_error.loc[index_row, state] = val

            

        return self.statdist_clusters_summary_error


    def get_probtraj_dtypes(self):
        with open(self.get_probtraj_file(), 'r') as probtraj:
            cols = probtraj.readline().split("\t")

            first_state_index = 5
            for i in range(first_state_index, len(cols)):
                if cols[i].startswith("State"):
                    first_state_index = i
                    break

            nb_states = int((len(cols) - first_state_index) / 3)

            dtype = {"Time": np.float64, "TH": np.float64, "ErrorTH": np.float64, "H": np.float64, "HD=0": np.float64}
            
            for i in range(first_state_index-5):
                dtype.update({("HD=%d" % (i+1)): np.float64})
            
            dtype.update({"State": np.str, "Proba": np.float64, "ErrorProba": np.float64})
            for i in range(1, nb_states):
                dtype.update({"State.%d" % i: np.str, "Proba.%d" % i: np.float64, "ErrorProba.%d" % i: np.float64})
            return dtype

    def get_statdist_dtypes(self):
        with open(self.get_statdist_file(), 'r') as statdist:
            cols = statdist.readline().split("\t")
            dtype = {}
            dtype.update({"State": np.str, "Proba": np.float64})

            for i in range(1, len(cols)//2):
                dtype.update({"State.%d" % i: np.str, "Proba.%d" % i: np.float64})
            
            return dtype

    def get_states_parallel(self, df, cols, nb_cores):
        states = set()
        with Pool(processes=nb_cores) as pool:
            states = states.union(*(pool.starmap(
                get_state_from_line, 
                [(df.iloc[i, :], cols) for i in df.index]
            )))
        return states

    def get_states(self, df, cols, nona=False):
        states = set()
        if nona:
            for i in range(len(df.index)):
                for c in cols:
                    states.add(df.iloc[i, c])
        else:
            for i in range(len(df.index)):
                for c in cols:
                    if type(df.iloc[i, c]) is str:  # Otherwise it is nan
                        states.add(df.iloc[i, c])

        return states
        
    def get_nodes(self, df, cols):
        if self.nodes is None:
            states = self.get_states(df, cols)
            self.nodes = set()
            for s in states:
                if s != '<nil>':
                    nds = s.split(' -- ')
                    for nd in nds:
                        self.nodes.add(nd)
        return self.nodes

    def get_first_state_index(self, df):
        """Return the indice of the first column being a state
           By default it's five, but if we specify some refstate,
           it'll be more.
        """
        if self.first_state_index is None:
            for i in range(5, len(df.columns)):
                if df.columns[i].startswith("State"):
                    self.first_state_index = i
                    break

        return self.first_state_index

    def write_statdist_table(self, filename, prob_cutoff=None):
        clusters = self.get_raw_statdist_clusters()
        clusters_summary = self.get_raw_statdist_clusters_summary()
        with open(filename, 'w') as statdist_table:

            for i_cluster, cluster in enumerate(clusters_summary.iterrows()):

                line_0 = "Probability threshold=%s\n" % (str(prob_cutoff) if prob_cutoff is not None else "") 
                line_1 = ["Prob[Cluster %s]" % cluster[0]] 
                line_2 = ["%g" % (len(clusters[i_cluster])/self.get_statdist_trajcount())]
                line_3 = ["ErrorProb"]

                t_cluster = cluster[1].dropna()

                for i in range(0, len(t_cluster), 3):
                    if prob_cutoff is None or t_cluster[i+1] > prob_cutoff:
                        line_1.append("Prob[%s | Cluster %s]" % (t_cluster[i], cluster[0]))
                        line_2.append("%g" % t_cluster[i+1])
                        line_3.append("%g" % t_cluster[i+2])

                statdist_table.write(line_0)
                statdist_table.write("\t".join(line_1) + "\n")
                statdist_table.write("\t".join(line_2) + "\n")
                statdist_table.write("\t".join(line_3) + "\n")
                statdist_table.write("\n")

    def make_trajectory_table(self, df, states, cols, nona=False):
        """Creates a table giving the probablilty of each state a every moment.

            The rows are indexed by time points and the columns are indexed by
            state name.
        """

        time_points = np.asarray(df['Time'])
        
        time_table = pd.DataFrame(
            np.zeros((len(time_points), len(states))),
            index=time_points, columns=states
        )

        if len(time_points) > 1:
            for index, (_, row) in enumerate(time_table.iterrows()):
                make_trajectory_line(row, df, cols, index, nona)
        
            time_table.sort_index(axis=1, inplace=True) 
        else:
            make_trajectory_line(time_table.iloc[0, :], df, cols, 0, nona)
            time_table.sort_index(axis=1, inplace=True) 

        return time_table


    def make_trajectory_error_table(self, df, states, cols):
        """Creates a table giving the probablilty of each state a every moment.

            The rows are indexed by time points and the columns are indexed by
            state name.
        """
        
        time_points = np.asarray(df['Time'])
        time_table = pd.DataFrame(
            np.zeros((len(time_points), len(states))),
            index=time_points, columns=states
        )
        for index, (_, row) in enumerate(time_table.iterrows()):
            make_trajectory_error_line(row, df, cols, index)

        time_table.sort_index(axis=1, inplace=True) 

        return time_table

    def make_trajectory_full_table(self, df, states, cols): 
        """
        Creates a table with the format used in the original script MBSS_FormatTable.pl

        """
        time_points = df["Time"]
        time_table = pd.DataFrame(
            np.zeros((len(time_points), len(states))),
            index=time_points, columns=states
        )

        time_table['TH'] = df['TH'].values
        time_table['ErrorTH'] = df['ErrorTH'].values
        time_table['H'] = df['H'].values

        for index, (_, row) in enumerate(time_table.iterrows()):
            make_trajectory_full_line(row, df, cols, index)

        return time_table

    def make_trajectory_table_parallel(self, df, states, cols, nb_cores):
        # TODO : Here we should parallelize all these functions
        """Creates a table giving the probablilty of each state a every moment.

            The rows are indexed by time points and the columns are indexed by
            state name.
        """

        with Pool(processes=nb_cores) as pool:
            time_table = pd.concat(pool.starmap(
                make_trajectory_line_parallel, 
                [(df.iloc[i, :], states, cols) for i in df.index]
            ))
        
        time_table.sort_index(axis=1, inplace=True) 
        return time_table

    def make_statdist_table(self, df, states):    
        time_table = pd.DataFrame(
            np.zeros((len(df.index), len(states))),
            columns=states
        )

        for index, (_, row) in enumerate(time_table.iterrows()):
            make_statdist_line(row, df, range(0, len(df.columns), 2), index)

        return time_table

    def make_node_proba_table(self, df):
        """Same as make_trajectory_table but with nodes instead of states."""
        cols = self.get_states_cols(df)
        nodes = self.get_nodes(df, cols)
        time_points = np.asarray(df['Time'])
        time_table = pd.DataFrame(
            np.zeros((len(time_points), len(nodes))),
            index=time_points, columns=nodes
        )

        for index, (_, row) in enumerate(time_table.iterrows()):
            make_node_proba_line(row, df, cols, index)

        time_table.sort_index(axis=1, inplace=True)
        return time_table

    def make_node_proba_error_table(self, df):
        """Same as make_trajectory_table but with nodes instead of states."""
        cols = self.get_states_cols(df)
        nodes = self.get_nodes(df, cols)
        time_points = np.asarray(df['Time'])
        time_table = pd.DataFrame(
            np.zeros((len(time_points), len(nodes))),
            index=time_points, columns=nodes
        )
        for index, (_, row) in enumerate(time_table.iterrows()):
            make_node_proba_error_line(row, df, cols, index)

        time_table.sort_index(axis=1, inplace=True)
        return time_table

    def get_states_cols(self, df):
        if isinstance(df, pd.DataFrame):
            return range(self.get_first_state_index(df), len(df.columns), 3)
        else:
            return range(self.get_first_state_index(df), len(df), 3)


def make_trajectory_line(row, df, cols, index, nona=False):
    if nona:
        for c in cols:
            state = df.iloc[index, c]
            row[state] = df.iloc[index, c+1]
    else:
        for c in cols:
            if type(df.iloc[index, c]) is str:  # Otherwise it is nan
                state = df.iloc[index, c]
                row[state] = df.iloc[index, c+1]
   
def make_trajectory_error_line(row, df, cols, index):
    for c in cols:
        if type(df.iloc[index, c]) is str:  # Otherwise it is nan
            state = df.iloc[index, c]
            row[state] = df.iloc[index, c+2]

def make_trajectory_full_line(row, df, cols, index):
    for c in cols:
        if type(df.iloc[index, c]) is str:# Otherwise it's NaN
            state = df.iloc[index, c]
            row["Prob[%s]" % state] = df.iloc[index, c+1]
            row["ErrProb[%s]" % state] = df.iloc[index, c+2]

def make_trajectory_line_parallel(row, states, cols):
    df = pd.DataFrame(np.zeros((1, len(states))), index=[row["Time"]], columns=states)
    for c in cols:
        if type(row[c]) is str:  # Otherwise it is nan
            state = row[c]
            df[state][row["Time"]] = row[c+1]
    return df

def make_statdist_line(row, df, cols, index):
    for c in cols:
        if type(df.iloc[index, c]) is str:  # Otherwise it is nan
            state = df.iloc[index, c]
            row[state] = df.iloc[index, c+1]

def get_state_from_line(line, cols):
    t_states = set()
    for c in cols:
        if type(line[c]) is str:  # Otherwise it is nan
            t_states.add(line[c])
    return t_states

def make_node_proba_line(row, df, cols, index):
    for c in cols:
        if type(df.iloc[index, c]) is str:
            state = df.iloc[index, c]
            if state != '<nil>':
                nodes = state.split(' -- ')
                for nd in nodes:
                    value = df.iloc[index, c+1]
                    row[nd] += value

def make_node_proba_error_line(row, df, cols, index):
    for c in cols:
        if type(df.iloc[index, c]) is str:
            state = df.iloc[index, c]
            if state != '<nil>':
                nodes = state.split(' -- ')
                for nd in nodes:
                    row[nd] += df.iloc[index, c+2]

__all__ = ["Result", "StoredResult"]
