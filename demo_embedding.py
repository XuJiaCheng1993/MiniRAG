from src.embedding import load_and_chunk


load_and_chunk(
    file_path = "demo.md",
    separator = "\n\n", 
    chunk_size = 1024, 
    chunk_overlap = 80
)

