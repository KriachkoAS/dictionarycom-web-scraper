from inspect import trace
from .imported import *
from .funcs_over_blocks import *



class ParsedWord:
    """class to parse html string and work with one parsed"""

    @staticmethod
    def default_block_filter(word, hw):
        return not word or word == hw


    def __init__(self, html, word = None, block_filter = default_block_filter, save_blocks = False):

        self.word = word
        dom = bs4.BeautifulSoup(html, features="html.parser")


        try:
            
            blocks = funcs_over_blocks.get_prepared_blocks(dom, word, block_filter)

            try: self.lvl = funcs_over_blocks.get_lvl(blocks)
            except: pass

            try: self.ipa = funcs_over_blocks.get_ipa(blocks)
            except:
                #traceback.print_exc()
                pass

            #aftercode
            if (save_blocks):
                self.blocks = blocks

        except:
            pass
    

    @staticmethod
    def is_parse_complete(html):
        return None
    

    def ipa_as_str(self):
        if len(self.ipa) == 0:
            return ''
        rev_ipa = reverse_pos_to_ipa_dict(self.ipa)
        ids = list(rev_ipa)
        ids.sort(key = lambda x: len(rev_ipa[x]))


        for i in rev_ipa:
            if 'adjective' in rev_ipa[i]:
                ids.remove(i)
                ids.insert(0, i)
        
        for i in rev_ipa:
            if 'verb' in rev_ipa[i]:
                ids.remove(i)
                ids.insert(0, i)
        

        res = ''
        while len(ids) > 1:
            poses_str = ''
            for i in rev_ipa[ids[0]]:
                poses_str += i + ', '
            poses_str = poses_str[:-2]
            res = '; ' + poses_str + ": " + ids.pop(0) + res
        res = ids[0] + res
        return res