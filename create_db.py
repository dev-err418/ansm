import json
import sys
import ast
import uuid
from typing import Dict
from medee.sparse import create_sparse_embedding
from medee.dense import create_dense_embedding
from medee.utils import remove_parentheses, remove_prefix, remove_extra_dots, remove_bracketed_content
from medee.qdrant import is_collection_created, create_collection, upload_single

collection_name = "ansm"

# lecture du JSON
def read_json(file_path: str):
    with open(file_path, "r") as f:
        return json.load(f)

def vectorize_and_append(to_embed_dense: str, to_embed_sparse: str, content: str):
    dense_vector = create_dense_embedding(to_embed_dense)
    cols, weights = create_sparse_embedding(to_embed_sparse)
    sparse_vector = {
        "indices": cols, "values": weights
    }

    upload_single(
        id=str(uuid.uuid4()),
        collection_name=collection_name,
        dense_vector=dense_vector,
        sparse_vector=sparse_vector,
        payload={
            content: content
        }
    )

def recursive_sub_or_content(sub: str, branch: Dict):
    if sub == "content": # on a un child et du contenu
        # enlève les "................."
        content = remove_extra_dots(branch["content"])

        # enlève les "[à compléter ultérieurement par le titulaire]"
        content = remove_bracketed_content(content)

        vectorize_and_append(
            to_embed_dense=sub, # la str a dense embed (contenu/titre/path/etc...)
            to_embed_sparse=sub, # la str a sparse embed (contenu/titre/path/etc...)
            content=content # le contenu affiché dans la DB pour se reperer
        )
    elif sub != "": # on a un sous titre
        print(sub)
        for sub_sub in branch[sub]:
            recursive_sub_or_content(
                sub=sub_sub,
                branch=branch[sub]
            )

if __name__ == "__main__":
    file_path = "data.json"

    is_collection_created(collection_name)

    medicaments = read_json(file_path)

    for med in medicaments:
        title = med["name"]
        infos = med["fiche_info"]
        caracteristiques = med["resume_caracteristique"]

        for i in infos:
            # transforme "Autres informations (cliquer pour afficher)" en "Autres informations"
            key = remove_parentheses(i)
            path = title + key
            content = infos[i]

            vectorize_and_append(
                to_embed_dense=path, # la str a dense embed (contenu/titre/path/etc...)
                to_embed_sparse=path, # la str a sparse embed (contenu/titre/path/etc...)
                content=content # le contenu affiché dans la DB pour se reperer
            )

        for c in caracteristiques:
            # transforme "1. DENOMINATION DU MEDICAMENT" en "DENOMINATION DU MEDICAMENT"
            key = remove_prefix(c) # ?.lower()
            path = title + key

            for sub in caracteristiques[c]:
                recursive_sub_or_content(
                    sub=sub,
                    branch=caracteristiques[c]
                )
