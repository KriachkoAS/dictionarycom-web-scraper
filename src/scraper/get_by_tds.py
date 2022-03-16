from .imported import *



def get_hw(tds) -> str:
    hws = tds.select('.e1wg9v5m5')
    if (len(hws) == 1):
        if hws[0].find():
            raise Exception('Unsupported HW format')
        return str(hws[0].contents[0])
    raise Exception('HW amount exception')



class WordLVL:
    def __init__(self, el):

        if len(el.contents) == 1:
            if 'css-irpbha' in el.contents[0]['class']:
                el = el.contents[0]
            else:
                raise Exception('Unsupported word LVL format')
        else:
            raise Exception('Word LVL amount error')

        
        if ('img' == el.contents[0]['role']
        and 'aria-label' in el.contents[0].attrs
        and isinstance(el.contents[3], bs4.element.NavigableString)
        and isinstance(el.contents[2], bs4.element.Comment)
        and el.contents[1] == ' '
        and len(el.contents) == 4):

            self.img = el.contents[0].decode_contents()
            self.name = el.contents[3]
            self.img_name = el.contents[0]['aria-label']
            
            if not self.name or not self.img or not self.img_name:
                raise Exception('WordLVL build error')
        else:
            raise Exception('Unsupported LVL format')


def get_lvl(tds) -> WordLVL:
    wls = tds.select('[data-testid=\'word-complexity-badge\']')
    if (len(wls)) == 0:
        return None
    for i in range(1, len(wls)):
        if wls[0] != wls[i]:
            raise Exception('Different lvls')
    return WordLVL(wls[0])



def get_ipa_by_multiple_parts(parts: list[str]) -> dict[str: str]:
    res = {}
    for i in parts:
        el = bs4.BeautifulSoup(i.strip(), features="html.parser")
        con = el.contents
        poses = el.find_all(class_ = 'luna-pos')
        for i in range(len(poses) - 1):
            if ("luna-pos" not in el.contents[i * 2]['class']
            or el.contents[i * 2 + 1] != ' '
            or el.contents[i * 2].string[-1:] != ','):
                raise Exception('Unsupported ipa poses structure')
            poses[i] = poses[i].string[:-1].strip()
            con = con[2:]
        if ("luna-pos" not in el.contents[(len(poses) - 1) * 2]['class']
        or ',' in el.contents[(len(poses) - 1) * 2]):
            raise Exception('Unsupported ipa poses structure')
        poses[len(poses) - 1] = poses[len(poses) - 1].string.strip()
        con.pop(0)

        #creating res_ipa
        res_ipa = ''
        for j in con:
            res_ipa += str(j)
        res_ipa = res_ipa.strip()

        #fullfilling res
        for i in poses:
            if i in res:
                raise Exception('Pos duplication during block.ipa agregation')
            res[i] = res_ipa
    return res


def get_ipa(tds) -> dict[str: str]:
    ipa_secs = tds.find_all(class_='pron-ipa-content')
    if len(ipa_secs) == 0:
        return None

    elif len(ipa_secs) == 1:
        dec_con = ipa_secs[0].decode_contents()
        if dec_con[0] != '/' or dec_con[-1] != '/':
            raise Exception('Unsupported IPA representation')
        dec_con = dec_con[1:-1]
        parts = dec_con.split(';')

        if len(parts) == 0:
            raise Exception('Block IPA partition error')
        elif len(parts) == 1:
            return {'*': parts[0].strip()}
        else:
            return get_ipa_by_multiple_parts(parts)

    raise Exception('tds IPA amount error')



class POS:
    def __init__(self, el):

        self.forms = el.find_all(class_ = 'e1hk9ate1')
        if len(self.forms) == 0:
            self.forms = None
        elif len(self.forms) == 1:
            self.forms = self.forms[0]
            supposed_pos_core_el = el.find(class_ = 'luna-pos')
            supposed_pos_core_el.string = supposed_pos_core_el.string.strip()
            if supposed_pos_core_el.string[-1] == ',':
                supposed_pos_core_el.string = supposed_pos_core_el.string[:-1]
            else:
                raise Exception('Unsupported coma absence in POS name')
        else:
            raise Exception('Forms blocks amount exception')

        pos_name_els = el.find_all(class_ = 'e1hk9ate2')
        if len(pos_name_els) == 1:
            pos_name_core_els = pos_name_els[0].find_all()
            if len(pos_name_core_els) == 1:
                if 'luna-pos' in pos_name_core_els[0]['class']:
                    self.name = pos_name_core_els[0].decode_contents()
                else:
                    raise Exception('Unsupported POS name format')
            else:
                raise Exception('POS amount error (inner)')
        else:
            raise Exception('POS amount error (outer)')


def get_poses(tds):
    pos_secs = tds.parent.find_all(class_ = 'e1hk9ate4')
    poses = []
    for i in pos_secs:
        poseses = []
        poseses = i.find_all(class_ = 'e1hk9ate3')
        if len(poseses) == 1:
            poses.append(POS(poseses[0]))
        else:
            raise Exception('tds POS amount error')
    return poses