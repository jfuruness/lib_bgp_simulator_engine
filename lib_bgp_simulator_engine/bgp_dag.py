from .base_as import AS
from .bgp_as import BGPAS

class BGPDAG:
    """BGP Topology. Must be a DAG"""

    # Slots are used here to allow for fast access (1/3 faster)
    # And also because it allows others to easily see the instance attrs
    __slots__ = ["as_dict", "ranks"]

    def __init__(self, tsv_path: str, as_classes_dict={0: BGPAS}):
        """Reads in relationship data from a TSV and generate graph"""

        rows = self._read_relationships(tsv_path)
        self.as_dict, max_rank = self._populate_as_dict(rows, as_classes_dict)
        self._convert_relationships_to_references()
        self._assert_dag()
        self.ranks: tuple = self._get_ranks(max_rank)

    def _read_relationships(self, tsv_path):
        """Reads in the relationships data"""

        with open(tsv_path, "r") as f:
            return list(csv.DictReader(f, delimiter="\t"))

    def _populate_as_dict(self, rows: list, as_classes_dict: dict):
        """Populates AS dict and gets the max rank"""

        max_rank = 0
        as_dict = dict()
        # populates AS dict
        for row in rows:
            try:
                # Type of AS that this AS is
                ASCls = as_classes_dict[row["as_type"]]
                assert isinstance(ASCls, AS), "Improper AS type"
            # If the type of AS doesn't exist in the as dict
            except IndexError as e:
                msg = f"as_type_dict doesn't have an entry of {row['as_type']}"
                logging.error(msg)
                raise e

            as_dict[row["asn"]] = ASCls(**row)
            max_rank = max_rank if row["rank"] <= max_rank else row["rank"]
        return as_dict, max_rank
        
    def _convert_relationships_to_references(self):
        """Converts peers, customers, providers to references from ints"""

        # Converts list of ints to AS objects
        for asn, as_obj in self.as_dict.items():
            for attr in ["peers", "customers", "providers"]:
                refs = [self.as_dict[asn] for asn in getattr(as_obj, attr)]
                setattr(as_obj, attr, refs)

    def _assert_dag(self):
        """Asserts that graph is a DAG for provider customers"""

        # I know it could be done with dynamic programming. idc.
        for asn, as_obj in self.as_dict.items():
            # Make sure there are no provider or provider loops
            for attr in ["customers", "providers"]:
                self._assert_dag_helper(as_obj, set(as_obj), attr)
            

    def _assert_dag_helper(self, og_as_obj, set_of_asns: set, attr: str):
        """Recursive func to make sure there are no cycles"""

        for as_obj in getattr(og_as_obj, attr):
            # Make sure we aren't cycling
            assert as_obj.asn not in set_of_asns, "Not a DAG"
            # Make a new set and add the current AS object to it
            temp_set_of_asns = set_of_asns.copy()
            temp_set_of_asns.add(as_obj.asn)
            # Continue recursively searching
            self._assert_dag_helper(as_obj, temp_set_of_asns)

    def _get_ranks(self, max_rank):
        """Orders ASes by rank"""

        # Create a list of empty lists
        ranks = list(list() for _ in range(max_rank + 1))
        # Append the ASes into their proper rank
        for as_obj in self.as_dict.values():
            ranks[as_obj.rank].append(asn)
        # Sort the ASes for deterministic
        for i, rank in enumerate(ranks):
            ranks[i] = tuple(sorted(rank))
        # Tuples are faster
        return tuple(ranks)
