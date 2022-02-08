from sentence_transformers import SentenceTransformers
from sentence_transformers.util import semantic_search
import torch
import spacy
from typing import List

class SemanticSearch:

    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        self.embedder = SentenceTransformers(model_name)
        self.device = 'cuda' if torch.cude.is_available() else 'cpu'
        self.embedder.to(self.device)
        self.tokenizer = spacy.load('')

    def preprocessing(self, text: List[str]) -> List[str]:
        # Tokenize
        # Remove stopwords
        return 

    def embed(self, text: List[str]) -> List[torch.Tensor]:
        return self.embedder.encode(text, convert_to_tensor=True)

    def search(self, query: torch.Tensor, corpus: List[torch.Tensor], top_k=5) -> List[str]:
        query.to(self.device)
        corpus.to(self.device)
        search_results = semantic_search([query], corpus, top_k=top_k)[0]
        return [result['corpus_id'] for result in search_results]
