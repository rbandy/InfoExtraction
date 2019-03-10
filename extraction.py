import spacy
#from spacy.matcher import PhraseMatcher
import application

#nlp = spacy.load('en_core_web_sm')
nlp = spacy.load('en_coref_md')

#text = (u"Bill, Mark, and Fred are cool. He has a sister named Sally May, who is a fast runner.")
#text = "Izzy is a dog. He likes to run. Spike is a cat. He likes to scratch."
#text = application.wiki_to_string()
text = "Premier League Player of the Month\n\nThe Premier League Player of the Month is an association football award that recognises the best adjudged Premier League player each month of the season. The winner is chosen by a combination of an online public vote, which contributes to 10% of the final tally, a panel of experts, and the captain of each Premier League club. It has been called the Carling Premiership Player of the Month (1994–2001), the Barclaycard Premiership Player of the Month (2001–2004) and the Barclays Player of the Month (2004–2016); it is currently known as the EA Sports Player of the Month."

def resolve_coref(text):
    sentences = text.split(".")
    print("sentences\n", sentences, "\n")
    new_text = [sentences[0]]
    for i in range(1,len(sentences)):
        s1 = sentences[i-1]
        s2 = sentences[i]
        window = s1 + "." + s2
        print("window:", window)
        doc = nlp(window)
        coref = doc._.coref_resolved
        print(coref)
        if doc._.has_coref:
            new_text.append((coref.split("."))[1])
        else:
            new_text.append(s2)

    text = ".".join(new_text)
    return text

text = resolve_coref(text)
print(text)
doc = nlp(text)

def relation_by_verb(doc):
    triples = set()
    sub = []
    obj = []
    verb = []

    for token in doc:
        #print(token.text, "lemma", token.lemma_, "pos", token.pos_, "dep", token.dep_)
        #if token.dep_ == "nsubj" or token.dep_ == "conj" or token.dep_ == "nsubjpass":

        #if (token.pos_ == "VERB" or token.pos_ == "ADP") and len(obj) == 0:
        if (token.pos_ == "VERB") and len(obj) == 0:
        	#verb += [str(token.lemma_)]
            print(str(token))
            verb += [str(token)]
        # token.pos_ != "SPACE" and token.pos_ != "DET" and token.text != '.' and 
        elif len(verb) == 0 and len(obj) == 0 and (token.pos_ == "PROPN" or token.pos_ == "PRON"\
         or token.pos_ == "NOUN" or token.text == ',' or token.pos_ == "CCONJ"):
            print(str(token))
            sub += [str(token)]
        #elif token.dep_ == "compound" or token.dep_ == "dobj" or token.dep_ == "pobj" \
        #or token.dep_ == "amod" or token.dep_ == "acomp" or token.dep_ == "attr" or token.dep_ == "advmod":
        #    obj += [str(token)]

        #elif token.pos_ == "PUNCT" or token.pos_ == "SPACE" or token.dep_ == "nsubj":
        elif token.pos_ == "PUNCT" or token.dep_ == "nsubj":
            if len(sub) > 0 and len(obj) > 0 and len(verb) > 0:
                t = (" ".join(sub), " ".join(verb), " ".join(obj))
                triples.add(t)
                #print()
                #print(t)
                #print()
            #sub = []
            obj = []
            verb = []
            if token.pos_ != "ADJ":
                sub = []

        elif token.pos_ != "DET":
            print("OBJ:", str(token))
            obj += [str(token)]

    return triples

#verb_triples = relation_by_verb(doc)
#print(verb_triples)
#print(len(verb_triples))

#entity_triples = application.process_spacy()
#print(entity_triples)
#print(len(entity_triples))

def compute_confidence(doc, verb_triples, entity_triples):
    matches = verb_triples & entity_triples
    print(matches)

#compute_confidence(doc, verb_triples, entity_triples)
    	

# extract named entities
#for entity in doc.ents:
#	print(entity.text, entity.label_)

"""
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
"""
