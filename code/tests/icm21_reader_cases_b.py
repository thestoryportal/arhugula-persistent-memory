"""ReaderControls D2 wire, dispatch-coverage and registry-adapter cases (mixin for test_icm21)."""
from icm21_case_d2_wire import D2WireParserCase
from icm21_case_references import DispatchCoverageCase
from icm21_case_registry import CandidateRegistryCase


class ReaderCasesB(D2WireParserCase, DispatchCoverageCase, CandidateRegistryCase):
    pass
