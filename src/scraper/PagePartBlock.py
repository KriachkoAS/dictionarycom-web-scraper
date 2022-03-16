from .get_by_tds import *
from .imported import *



class PagePartBlock:
    def __init__(self, tds):
        self.tds = tds
        self.hw = get_hw(tds)
        
    def assign_secondary_fields(self):

        try: self.lvl = get_lvl(self.tds)
        except: pass
        
        try:
            self.poses = get_poses(self.tds)
        except: pass

        try:
            self.ipa = get_ipa(self.tds)
        except: pass