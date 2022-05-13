from typing import Dict

from epics import PV
from lcls_tools.superconducting.scLinac import Cavity, Cryomodule, make_lcls_cryomodules


class AcceptanceCavity(Cavity):
    def __init__(self, cavityNum, rackObject, ssaClass, stepperClass):
        super().__init__(cavityNum, rackObject)
        self.pvPrefix = self.pvPrefix + "AT:"

        self.at_gmaxPV: PV = PV(self.pvPrefix + "GMAX")
        self.at_amaxPV: PV = PV(self.pvPrefix + "AMAX")
        self.at_gusePV: PV = PV(self.pvPrefix + "GUSE")
        self.at_ausePV: PV = PV(self.pvPrefix + "AUSE")
        self.at_feonset_gradientPV: PV = PV(self.pvPrefix + "FEON_GACT")
        self.at_feonset_amplitudePV: PV = PV(self.pvPrefix + "FEON_AACT")

    def update_amax(self):
        self.at_amaxPV.put(self.at_gmaxPV.value * self.length)

    def update_ause(self):
        self.at_ausePV.put(self.at_gusePV.value * self.length)

    def update_feonset(self):
        self.at_feonset_amplitudePV.put(self.at_feonset_gradientPV.value * self.length)

    def update_amplitudes(self):
        self.update_amax()
        self.update_ause()
        self.update_feonset()


ACCEPTANCECRYOMODULES: Dict[str, Cryomodule] = make_lcls_cryomodules(cavityClass=AcceptanceCavity)

for cryomodule in ACCEPTANCECRYOMODULES.values():
    for cavity in cryomodule.cavities.values():
        cavity.update_amplitudes()
