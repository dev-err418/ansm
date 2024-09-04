import os
from dotenv import load_dotenv
import torch
from transformers import AutoModelForMaskedLM, AutoTokenizer
from typing import Tuple, List

load_dotenv()
token = os.getenv("HF_TOKEN")

model_id = "naver/splade-v3"
tokenizer = AutoTokenizer.from_pretrained(model_id, token=token)
model = AutoModelForMaskedLM.from_pretrained(model_id, token=token)

def create_sparse_embedding(d: str) -> Tuple[List[int], List[float]]:
    tokens = tokenizer(d, return_tensors="pt", truncation=True, max_length=512)
    output = model(**tokens)

    vec = torch.max(
        torch.log(
            1 + torch.relu(output.logits)
        ) * tokens.attention_mask.unsqueeze(-1),
        dim=1
    )[0].squeeze()

    # on transforme en objet notre vecteur sparse
    cols = vec.nonzero().squeeze().cpu().tolist()
    weights = vec[cols].cpu().tolist()

    return cols, weights
