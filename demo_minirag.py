from src.workflow import MiniRag


minirag = MiniRag()
query = "怎么使用Vanna实现chatBI"

chunks = []
for chunk in minirag.invoke(query):
    chunks.append(chunk)

print(chunks)