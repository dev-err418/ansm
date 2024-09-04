from qdrant_client import QdrantClient, models
from qdrant_client.grpc import CollectionDescription

client = QdrantClient(
    url="http://localhost:6333" # local dev
)

def create_collection(collection_name: str):
    client.recreate_collection(
        collection_name=collection_name,
        vectors_config={
            "dense": models.VectorParams(size=1536, distance=models.Distance.COSINE)
        },
        # optimizers_config=models.OptimizersConfigDiff(
        #     indexing_threshold=0,
        # ),
        sparse_vectors_config={
            "sparse": models.SparseVectorParams(
                index=models.SparseIndexParams(
                    on_disk=False
                )
            )
        }
    )
    print(collection_name, "collection created !")

def is_collection_created(collection_name: str):
    if client.collection_exists(collection_name=collection_name):
        print(collection_name, "collection already created")
    else:
        create_collection(collection_name)

def enable_indexing_threshold(collection_name: str):
    client.update_collection(
        collection_name=collection_name,
        optimizer_config=models.OptimizersConfigDiff(indexing_threshold=20000),
    )

def upload_single(collection_name, id, payload, dense_vector, sparse_vector):
    client.upsert(
        collection_name=collection_name,
        points=[
            models.PointStruct(
            id=id,
            payload={},
            vector={
                "dense": dense_vector,
                "sparse": sparse_vector
            })
        ]
    )

def upload_batch(collection_name, ids, payloads, dense_vectors, dense_content_vectors, sparse_vectors):
    client.upsert(
        collection_name=collection_name,
        points=models.Batch(
            ids=ids,
            payloads=payloads,
            vectors={
                "dense": dense_vectors,
                "sparse": sparse_vectors,
            },
        ),
    )

def get_chunk_by_id(collection_name, ids):
    results = client.retrieve(
        collection_name=collection_name,
        ids=ids
    )

    return results

def run_filter(collection_name, value, key="title"):
    results = client.scroll(
        collection_name=collection_name,
        with_vectors=True,
        scroll_filter=models.Filter(
            must=[
                models.FieldCondition(
                    key=key,
                    match=models.MatchValue(value=value),
                )
            ]
        ),
    )

    return results[0]

def run_query(collection_name, embedding, limit):
    results = client.search(
        collection_name=collection_name,
        query_vector=models.NamedVector(
            name="dense",
            vector=embedding
        ),
        limit=limit,
        # with_vectors=["dense_content", "dense"]
    )

    return results

def run_query_sparse(collection_name, vec_name, indices, values, limit):
    results = client.search(
        collection_name=collection_name,
        query_vector=models.NamedSparseVector(
            name=vec_name,
            vector=models.SparseVector(
                indices=indices,
                values=values,
            ),
        ),
        limit=limit,
        # with_vectors=["dense_content", "dense"]
    )

    return results

def get_collection_infos(collection_name):
    infos = client.get_collection(collection_name=collection_name)

    return infos
