from time import sleep
from typing import Dict

from epics import PV
from lcls_tools.superconducting.scLinac import Cavity, Cryomodule, make_lcls_cryomodules

NEW_QUALITY_FACTOR = 2e10


class AcceptanceCavity(Cavity):
    def __init__(self, cavityNum, rackObject, ssaClass, stepperClass):
        super().__init__(cavityNum, rackObject)

        self.measured_quality_factorPV: PV = PV(self.pvPrefix + "Q0:MEAS")

    def update_quality_factor(self):
        self.measured_quality_factorPV.put(NEW_QUALITY_FACTOR)


ACCEPTANCECRYOMODULES: Dict[str, Cryomodule] = make_lcls_cryomodules(cavityClass=AcceptanceCavity)

for cryomodule in ACCEPTANCECRYOMODULES.values():
    for cavity in cryomodule.cavities.values():
        print("Setting {pv} to {value}".format(pv=cavity.measured_quality_factorPV.pvname, value=NEW_QUALITY_FACTOR))
        cavity.update_quality_factor()
        sleep(0.2)
        print("New value for {pv} is {value}".format(pv=cavity.measured_quality_factorPV.pvname,
                                                     value=cavity.measured_quality_factorPV.value))
