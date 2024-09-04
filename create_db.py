import json
import sys
import ast
from typing import Dict
from medee.sparse import create_sparse_embedding
from medee.utils import remove_parentheses, remove_prefix, remove_extra_dots, remove_bracketed_content

# lecture du JSON
def read_json(file_path: str):
    with open(file_path, "r") as f:
        return json.load(f)

def vectorize_and_append(to_embed_dense: str, to_embed_sparse: str, content: str):
    return 0

def recursive_sub_or_content(sub: str, branch: Dict):
    if sub == "content": # on a un child et du contenu
        # enlève les "................."
        content = remove_extra_dots(branch["content"])

        # enlève les "[à compléter ultérieurement par le titulaire]"
        content = remove_bracketed_content(content)

        vectorize_and_append(
            to_embed_dense="", # la str a dense embed (contenu/titre/path/etc...)
            to_embed_sparse="", # la str a sparse embed (contenu/titre/path/etc...)
            content="" # le contenu affiché dans la DB pour se reperer
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
                to_embed_dense="", # la str a dense embed (contenu/titre/path/etc...)
                to_embed_sparse="", # la str a sparse embed (contenu/titre/path/etc...)
                content="" # le contenu affiché dans la DB pour se reperer
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

    # print(remove_parentheses("Autres informations (cliquer pour afficher)"))
