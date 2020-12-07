import requests
import os
import spacy
from itertools import product
from bs4 import BeautifulSoup

nlp = spacy.load("pl_spacy_model_morfeusz")

# reguły są jednopoziomowe
# notacja dla reguł ma postać rodzic(dziecko+dziecko+...)

rules = {
  "SV" : "ROOT(nsubj)",
  "SVO" : "ROOT(nsubj+obj)",
  "SVObl" : "ROOT(nsubj+obl)",
  "SVOO" : "ROOT(nsubj+obj+obl)",
  "COP" : "ROOT(nsubj+cop)"
}

def process_rule(rule):
  # podział reguły na rodzica i dzieci
  head = ""
  tail = None
  ind = 0
  while ind < len(rule) and rule[ind] != "(":
    head += rule[ind]
    ind += 1
  tail = rule[ind:]
  tail = tail.strip("()")
  return head, tail

def prune_dep(dep, strict):
  # obcinanie specyficznych dla języka kwalifikatorów relacji
  if strict:
    return dep
  else:
    return dep.split(":", 1)[0]

def process_tree(toks, rule, strict = False):
  # wyszukiwanie dopasowań do reguły w drzewie
  rule_head, rule_tail = process_rule(rule)
  rule_head = prune_dep(rule_head, strict)
  tail_deps = [prune_dep(dep, strict) for dep in rule_tail.split("+")]
  matches = []
  for tok in toks:
    if prune_dep(tok.dep_, strict) == rule_head: # token pasuje do rodzica z reguły
      match = (tok, tok.dep_)
      match_dic = {dep: [] for dep in tail_deps}
      children = tok.children
      for child in children:
        if prune_dep(child.dep_, strict) in match_dic: # dziecko pasuje do reguły
          match_dic[prune_dep(child.dep_, strict)].append((child, child.dep_))
      # znajdowanie wszystkich możliwych kombinacji dopasowań do reguły
      combinations = list(product([match], *[v for k, v in match_dic.items()]))
      sorted_combinations = [sorted(c, key = lambda c:c[0].i) for c in combinations]
      matches.extend(sorted_combinations)
  return matches

def lemmatize_matches(sent_matches):
  # lematyzacja dopasowań
  lemmatized_matches = []
  for match in sent_matches:
    lemmatized_match = [] 
    for tok in match:
      lemmatized_match.append((tok[0].lemma_, tok[1]))
    lemmatized_matches.append(tuple(lemmatized_match))
  return lemmatized_matches


# Pobieranie artykułu z wikipedii
url = "https://pl.wikipedia.org/wiki/Lew_afryka%C5%84ski"
page = requests.get(url)
soup = BeautifulSoup(page.content, "html.parser")
paragraphs = soup.find_all("p") # paragrafy mają znacznik html <p>
paragraph_texts = [p.text for p in paragraphs if p.text != ""]
full_text = "\n".join(paragraph_texts)
doc = nlp(full_text)

for rule in [rules["COP"], rules["SVO"], rules["SVObl"]]:
  for s in doc.sents:
    matches = process_tree(s, rule)
    lemmatized = lemmatize_matches(matches)
    if lemmatized != []:
      for match in lemmatized:
        if ("lew", "nsubj") in match:
          print(match)

"""
(('lew', 'nsubj'), ('być', 'cop'), ('mięsożerca', 'ROOT'))
(('lew', 'nsubj'), ('stać', 'cop'), ('atrakcja', 'ROOT'))
(('lew', 'nsubj'), ('być', 'cop'), ('symbol', 'ROOT'))
(('lew', 'nsubj'), ('zamieszkiwać', 'ROOT'), ('Afryka', 'obj'))
(('lew', 'nsubj'), ('zasięg', 'obj'), ('obejmować', 'ROOT'))
(('lew', 'nsubj'), ('obejmować', 'ROOT'), ('teren', 'obj'))
(('lew', 'nsubj'), ('obejmować', 'ROOT'), ('część', 'obj'))
(('lew', 'nsubj'), ('mieć', 'ROOT'), ('grzywy[13][22', 'obj'))
(('lew', 'nsubj'), ('oddalać', 'ROOT'), ('czas', 'obj'))
(('lew', 'nsubj'), ('używać', 'ROOT'), ('technika', 'obj'))
(('lew', 'nsubj'), ('kierować', 'ROOT'), ('zdobycz', 'obj'))
(('lew', 'nsubj'), ('odbierać', 'ROOT'), ('zdobycz', 'obj'))
(('lew', 'nsubj'), ('atakować', 'ROOT'), ('czas', 'obj'))
(('lew', 'nsubj'), ('atakować', 'ROOT'), ('zwierzę', 'obj'))
(('lew', 'nsubj'), ('zabić', 'ROOT'), ('560', 'obj'))
(('lew', 'nsubj'), ('pojawić', 'ROOT'), ('plejstocen', 'obl:arg'))
(('lew', 'nsubj'), ('adaptować', 'ROOT'), ('środowisko', 'obl'))
(('lew', 'nsubj'), ('mieć', 'ROOT'), ('19', 'obl'))
(('lew', 'nsubj'), ('żyć', 'ROOT'), ('grupa', 'obl:arg'))
(('lew', 'nsubj'), ('samka', 'obl'), ('oddalać', 'ROOT'))
(('zależność', 'obl'), ('lew', 'nsubj'), ('używać', 'ROOT'))
(('lew', 'nsubj'), ('rozmnażać', 'ROOT'), ('rok', 'obl'))
(('lew', 'nsubj'), ('napadać', 'ROOT'), ('inwentarz', 'obl:arg'))
(('obszar', 'obl'), ('lew', 'nsubj'), ('zabić', 'ROOT'))
(('lew', 'nsubj'), ('zabić', 'ROOT'), (']', 'obl'))
(('Tanzania', 'obl'), ('lew', 'nsubj'), ('zabić', 'ROOT'))
(('lew', 'nsubj'), ('chorować', 'ROOT'), ('gruźlica', 'obl:arg'))
(('lew', 'nsubj'), ('różnić', 'ROOT'), ('afrykański', 'obl:arg'))
(('książka', 'obl'), ('lew', 'nsubj'), ('występować', 'ROOT'))
(('lew', 'nsubj'), ('występować', 'ROOT'), ('władca', 'obl:arg'))
(('lew', 'nsubj'), ('pojawiać', 'ROOT'), ('herb', 'obl:arg'))
"""
