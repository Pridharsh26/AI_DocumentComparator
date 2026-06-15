import torch
import torch.nn.functional as F

from transformers import (
    AutoTokenizer,
    AutoModel
)


class EmbeddingModel:

    def __init__(self):

        model_name = "intfloat/e5-small-v2"

        self.tokenizer = AutoTokenizer.from_pretrained(
            model_name
        )

        self.model = AutoModel.from_pretrained(
            model_name
        )


    def encode(self, texts):

        if isinstance(texts, str):
            texts = [texts]


        inputs = self.tokenizer(
            texts,
            padding=True,
            truncation=True,
            return_tensors="pt"
        )


        with torch.no_grad():

            output = self.model(**inputs)


        embeddings = self.mean_pool(
            output.last_hidden_state,
            inputs["attention_mask"]
        )


        embeddings = F.normalize(
            embeddings,
            p=2,
            dim=1
        )


        return embeddings.cpu().numpy()


    def mean_pool(self, tokens, mask):

        mask = mask.unsqueeze(-1).expand(
            tokens.size()
        ).float()


        total = (tokens * mask).sum(dim=1)


        count = mask.sum(dim=1)


        return total / count