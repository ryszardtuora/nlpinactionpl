# nlpinactionpl
Kod do przykładów dla posłowia

Po pobraniu repozytorium, należy zainstalować wymagane zależności
`python3 -m pip install -r nlpinactionpl/requirements.txt`

Poza requirements.txt, dla niektórych skryptów konieczna jest instalacja Morfeusza http://morfeusz.sgjp.pl), oraz API do Słowosieci (należy skontaktować się z twórcami poprzez http://plwordnet.pwr.wroc.pl/wordnet/), oraz modelu do spaCy dla języka polskiego(http://zil.ipipan.waw.pl/SpacyPL).

Skrypty uruchamiamy komendą python3 np:
`python3 nlpinactionpl/p9p10p11.py`

Polecamy uruchomienie skryptów w środowisku Google Colab, przy pomocy załączonego notatnika `notebook.ipynb`, pozwala to na łatwiejszą konfigurację zależności, oraz skorzystanie z GPU, co znacznie przyspieszy trening BERTa.

