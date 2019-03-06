import spacy

texts = ['Andy Cole and Shearer – with 34 goals in 1993–94 and 1994–95, respectively – scored the most goals to win the Golden Boot when the Premier League was a 42-game season, Mohamed Salah with 32 goals in 2017–18 holds the record for the current 38-game season, while Nicolas Anelka scored the fewest to clinch the award outright, with 19 goals in 2008–09.' , 'The all-time record for lowest number of goals scored to be bestowed the award, however, is 18 goals; this was achieved during the 1997–98 and 1998–99 seasons, when the award was shared between three players both times.', 'The latter season marked the last time the Golden Boot was shared until 2010–11, when Dimitar Berbatov and Carlos Tevez both scored 20 goals that season to tie for the award.', 'Harry Kane recorded the highest goals-to-games ratio to win the award, scoring 29 goals in 30 games in 2016–17 for a rate of 0.97.']   

def part_of_speech():
    global texts
    nlp = spacy.load('en_core_web_sm')
    for text in texts:
        doc = nlp(text)
        print(text)
        for ent in doc.ents:
            print(ent.text, ent.start_char, ent.end_char, ent.label_)
        print('\n')

def named_entity_checking():
    with open('input1.txt') as f:
        content = f.readlines()
    content = [x.strip()[8:len(x) - 2] for x in content]
    nlp = spacy.load('en')
    relationships = []

    for i in range(len(content)):
        raw_content = content[i]
        arr = content[i].split(';')
        beg = nlp(arr[0])
        mid = nlp(arr[1])
        end = nlp(arr[2])
        if len(beg.ents) >= 1 and len(mid.ents) == 0 and len(end.ents) >= 1:
            relationships.append(raw_content)
    
    with open('output_test2.txt', 'w') as f:
        for line in relationships:
            f.write(line)
            f.write('\n')

        



def test():
    text = 'Bill is cool. He has a brother named Spot, who is a fast runner.'
    nlp = spacy.load('en_coref_md')
    doc = nlp(text)
    print(text)
    print(doc._.coref_resolved)



def resolve_coref():
    nlp = spacy.load('en_coref_md')
    with open('wiki_00') as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    lines = []
    for x in content:
        if x != '' and x != '</doc>' and x[0:4] != '<doc':
            lines.append(x)
            lines.append(' ')
    bigString = ''.join(lines)
    with open('output_no_coref.txt', 'w') as f:
        f.write(bigString)
    doc = nlp(bigString)

    if doc._.has_coref:
        with open('output_coref.txt', 'w') as f:
            f.write(doc._.coref_resolved)
    
    return doc
    
    # lines = [nlp(x) for x in content]
    # for i in range(len(lines)):
    #     if lines[i]._.has_coref:
    #         lines[i] = lines[i]._.coref_resolved
    
    # with open('output.txt', 'w') as f:
    #     for line in lines:
    #         f.write(line)

def post_process_spacy():
    text = ""
    """
    split the text to make a list of sentences
    iterate through the list
    in each iteration:
        if it's the first sentence:
            save the first nobj and all compounds prior to it as replace_nobj
            save the first dobj and all compounds as replace_dobj
        else: (not first sentence)
            if nobj is not a pronoun:
                save new nobj as replace_nobj
            else (it is a pronoun):
                replace nobj (which is a pronoun) with replace_nobj
            
            if dobj is not a pronoun:
                save new dobj as replace_dobj
            else (it is a pronoun):
                replace dobj (which is a pronoun) with replace_dobj
        write new sentence to file that we will run through OpenIE
    
    run the document through OpenIE
    *Not sure OpenIE 
    
    """
def resolve_coref_ours():
    text = """Bob Johnson swims well for UT. He is their fastest athelete."""
    nlp = spacy.load('en_coref_md')
    doc = nlp(text)
    coref = doc._.coref_resolved
    coref_doc = nlp(coref)
    
    for token in coref_doc:
        print(token.text, token.dep_)
    

def main():
    resolve_coref_ours()


if __name__ == '__main__':
    main()