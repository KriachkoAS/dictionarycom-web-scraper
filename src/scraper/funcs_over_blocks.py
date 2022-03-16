from .PagePartBlock import PagePartBlock
from .imported import *



def get_us_tdses(dom): #return only american dictionary topDefinitionSections
    secs = []
    cur = dom.find(id="examples-section").find_previous(id="top-definitions-section")
    while cur != None:
        secs.insert(0, cur)
        cur = cur.find_previous(id="top-definitions-section")

    return secs


def get_prepared_blocks(dom, word, block_filter):
    blocks =    [i for i in
                    [PagePartBlock(i) for i in get_us_tdses(dom)]
                if block_filter(word, i.hw)]

    for i in blocks:
            i.assign_secondary_fields()

    return blocks



def get_lvl(blocks):
    lvl = blocks[0].lvl
    for i in blocks:
        if i.lvl.name != lvl.name:
            raise Exception('Different LVLs aggregation')
    return lvl



def simplify_pos_name(pos_name):
    if 'verb' in pos_name.split(' '):
        return 'verb'
    return pos_name

def add_to_ipa_dict(ipa_dict, pos_name, ipa_str):
    if pos_name in ipa_dict:
        if ipa_dict[pos_name] != ipa_str:
            raise Exception('Unaggregatable page ipa')
    ipa_dict[pos_name] = ipa_str



def raise_if_form_ipa(blocks):
    for i in blocks:
        for j in i.poses:
            if j.forms:
                if len(j.forms.find_all(class_ = 'pron-ipa')) > 0:
                    raise Exception('Form ipa exception')

def get_ipa(blocks):
    raise_if_form_ipa(blocks)
    aggregated = {}
    for i in blocks:
        #'*' unpacking
        if len(i.ipa) == 1 and '*' in i.ipa:
            ipa_str = i.ipa.pop('*')
            for j in i.poses:
                add_to_ipa_dict(i.ipa, simplify_pos_name(j.name), ipa_str)
        
        if '*' in i.ipa:
            raise Exception('* pos still exist after replace')
        
        #append to aggregated
        for j in i.ipa:
            add_to_ipa_dict(aggregated, j, i.ipa[j])
    
    return aggregated



def reverse_pos_to_ipa_dict(ipa):
    res = {}
    for i in ipa:
        if ipa[i] not in res:
            res[ipa[i]] = set()
        res[ipa[i]].add(i)
    if len(res) == 1:
        res[list(res)[0]] = set('*')
    return res