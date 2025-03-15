from openie import StanfordOpenIE

text = "Hawaii is a state in the United States. Barack Obama served as the 44th president of the United States. The Louvre Museum is located in Paris, France."

with StanfordOpenIE('openie.affinity_probability_cap') as client:
    triples = client.annotate(text)
    for triple in triples:
        print(triple)