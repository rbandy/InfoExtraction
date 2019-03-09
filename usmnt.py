import spacy
from spacy.matcher import PhraseMatcher

nlp = spacy.load('en_core_web_sm')

# copied from wiki USMNT
#text = (u"The United States Men's National Soccer Team (USMNT) is controlled by the United States Soccer Federation and competes in the Confederation of North, Central American and Caribbean Association Football. The team has appeared in ten FIFA World Cups, including the first in 1930, where they reached the semi-finals. The U.S. participated in the 1934 and 1950 World Cups, winning 1–0 against England in the latter. After 1950, the U.S. did not qualify for the World Cup until 1990. The U.S. hosted the 1994 World Cup, where they lost to Brazil in the round of sixteen. They qualified for five more consecutive World Cups after 1994 (for a total of seven straight appearances, a feat shared with only seven other nations),[10] becoming one of the tournament's regular competitors and often advancing to the knockout stage. The U.S. reached the quarter-finals of the 2002 World Cup, where they lost to Germany. In the 2009 Confederations Cup, they eliminated top-ranked Spain in the semi-finals before losing to Brazil in the final, their only appearance in the final of a major intercontinental tournament. The team failed to qualify for the 2018 World Cup, having been eliminated in continental qualifying, ending the streak of consecutive World Cups at seven. United States will co-host the 2026 FIFA World Cup along with Canada and Mexico, the automatic qualification on all three teams is likely as co-hosts.\n\nThe U.S. also competes in continental tournaments, including the CONCACAF Gold Cup and Copa América. The U.S. has hosted fourteen editions of the Gold Cup, winning six, and has achieved a fourth-place finish in two Copa Américas, including the 2016 edition that they hosted. The team's head coach is Gregg Berhalter, since November 29, 2018. Earnie Stewart is the team's General Manager since August 1, 2018.")
text = (u"The United States Men's National Soccer Team (USMNT) is controlled by the United States Soccer Federation and competes in the Confederation of North, Central American and Caribbean Association Football.")
doc = nlp(text)

# extract POS
for token in doc:
    print(token.text, token.lemma_, token.pos_, token.tag_,)

# extract named entities
for entity in doc.ents:
	print(entity.text, entity.label_)

# relationship extraction
#spacy.displacy.render(doc, style='dep', jupyter=True)

#matcher = PhraseMatcher(nlp.vocab)
#matcher.add('OBAMA', None, nlp(u"Barack Obama"))
#doc = nlp(u"Barack Obama lifts America one last time in emotional farewell")
#matches = matcher(doc)
#print(matches)
#m = matches[0]
#s = m[1]
#e = m[2]
#print(doc[s:e])