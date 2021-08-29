from datetime import datetime

from .graph_writer import write_graph

from ...bgp_as import BGPAS
from ...simulator_engine import SimulatorEngine


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

    path = tmp_path / "example.tsv"
    write_graph(peers, customer_providers, as_types, path)
    print("populating engine")
    start = datetime.now()
    engine = SimulatorEngine(str(path), as_classes_dict)
    print((start-datetime.now()).total_seconds())
    print("Running engine")
    start = datetime.now()
    engine.run(announcements, clear=False)
    input((start-datetime.now()).total_seconds())
    for as_obj in engine:
        print("ASN:", as_obj.asn)
        for prefix, ann in as_obj.local_rib.items():
            print(ann)
        if local_ribs:
            as_obj.local_rib.assert_eq(local_ribs[as_obj.asn])
