from spacy.tokens import Doc

def merger(doc):
    """
    Assumes that the lists can contain no more than one duplicate of each entity
    """
    list_ner, list_regex = doc.ents, doc._.ents_regex

    print("List_ner", list_ner, "List_regex", list_regex)
    #Remove overlap from regex list
    correct_regex = []
    start_index_list = []
    end_index_list = []
    for ent in list_regex:
        if ent.start in start_index_list or ent.end in end_index_list:
            continue
        else:
            correct_regex.append(ent)
            start_index_list.append(ent.start_char)
            end_index_list.append(ent.end_char)

    print("Correct_regex", correct_regex)
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
    print("Merged", merged)

    merged.sort(key=lambda x: x.start)
    final = merged.copy()
    if merged:
        for i in range(len(merged)):
            if(i==len(merged)-1):
                continue
            start_a = merged[i].start_char
            start_b = merged[i+1].start_char
            end_a = merged[i].end_char
            end_b = merged[i+1].end_char

            if start_a == start_b or end_a==end_b:
                start = min(start_a, start_b)
                end = max(end_a, end_b)
                del final[i:i+2]
                new_ent = doc.char_span(start, end, merged[i].label)
            elif start_a<start_b and end_a > end_b:
                start = min(start_a, start_b)
                end = max(end_a, end_b)
                del final[i:i+2]
                new_ent = doc.char_span(start, end, merged[i].label)
    print("final", final)
    doc.ents = final
    return doc