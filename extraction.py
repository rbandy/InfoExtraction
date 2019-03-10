import spacy
#from spacy.matcher import PhraseMatcher
from application import wiki_to_string

nlp = spacy.load('en_core_web_sm')

# copied from wiki USMNT
#text = (u"The United States Men's National Soccer Team (USMNT) is controlled by the United States Soccer Federation and competes in the Confederation of North, Central American and Caribbean Association Football. The team has appeared in ten FIFA World Cups, including the first in 1930, where they reached the semi-finals. The U.S. participated in the 1934 and 1950 World Cups, winning 1–0 against England in the latter. After 1950, the U.S. did not qualify for the World Cup until 1990. The U.S. hosted the 1994 World Cup, where they lost to Brazil in the round of sixteen. They qualified for five more consecutive World Cups after 1994 (for a total of seven straight appearances, a feat shared with only seven other nations),[10] becoming one of the tournament's regular competitors and often advancing to the knockout stage. The U.S. reached the quarter-finals of the 2002 World Cup, where they lost to Germany. In the 2009 Confederations Cup, they eliminated top-ranked Spain in the semi-finals before losing to Brazil in the final, their only appearance in the final of a major intercontinental tournament. The team failed to qualify for the 2018 World Cup, having been eliminated in continental qualifying, ending the streak of consecutive World Cups at seven. United States will co-host the 2026 FIFA World Cup along with Canada and Mexico, the automatic qualification on all three teams is likely as co-hosts.\n\nThe U.S. also competes in continental tournaments, including the CONCACAF Gold Cup and Copa América. The U.S. has hosted fourteen editions of the Gold Cup, winning six, and has achieved a fourth-place finish in two Copa Américas, including the 2016 edition that they hosted. The team's head coach is Gregg Berhalter, since November 29, 2018. Earnie Stewart is the team's General Manager since August 1, 2018.")
#text = (u"The United States Men's National Soccer Team (USMNT) is controlled by the United States Soccer Federation and competes in the Confederation of North, Central American and Caribbean Association Football.")
text = (u"Bill, Mark, and Kate are cool. He has a sister named Sally May, who is a fast runner.")
#text = wiki_to_string()
#text = "Premier League Player of the Month\n\nThe Premier League Player of the Month is an association football award that recognises the best adjudged Premier League player each month of the season. The winner is chosen by a combination of an online public vote, which contributes to 10% of the final tally, a panel of experts, and the captain of each Premier League club. It has been called the Carling Premiership Player of the Month (1994–2001), the Barclaycard Premiership Player of the Month (2001–2004) and the Barclays Player of the Month (2004–2016); it is currently known as the EA Sports Player of the Month."
doc = nlp(text)

triples = []
sub = []
obj = []
verb = []

#i = 0
for token in doc:
    print(token.text, "lemma", token.lemma_, "pos", token.pos_, "dep", token.dep_)
    #if token.dep_ == "nsubj" or token.dep_ == "conj" or token.dep_ == "nsubjpass":

    #if (token.pos_ == "VERB" or token.pos_ == "ADP") and len(obj) == 0:
    if (token.pos_ == "VERB") and len(obj) == 0:
    	#verb += [str(token.lemma_)]
        verb += [str(token)]
    elif len(verb) == 0 and len(obj) == 0 and token.pos_ != "SPACE" and token.pos_ != "DET" and token.text != '.':
        sub += [str(token)]
    #elif token.dep_ == "compound" or token.dep_ == "dobj" or token.dep_ == "pobj" \
    #or token.dep_ == "amod" or token.dep_ == "acomp" or token.dep_ == "attr" or token.dep_ == "advmod":
    #    obj += [str(token)]

    elif token.pos_ == "PUNCT" or token.pos_ == "SPACE" or token.dep_ == "nsubj":
        if len(sub) > 0 and len(obj) > 0 and len(verb) > 0:
            t = (" ".join(sub), " ".join(verb), " ".join(obj))
            triples.append(t)
            print(t)
        #sub = []
        obj = []
        verb = []
        if token.pos_ != "ADJ":
            sub = []

    elif token.pos_ != "DET":
        obj += [str(token)]
    #i += 1
    #if i > 40:
    #    break

#print("triples",triples)

    	

# extract named entities
for entity in doc.ents:
	print(entity.text, entity.label_)

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
