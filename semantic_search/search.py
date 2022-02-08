from sentence_transformers import SentenceTransformer
from sentence_transformers.util import semantic_search
import torch
from typing import List
import re
import spacy

class SemanticSearch:

    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        self.embedder = SentenceTransformer(model_name)
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.embedder.to(self.device)
        self.segmenter = spacy.load('en_core_web_sm')

    def preprocessing(self, texts: List[str]) -> List[str]:
        # Remove line breaks
        texts = list(map(lambda x: x.replace('\n', ''), texts))
        # Remove emojis
        emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           "]+", flags=re.UNICODE)
        texts = list(map(lambda x: emoji_pattern.sub(r'', x), texts))
        # Segment text into sentences
        text_sentences = []
        for t in texts:
            doc = self.segmenter(t)
            text_sentences.append([token.text for token in doc.sents])
        return text_sentences

    def embed(self, texts: List[str]) -> List[torch.Tensor]:
        return self.embedder.encode(texts, convert_to_tensor=True)

    def search(self, query: torch.Tensor, corpus: List[torch.Tensor], top_k=5) -> List[str]:
        query.to(self.device)
        corpus.to(self.device)
        search_results = semantic_search([query], corpus, top_k=top_k)[0]
        return search_results
