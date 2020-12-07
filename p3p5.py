import spacy

nlp = spacy.load("pl_spacy_model_morfeusz")
doc = nlp("W niedzielę otwarto lokale wyborcze.") # przepuszczanie stringa przez potok przetwarzania aby uzyskać obiekt Doc

for tok in doc:
  form, tag, upos = tok.orth_, tok.tag_, tok.pos_ # spaCy reprezentuje tagi przez liczby naturalne, aby zobaczyć wersję tekstową oznaczenia, należy dodać podkreślnik. W atrybucie .tag przechowywany jest tag w tagsecie NKJP, w atrybucie .pos jest zaś jego rzutowanie na tagset UD
  feats = tok._.feats # cechy morfosyntaktyczne są przechowywane w specjalnie dodanym atrybucie ._.feats
  print("{0:15} {1:8} {2:6} {3:15}".format(form, upos, tag, feats)) # wypisujemy interpretację morfosyntaktyczną każdego tokenu

"""
forma           UD-POS   NKJP   cechy morfologiczne
====================================================================
W               ADP      prep   acc:nwok       
niedzielę       NOUN     subst  sg:acc:f       
otwarto         VERB     imps   perf           
lokale          NOUN     subst  pl:acc:m3      
wyborcze        ADJ      adj    pl:acc:m3:pos  
.               PUNCT    interp                
"""

tok = nlp("jabłko")[0] # najlepiej jeśli argumentem do flexera będzie token, a nie sam string
flexer = nlp.get_pipe("flexer")
print("Nie zjadłem {}.".format(flexer.flex(tok, "gen")))
print("Przyglądam się {}.".format(flexer.flex(tok, "dat")))
print("Nie jedliśmy {}.".format(flexer.flex(tok, "gen:pl")))# jeśli chcemy zmienić dwie cechy naraz, należy podać je przedzielone dwukropkami

"""
Nie zjadłem jabłka
Przyglądam się jabłku
Nie jedliśmy jabłek
"""
