from SPARQLWrapper import SPARQLWrapper, JSON
import ssl

ssl._create_default_https_context = ssl._create_unverified_context
sparql = SPARQLWrapper('https://dbpedia.org/sparql')

query = '''
SELECT DISTINCT ?company ?name ?employees
WHERE {
  ?company a dbo:Company ;
           dct:subject dbc:Software_companies_of_Ukraine .

  OPTIONAL { ?company foaf:name ?name . }
  OPTIONAL { ?company dbo:numberOfEmployees ?employees . }
}
ORDER BY DESC(?employees)
LIMIT 50
'''

sparql.setQuery(query)
sparql.setReturnFormat(JSON)
query_res = sparql.query().convert()

print("Software-компанії України (впорядковано за кількістю співробітників):")
for i, row in enumerate(query_res["results"]["bindings"], 1):
    name = row["name"]["value"] if "name" in row else row["company"]["value"]
    employees = row["employees"]["value"] if "employees" in row else "Невідомо"
    print(f"{i}. {name} — {employees} співробітників")
