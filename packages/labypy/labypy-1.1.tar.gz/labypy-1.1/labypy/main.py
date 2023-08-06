from labypy import Halo
from Authenticate import LabyAuth

cookie = ""
halo = Halo.Instance(cookie, "707243")
Acc1 = LabyAuth("SchlechteAbsicht", "Fussball2004")
cookie = Acc1.getCookie()
print(cookie)
halo.update_visibility(0)
