from rdflib import Graph, Literal
import pandas as pd

g = Graph()
g.parse("countrues_info.ttl", format="turtle")

def find_pred(name):
    for _, p, _ in g:
        if name.lower() in str(p).lower():
            return p
    return None

pop_p = find_pred("population")
cont_p = find_pred("continent")
label_p = find_pred("prefLabel") or find_pred("name")

def get_label(res):
    for _, _, l in g.triples((res, label_p, None)):
        if isinstance(l, Literal):
            return str(l)
    return str(res)

rows = []
for s, _, pop in g.triples((None, pop_p, None)):
    try:
        pop_val = int(str(pop))
    except ValueError:
        continue
    for _, _, cont in g.triples((s, cont_p, None)):
        rows.append({
            "continent": get_label(cont),
            "country": get_label(s),
            "population": pop_val
        })

df = pd.DataFrame(rows)
if df.empty:
    print("Даних не знайдено.")
    exit()

top5 = (
    df.sort_values(["continent", "population"], ascending=[True, False])
      .groupby("continent")
      .head(5)
)

for cont, grp in top5.groupby("continent"):
    print(f"\n {cont}")
    for i, row in enumerate(grp.itertuples(index=False), 1):
        print(f"  {i}. Країна: {row.country} Населення: {row.population:,}")
