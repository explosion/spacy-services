from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel
from spacy.lang.en import English
from sense2vec import Sense2Vec

MODEL_PATHS = {
    "2015": "./vectors/s2v_reddit_2015_md",
    "2019": "./vectors/s2v_reddit_2019_lg",
}
# fmt: off
SENSES = ["auto", "ADJ", "ADP", "ADV", "AUX", "CONJ", "DET", "INTJ", "NOUN",
          "NUM", "PART", "PERSON", "PRON", "PROPN", "PUNCT", "SCONJ", "SYM",
          "VERB", "NORP", "FACILITY", "ORG", "GPE", "LOC", "PRODUCT", "EVENT",
          "WORK_OF_ART", "LANGUAGE"]
# fmt: on

app = FastAPI()


class Query(BaseModel):
    word: str
    sense: str = "auto"
    model: str = "2015"
    n_results: int = 200


print(f"Loading {len(MODEL_PATHS)} vector models...")
LEMMATIZER = English().vocab.morphology.lemmatizer
MODELS = {}
for name, path in MODEL_PATHS.items():
    print(f"Loading vectors '{name}'...")
    s2v = Sense2Vec().from_disk(path)
    MODELS[name] = s2v
    print(f"Loaded vectors '{name}'.")
print(f"Loaded {len(MODELS)} vector models.")


@app.get("/models")
def models():
    """Get all available models and their senses."""
    return {"senses": SENSES, "models": list(MODELS)}


@app.post("/find")
def find(query: Query):
    """Find similar terms for a given term and optional sense."""
    s2v = MODELS[query.model]
    sense_options = [query.sense] if query.sense != "auto" else []
    best_key = s2v.get_best_sense(query.word, sense_options)
    if not query.word or not best_key:
        return {"text": query.word, "sense": query.sense, "results": [], "count": 0}
    results = []
    best_word, best_sense = s2v.split_key(best_key)
    seen = set([best_word, min(LEMMATIZER(best_word, best_sense))])
    similar = s2v.most_similar(best_key, n=query.n_results)
    for sim_key, score in similar:
        sim_word, sim_sense = s2v.split_key(sim_key)
        head = min(LEMMATIZER(sim_word, sim_sense))
        if head not in seen:
            freq = s2v.get_freq(sim_key)
            results.append({"score": float(score), "text": sim_word, "count": freq})
            seen.add(head)
        if len(results) >= query.n_results:
            break
    return {"text": best_word, "sense": best_sense, "results": results}


if __name__ == "__main__":
    uvicorn.run(app, port=8080)
