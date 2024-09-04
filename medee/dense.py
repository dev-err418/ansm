from transformers import AutoModel, AutoTokenizer
import torch
import torch.nn.functional as F
from torch import Tensor
from typing import List

model_name = "Alibaba-NLP/gte-Qwen2-1.5B-instruct"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

def create_dense_embedding(d: str) -> List[float]:
    inputs = tokenizer(d, return_tensors="pt", padding=True, truncation=True)

    with torch.no_grad():
        outputs = model(**inputs)
        embedding = outputs.last_hidden_state.mean(dim=1)

        return embedding.tolist()[0]
