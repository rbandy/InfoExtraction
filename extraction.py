import spacy
#from spacy.matcher import PhraseMatcher
import application
from difflib import SequenceMatcher
import csv

#nlp = spacy.load('en_core_web_sm')


#text = (u"Bill, Mark, and Fred are cool. He has a sister named Sally May, who is a fast runner.")
#text = "Izzy is a dog. He likes to run. Spike is a cat. He likes to scratch."

def resolve_coref(text, nlp):
    """
    Sliding window solution resolving coreferences. Without the sliding window,
    neuralcoref will reslove everything to the first subject/object instead of the most recent.
    """
    sentences = text.split(". ")
    new_text = [sentences[0].lstrip()]
    for i in range(1,len(sentences)):
        s1 = sentences[i-1]
        s2 = sentences[i]
        window = s1 + ". " + s2
        doc = nlp(window)
        coref = doc._.coref_resolved
        if doc._.has_coref:
            #print(window,coref)
            try:
                new_text.append((coref.split(". "))[1].lstrip())
            except IndexError:
                # replaced token and "." with named entity == bad
                new_text.append(s2)
        else:
            new_text.append(s2)

    text = ".".join(new_text)
    f = open("nba_coref.txt", "w")
    f.write(text)
    return text

#text = resolve_coref(text)
#print(text)
#doc = nlp(text)

def relation_by_verb(text, nlp):
    triples = set()

    sentences = text.split(".")

    for sentence in sentences:
        sub = []
        obj = []
        verb = []
        doc = nlp(sentence)
        for token in doc:
            #print(token.text, "lemma", token.lemma_, "pos", token.pos_, "dep", token.dep_)
            #if token.dep_ == "nsubj" or token.dep_ == "conj" or token.dep_ == "nsubjpass":

            if len(obj) == 0  and (token.pos_ == "VERB" or (token.pos_ == "ADP" and len(verb) > 0)):
            	#verb += [str(token.lemma_)]
                verb += [str(token)]
            # token.pos_ != "SPACE" and token.pos_ != "DET" and token.text != '.' and 
            #  or token.text == ',' or token.pos_ == "CCONJ"
            elif len(verb) == 0 and len(obj) == 0 and (token.pos_ == "PROPN" \
                or token.pos_ == "PRON" or token.pos_ == "NOUN"):
                sub += [str(token)]

            elif token.pos_ == "PUNCT":
                if len(sub) > 0 and len(obj) > 0 and len(verb) > 0:
                    t = (" ".join(sub), " ".join(verb), " ".join(obj))
                    triples.add(t)
                    #print()
                    #print(t)
                    #print()
                sub = []
                obj = []
                verb = []
                #if token.pos_ != "ADJ":
                #    sub = []

            #elif token.pos_ != "DET":
            else:
                obj += [str(token)]

        if len(sub) > 0 and len(obj) > 0 and len(verb) > 0:
            t = (" ".join(sub), " ".join(verb), " ".join(obj))
            triples.add(t)

    return triples

def extract_openie_triples(filename):
    triples = set()
    with open(filename, mode='r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=";")
        for row in csv_reader:
            row[0] = (row[0].split('('))[1].strip()
            row[1] = row[1].strip()
            row[-1] = (row[-1].split(')'))[0].strip()
            triples.add(tuple(row))
    return triples

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def compute_confidence(text, nlp, verb_triples, entity_triples, openie_triples, writer):
    confidences = []

    # triples in either but not both sets
    all_triples = verb_triples ^ entity_triples ^ openie_triples
    for triple in all_triples:
        score = 0.0
        # some bad triples from openie contained '.'
        if '.' not in triple:
            sub = nlp(triple[0])
            
            for token in sub:
                if token.ent_type_ == "PERSON":
                    score += 0.1/len(sub)
            

            rel = triple[1]
            obj = nlp(triple[2])
            for token in obj:
                if token.ent_type_ == "PERSON" or token.ent_type_ == "NORP" \
                or token.ent_type_ == "FAC" or token.ent_type_ == "ORG" or token.ent_type_ == "GPE":
                    score += 0.1/len(obj)

            # max_sim = 0.0
            # for t in all_triples:
            #     if t != triple:
            #         s = similar(str(t), str(triple))
            #         max_sim = max(max_sim, s)
            
            score += max_sim*0.6
            if score >= 0.5:
                writer.writerow(triple + (score,))
                confidences.append(triple + (score,))
            #print(triple + (score,))

    # triples in both sets
    exact_matches = (verb_triples & entity_triples) | (verb_triples & openie_triples) | (openie_triples & entity_triples)
    print("num exact matches:", len(exact_matches))
    for triple in exact_matches:
        score = 0.0
        sub = nlp(triple[0])
        for token in sub:
            if token.ent_type_ == "PERSON":
                score += 0.2/len(sub)

        obj = nlp(triple[2])
        for token in obj:
            if token.ent_type_ == "PERSON" or token.ent_type_ == "NORP" \
            or token.ent_type_ == "FAC" or token.ent_type_ == "ORG" or token.ent_type_ == "GPE":
                score += 0.2/len(obj)

        # similarity = 1 for exact matches
        score += 0.6
        writer.writerow(triple + (score,))
        confidences.append(triple + (score,))
        #print(triple + (score,))

    return confidences

def main():
    nlp = spacy.load('en_coref_md')
    file = open("nba_coref.txt", 'r')
    text = file.read()

    verb_triples = relation_by_verb(text, nlp)
    #print("verb", verb_triples)
    #print(len(verb_triples))

    entity_triples = application.process_spacy(text, nlp)
    #print("entity",entity_triples)
    #print(len(entity_triples))

    #openie_triples = extract_openie_triples("openie_output.csv")
    openie_triples = set()
    #print("openie",openie_triples)
    #print(len(openie_triples))

    with open('triples.csv', 'w') as f:
        writer = csv.writer(f , lineterminator='\n')
        header = ("entity1", "relation", "entity2", "score")

        c = compute_confidence(text, nlp, verb_triples, entity_triples, openie_triples, writer)

    # with open('triples.csv', 'w') as f:
    #     writer = csv.writer(f , lineterminator='\n')
    #     header = ("entity1", "relation", "entity2", "score")
    #     writer.writerow(header)
    #     for tup in c:
    #         writer.writerow(tup)
        f.close()

if __name__ == '__main__':
    main()
