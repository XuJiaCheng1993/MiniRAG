import requests


class SiliconFlowReranker():
    def __init__(self, api_key: str, model_name: str):
        self.api_url = "https://api.siliconflow.cn/v1/rerank"
        self.api_key = api_key
        self.model_name = model_name


    def rerank(self, query: str, documents: list[str], top_k=5):

        payload = {
            "model": self.model_name,
            "query": query,
            "documents": documents
        }
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        response = requests.request("POST", self.api_url, json=payload, headers=headers)

        index = list(range(len(documents)))

        if response.status_code == 200:
            results = response.json()
            results = results.get('results', [])
            if len(results) > 0:
                index = sorted(results, key=lambda x: x['relevance_score'], reverse=True)
                index = [p["index"] for p in index[:top_k]]
        
        return [documents[idx] for idx in index]


if __name__ == "__main__":
    from config import api_key
    reranker = SiliconFlowReranker(api_key, "BAAI/bge-reranker-v2-m3")
    res = reranker.rerank("What is the capital of France?", ["London", "Paris", "Berlin", "Tokyo"])
    print(res)



