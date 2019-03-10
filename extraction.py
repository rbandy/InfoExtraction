import spacy
#from spacy.matcher import PhraseMatcher
import application

#nlp = spacy.load('en_core_web_sm')


#text = (u"Bill, Mark, and Fred are cool. He has a sister named Sally May, who is a fast runner.")
#text = "Izzy is a dog. He likes to run. Spike is a cat. He likes to scratch."

def resolve_coref(text, nlp):
    """
    Sliding window solution resolving coreferences. Without the sliding window,
    neuralcoref will reslove everything to the first subject/object instead of the most recent.
    """
    sentences = text.split(".")
    new_text = [sentences[0].lstrip()]
    for i in range(1,len(sentences)):
        s1 = sentences[i-1]
        s2 = sentences[i]
        window = s1 + "." + s2
        doc = nlp(window)
        coref = doc._.coref_resolved
        if doc._.has_coref:
            new_text.append((coref.split("."))[1].lstrip())
        else:
            new_text.append(s2)

    text = ".".join(new_text)
    return text

#text = resolve_coref(text)
#print(text)
#doc = nlp(text)

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
            verb += [str(token)]
        # token.pos_ != "SPACE" and token.pos_ != "DET" and token.text != '.' and 
        #  or token.text == ',' or token.pos_ == "CCONJ"
        elif len(verb) == 0 and len(obj) == 0 and (token.pos_ == "PROPN" or token.pos_ == "PRON"\
         or token.pos_ == "NOUN" or token.text == ',' or token.pos_ == "CCONJ"):
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

        #elif token.pos_ != "DET":
        else:
            obj += [str(token)]

    return triples

def compute_confidence(doc, verb_triples, entity_triples):
    matches = verb_triples & entity_triples
    print(matches)

def main():
    nlp = spacy.load('en_coref_md')
    text = application.wiki_to_string()
    #text = "Izzy is a dog. He likes to run. Spike is a cat. He likes scratch."
    text = resolve_coref(text, nlp)
    print(text)
    doc = nlp(text)

    verb_triples = relation_by_verb(doc)
    print("verb", verb_triples)
    print(len(verb_triples))

    entity_triples = application.process_spacy(text, nlp)
    print("entity",entity_triples)
    print(len(entity_triples))

    compute_confidence(doc, verb_triples, entity_triples)

if __name__ == '__main__':
    main()
