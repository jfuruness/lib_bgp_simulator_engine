from .announcement import Announcement
from .bgp_as import BGPAS
from .bgp_dag import BGPDAG


class SimulatorEngine(BGPDAG):
    def run(self, announcements, save_path=None, clear=True):
        """Propogates announcements"""

        self._seed(announcements)
        self._propogate()
        if save_path:
            self._save(save_path)
        if clear:
            self._clear()

    def _seed(self, announcements: list):
        """Seeds/inserts announcements into the BGP DAG"""

        for ann in announcements:
            assert isinstance(ann, Announcement)

        prefix_origins = list()
        for ann in announcements:
            # Let the announcement do the seeding
            # That way it's easy for anns to seed with path manipulation
            # Simply inherit the announcement class
            ann.seed(self.as_dict)
            prefix_origins.append((ann.prefix, ann.origin))

        msg = "You should never have overlapping prefix origin pairs"
        assert len(prefix_origins) == len(set(prefix_origins)), msg

    def _propogate(self):
        """Propogates announcements"""

        print("fill in prop func")
        for rank in self.ranks:
            for as_obj in rank:
                as_obj.propogate(Relationships.PROVIDERS)
            for as_obj in rank:
                as_obj.process_incoming_anns(Relationships.CUSTOMERS)
            for as_obj in rank:
                as_obj.propogate(Relationships.PEERS)
            for as_obj in rank:
                as_obj.process_incoming_anns(Relationships.PEERS)

        for i, rank in enumerate(reversed(self.ranks)):
            # There are no incomming Anns at the top
            if i > 0:
                for as_obj in rank:
                    as_obj.process_incoming_anns(Relationships.PROVIDERS)
            for as_obj in rank:
                as_obj.propogate_to_customers(Relationships.CUSTOMERS)

    def _save(self):
        """Saves DAG"""

        print("fill in save func")

    def _clear(self):
        """Clears DAG"""

        print("fill in clear func")
