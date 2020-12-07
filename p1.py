import morfeusz2
morf = morfeusz2.Morfeusz()


for analysis in morf.analyse("Nornica prowadzi zmierzchowo-nocny tryb życia, ale wychodzi również za dnia w poszukiwaniu pokarmu."):
  # na wyjściu z morf.analyse dostajemy listę interpretacji, niektóre tokeny mogą mieć więcej niż jedną interpretację, jak tu z tokenem "życia"
  start_ind, end_ind, interp = analysis
  form, lemma, tag, qualifiers, _ = interp
  try:
    pos, feats = tag.split(":", 1)
  except ValueError: # podana forma nie ma cech morfosyntaktycznych
    pos, feats = tag, ""
  print("{0:4} {1:4} {2:8} {3:8} {4:6} {5:20} {6:15}".format(start_ind, end_ind, form, lemma, pos, feats, str(qualifiers)))

"""
start end forma    lemat    POS    cechy morfologiczne  kwalifikatory
==============================================================================
   0    1 Nornica  nornica  subst  sg:nom:f             ['nazwa_pospolita']
   1    2 prowadzi prowadzić fin    sg:ter:imperf        []             
   2    3 zmierzchowo zmierzchowy adja                        []             
   3    4 -        -        interp                      []             
   4    5 nocny    nocny    adj    sg:acc:m3:pos        []             
   4    5 nocny    nocny    adj    sg:nom.voc:m1.m2.m3:pos [] # notacja kropkowa oznacza że dana forma może podpadać pod każdy z podanych przypadków (mianownik, biernik, wołacz)            
   5    6 tryb     tryb     subst  sg:nom.acc:m3        ['nazwa_pospolita']
   5    6 tryb     tryba    subst  pl:gen:f             ['nazwa_pospolita']
   5    6 tryb     trybić   impt   sg:sec:imperf        []             
   6    7 życia    życie    subst  sg:gen:n:ncol        ['nazwa_pospolita']
   6    7 życia    życie    subst  pl:nom.acc.voc:n:ncol ['nazwa_pospolita']
   6    7 życia    żyć      ger    pl:nom.acc:n:imperf:aff []             
   6    7 życia    żyć      ger    sg:gen:n:imperf:aff  []             
   7    8 ,        ,        interp                      []             
   8    9 ale      ale:j    conj                        []             
   8    9 ale      ale:q    part                        []             
   8    9 ale      ale:i    interj                      []             
   9   10 wychodzi wychodzić:v2 fin    sg:ter:perf          [] # v1 i v2 to różne leksemy, podpadające pod ten sam lemat
   9   10 wychodzi wychodzić:v1 fin    sg:ter:imperf        []             
  10   11 również  również  part                        []             
  11   12 za       za:q     part                        []             
  11   12 za       za:p     prep   acc                  []             
  11   12 za       za:p     prep   gen                  []             
  11   12 za       za:p     prep   inst                 []             
  12   13 dnia     dzień:s1 subst  sg:gen:m3            ['nazwa_pospolita']
  13   14 w        w        prep   acc:nwok             []             
  13   14 w        w        prep   loc:nwok             []             
  14   15 poszukiwaniu poszukiwanie subst  sg:dat:n:ncol        ['nazwa_pospolita']
  14   15 poszukiwaniu poszukiwanie subst  sg:loc:n:ncol        ['nazwa_pospolita']
  14   15 poszukiwaniu poszukiwać ger    sg:dat.loc:n:imperf:aff []             
  15   16 pokarmu  pokarm   subst  sg:gen:m3            ['nazwa_pospolita']
  16   17 .        .        interp                      []             

"""

for proposal in morf.generate("drzewo"):
  form, lemma, tag, qualifiers, _ = proposal
  try:
    pos, feats = tag.split(":", 1)
  except ValueError: # podana forma nie ma cech morfosyntaktycznych
    pos, feats = tag, ""
  print("{0:8} {1:8} {2:6} {3:20} {4:15}".format(form, lemma, pos, feats, str(qualifiers)))

"""
forma    lemat    POS    cechy morfologiczne  kwalifikatory
==============================================================================
drzewo   drzewo   subst  sg:nom.acc.voc:n:ncol ['nazwa_pospolita']
drzewa   drzewo   subst  sg:gen:n:ncol        ['nazwa_pospolita']
drzewu   drzewo   subst  sg:dat:n:ncol        ['nazwa_pospolita']
drzewem  drzewo   subst  sg:inst:n:ncol       ['nazwa_pospolita']
drzewie  drzewo   subst  sg:loc:n:ncol        ['nazwa_pospolita']
drzewa   drzewo   subst  pl:nom.acc.voc:n:ncol ['nazwa_pospolita']
drzew    drzewo   subst  pl:gen:n:ncol        ['nazwa_pospolita']
drzewom  drzewo   subst  pl:dat:n:ncol        ['nazwa_pospolita']
drzewami drzewo   subst  pl:inst:n:ncol       ['nazwa_pospolita']
drzewach drzewo   subst  pl:loc:n:ncol        ['nazwa_pospolita']
"""
