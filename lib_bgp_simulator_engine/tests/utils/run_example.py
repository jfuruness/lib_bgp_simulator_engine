from .graph_writer import write_graph

from ...bgp_as import BGPAS


# tmp_path is a pytest fixture
def run_example(tmp_path,
                peers=list(),
                customer_providers=list(),
                as_types=dict(),
                as_classes_dict={0: BGPAS},
                announcements=list(),
                local_ribs=dict(),
                ):
    """Runs an example"""

    write_graph(peers, customers_providers, as_types, tmp_path)
    engine = SimulatorEngine(str(tmp_path), as_type_dict)
    engine.run(announcements, clear=False)
    for as_obj in engine:
        assert as_obj.local_rib.assert_eq(lobal_ribs[as_obj.asn])
