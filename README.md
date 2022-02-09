# Seniordata Takehome Challenge

This repository aims at approaching a methodology for retrieving the suppliers that are semantically closer to the given company (a given text query) by using the text scrapped from each supplier.

## Setup

* Create and activate python environment using Virtualenv or conda
* Install dependencies: `sh install_dependencies.sh`

## Run

* Go to semantic_search folder: `cd semantic_search`
* Run main.py: `python main.py`

Inside the main.py file, you can change the query and the number of results to be returned. Also, if short of time, you can reduce the number of suppliers taken into account by changing `max_suppliers`.

Running scrapping over websites (if cache is not available) would take some time as well as embedding the sentences (although much less).

## Methodology

1. Scrap the text from each supplier's website. I do caching to avoid having to scrape the same data over and over again.
2. Preprocess to remove emojis and break down the text into sentences. I don't remove punctuation or lowercase or anything because I'm using Transformers to embed the sentences and those are trained on raw data.
3. Flatten documents (list of lists of sentences) so each sentence is a single element in the list and thus can be retreived individually.
4. Embed the sentences using Sentence Transformers. I particularly use 'all-MiniLM-L6-v2' because performs well for general english.
5. Search for the closest sentences using the cosine similarity. Although in the code says `dot_product`, because I'm normalising the embeddings for optimisation, it works the same way as no normalisation and then using cosine similarity.
6. Sentences from the same supplier are collapsed into one supplier as a result.
7. Results are printed

## Results

For the query:

`Organic Almonds. We're looking for almonds from an organic producer or grower`.

And top_k = 5

Results are:

```text
----------------------------------------------------------------
1. RAW ORGANIC NUTS AND SEEDS -> 0.7555698156356812
URL: http://www.rawnutsandseeds.com
Matching sentence: pastuerized USA Grown Almonds are now available !
----------------------------------------------------------------
2. Watkins Products -> 0.7503774166107178
URL: https://www.watkins1868.com
Matching sentence: Organic Pure Almond , 4 fl .
----------------------------------------------------------------
3. Watson & Pratts -> 0.725695013999939
URL: https://www.watsonandpratts.co.uk
Matching sentence: IngredientsOrganically Grown Almonds .
----------------------------------------------------------------
4. Earls Organic -> 0.6960368752479553
URL: https://www.earlsorganic.com
Matching sentence: YesCommodities : Multiple almond varieties .
----------------------------------------------------------------
5. Produce Express -> 0.6860389113426208
URL: https://www.produceexpress.net
Matching sentence: operative of over 3,000 California growers who produce the finest almonds for raw consumption , and various almond products like their luscious almond milk .
----------------------------------------------------------------
```

Each section contains the name of the provider with the assigned score, the main URL and the sentence with highest score for the given query for that provider.

## Improvements

1. I would improve the scrapping algorithm:
   1. Avoid failing as much as possible.
   2. Get text from more relevant tags inside the website.
2. Improve preprocessing:
   1. I would look more thoroughly at the returned text to improve cleaning of the same.
   2. Improve sentence segmentation (currently it's a more naive approach than using Spacy, but much faster).
3. Representation of a supplier (document with sentences) could be better done. Right now each sentence is ranked separetely without including the information of belonging to a supplier.
4. Embedding and ranked search.
   1. Normally I would use Elasticsearch with Haystack + Faiss for semantic search.
   2. Indexing of documents could only be done once (depending on the use case) and then the entire process would just be searching using the given query, which is fast.
   3. Look for a better sentence transformer related to food or create our own.
5. Perform query expansion on input query to look for more specific results.For instance, adding `buy` to the query could help search for websites that sell almonds.