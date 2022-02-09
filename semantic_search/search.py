from sentence_transformers import SentenceTransformer
from sentence_transformers.util import semantic_search, normalize_embeddings, dot_score
import torch
from typing import List
import re
from tok import sent_tokenize

class SemanticSearch:

    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        self.embedder = SentenceTransformer(model_name)
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.embedder.to(self.device)

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
            sentences = sent_tokenize(t)
            # Join tokens
            sentences = list(map(lambda x: ' '.join(x), sentences))
            text_sentences.append(sentences)
        # Remove repeated sentences
        text_sentences = list(map(lambda x: list(set(x)), text_sentences))
        return text_sentences

    def embed(self, texts: List[str]) -> List[torch.Tensor]:
        return self.embedder.encode(texts, convert_to_tensor=True)

    def search(self, query_embeddings: torch.Tensor, corpus_embeddings: torch.Tensor, top_k=5) -> List[str]:
        query_embeddings.to(self.device)
        corpus_embeddings.to(self.device)
        corpus_embeddings = normalize_embeddings(corpus_embeddings)
        query_embeddings = normalize_embeddings(query_embeddings)
        # top_k is multiplied by 5 because we may have several relevant sentences per supplier
        search_results = semantic_search(query_embeddings, corpus_embeddings, top_k=top_k*5, score_function=dot_score)[0]
        return search_results
