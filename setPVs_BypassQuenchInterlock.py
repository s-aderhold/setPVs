from time import sleep
from typing import Dict

from epics import PV
from lcls_tools.superconducting.scLinac import Cavity, Cryomodule, CryoDict

BYPASS_VALUE = 1
UNBYPASS_VALUE = 0


class BypassCavity(Cavity):
    def __init__(self, cavityNum, rackObject, ssaClass, stepperClass):
        super().__init__(cavityNum, rackObject)

        self.quench_bypassPV: PV = PV(self.pvPrefix + "QUENCH_BYP")

    def change_quench_interlock(self):
        self.quench_bypassPV.put(BYPASS_VALUE)


BYPASS_CRYOMODULES: Dict[str, Cryomodule] = CryoDict(cavityClass=BypassCavity)

for cryomodule in BYPASS_CRYOMODULES.values():
    for cavity in cryomodule.cavities.values():
        print("Setting {pv} to {value}".format(pv=cavity.quench_bypassPV.pvname, value=))
        cavity.change_quench_interlock()
        sleep(0.2)
        print("New value for {pv} is {value}".format(pv=cavity.measured_quality_factorPV.pvname,
                                                     value=cavity.measured_quality_factorPV.value))
