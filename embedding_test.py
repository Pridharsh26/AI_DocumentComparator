from transformers import AutoTokenizer, AutoModel
import torch


model_name = "BAAI/bge-small-en-v1.5"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)


text = "Employees can work remotely 3 days a week."

inputs = tokenizer(
    text,
    return_tensors="pt",
    truncation=True
)


with torch.no_grad():
    output = model(**inputs)


embedding = output.last_hidden_state[:, 0]

print(embedding.shape)