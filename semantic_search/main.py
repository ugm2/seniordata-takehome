from search import SemanticSearch
from scraper import scrape_text_from_suppliers

semantic_search = SemanticSearch()

def run():
    # Load text from URLs
    print('Scraping text from URLs...')
    docs, suppliers = scrape_text_from_suppliers('../suppliers.json', max_suppliers=10)

    # Preprocessing
    print('Preprocessing...')
    docs = semantic_search.preprocessing(docs)

    # Flatten documents keeping reference
    print('Flattening documents...')
    flatten_docs = []
    reference_docs = {}
    count = 0
    for doc, supplier in zip(docs, suppliers):
        for i in range(len(doc)):
            reference_docs[count + i] = supplier
            flatten_docs.append(doc[i])
        count += len(doc)

    # Embed
    print('Embedding...')
    embeddings = semantic_search.embed(flatten_docs)
    query = "Organic Almonds. We're looking for almonds from an organic producer or grower"
    query_embedding = semantic_search.embed([query])[0]

    # Search
    print('Searching for "{}"'.format(query))
    results = semantic_search.search(query_embedding, embeddings)

    # Print results
    for i, result in enumerate(results):
        print('{}. {} -> {}'.format(i+1, reference_docs[result['corpus_id']], result['score']))

if __name__ == "__main__":
    run()