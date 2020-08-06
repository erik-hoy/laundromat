from spacy.tokens import Doc

def merger(doc):
    """
    Assumes that the lists can contain no more than one duplicate of each entity
    """
    list_ner, list_regex = doc.ents, doc._.ents_regex

    #Remove overlap from regex list
    correct_regex = []
    start_index_list = []
    end_index_list = []
    for ent in list_regex:
        if ent.start in start_index_list or ent.end in end_index_list:
            continue
        else:
            correct_regex.append(ent)
            start_index_list.append(ent.start)
            end_index_list.append(ent.end)

    merged = list(list_ner)
    start_index_list = [ent.start for ent in list_ner]
    end_index_list = [ent.end for ent in list_ner]
    for ent in correct_regex:
        if ent.start in start_index_list or ent.end in end_index_list:
            continue
        else:
            merged.append(ent)
            start_index_list.append(ent.start)
            end_index_list.append(ent.end)
    #print("List ner", list_ner, "List regex", list_regex, "correct regex", correct_regex)
    #print("Merged", merged)
    doc.ents = merged
    return doc