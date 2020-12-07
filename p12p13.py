import spacy
import plwn

nlp = spacy.load("pl_spacy_model_morfeusz")
wn = plwn.load_default()

txt = "Fragment kuli tkwi do dzisiaj w murach zamku (nad kominkiem refektarza letniego)."
doc = nlp(txt)
txt2 = "Kurtka zapina się na pionowy, pociągnięty przez środek zamek błyskawiczny."
doc2 = nlp(txt2)

ranking = [] # ranking odległości
ranking2 = []
lexems = wn.lexical_units("zamek") # pobieranie jednostek leksykalnych dla formy "zamek"
for i, lex in enumerate(lexems): # dla każdej jednostki (sensu)
  pos = lex.pos # znacznik części mowy
  variant = lex.variant # numer wariantu
  unit = wn.lexical_unit('zamek', pos, variant) 
  gloss =  lex.definition # wytłumaczenie/definicja danego sensu
  print(i+1, "zamek: ", gloss)
  gloss_doc = nlp(gloss)
  dist = doc.similarity(gloss_doc)
  dist2 = doc2.similarity(gloss_doc)
  ranking.append((dist, gloss))
  ranking2.append((dist2, gloss))

sorted_ranking = sorted(ranking, reverse=True) # sortowanie rankingu wedle podobieństwa
sorted_ranking2 = sorted(ranking2, reverse=True)
print("\n Wzór 1:", doc, "\n")
for place in sorted_ranking[:3]:
  print(place) # pierwsze miejsce uznajemy za najlepsze

print("\n Wzór 2:", doc2, "\n")
for place in sorted_ranking2[:3]:
  print(place)

"""
Wzór 1: Fragment kuli tkwi do dzisiaj w murach zamku (nad kominkiem refektarza letniego). 

(0.7939603211724038, 'warowna budowla mieszkalna, rezydencja pana, króla, księcia lub magnata.')
(0.7774556566820001, 'mechanizm broni palnej służący do zamykania na czas wystrzału i otwierania po strzale tylnej części lufy.')
(0.7408859653636716, 'zagranie taktyczne w hokeju; zamknięcie przeciwnika w jego tercji lodowiska/boiska.')

Wzór 2: Kurtka zapina się na pionowy, pociągnięty przez środek zamek błyskawiczny. 

(0.8928199834155998, 'zapięcie przy ubraniu, suwak, ekler.')
(0.8092869844318508, 'mechanizm broni palnej służący do zamykania na czas wystrzału i otwierania po strzale tylnej części lufy.')
(0.7991736001585494, 'mechanizm lub urządzenie do zamykania drzwi, szuflad, walizek.')
"""


lexeme = wn.lexical_unit("palić", pos="verb", variant=1)
print("Domena: ", lexeme.domain)
#Domena:  Domain.cwytw
print("Anotacja wydźwięku: ", lexeme.emotion_markedness.name)
#Anotacja wydźwięku:  weak_negative
for relation, correlate in lexeme.related_pairs():
  print("Relacja: {}, korelat: {}".format(relation.name, correlate.lemma))
#Relacja: synonimia międzyparadygmatyczna V-N, korelat: palenie
#Relacja: aspektowość czysta, korelat: przypalić
#Relacja: aspektowość czysta, korelat: wypalić
#Relacja: kolokacyjność, korelat: gafa



lexeme = wn.lexical_unit("jedzenie", pos="noun", variant=1)
synonyms = lexeme.synset.lexical_units
for s in synonyms:
  print("Dieta reguluje nasze {}.".format(s.lemma))
#Dieta reguluje nasze jedzenie.
#Dieta reguluje nasze spożywanie.
#Dieta reguluje nasze zjadanie.
#Dieta reguluje nasze konsumowanie.
#Dieta reguluje nasze posilanie się.
#Dieta reguluje nasze pożywianie się.


