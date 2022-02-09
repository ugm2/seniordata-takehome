from search import SemanticSearch
from scraper import scrape_text_from_suppliers

semantic_search = SemanticSearch()

def run(query: str, top_k: int, max_suppliers: int):
    # Load text from URLs
    print('Scraping text from URLs...')
    docs, suppliers = scrape_text_from_suppliers(
        '../suppliers.json',
        folder_persistance='data',
        max_suppliers=max_suppliers)

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
    query_embedding = semantic_search.embed([query])

    # Search
    print('Searching for "{}"'.format(query))
    results = semantic_search.search(query_embedding, embeddings, top_k=top_k)

    # Collapse repeated results and get relevant information about the selected suppliers
    results_dict = {}
    for i, result in enumerate(results):
        supplier = reference_docs[result['corpus_id']]['supplier']
        if supplier not in results_dict:
            results_dict[supplier] = {
                'score': result['score'],
                'sentence': flatten_docs[result['corpus_id']],
                'url': reference_docs[result['corpus_id']]['rootDomain']
            }
        if len(results_dict) == top_k:
            break

    # Print results
    print('--------------------------------')
    for i, (supplier, result) in enumerate(results_dict.items()):
        print('{}. {} -> {}'.format(i+1, supplier, result['score']))
        print('URL: {}'.format(result['url']))
        print('Matching sentence: {}'.format(result['sentence']))
        print('--------------------------------')

if __name__ == "__main__":
    # Query to search
    query = "Organic Almonds. We're looking for almonds from an organic producer or grower"
    # Max number of results
    top_k = 5
    # Number of suppliers to scrape. -1 means all
    max_suppliers = -1

    run(query, top_k, max_suppliers)