# model/model.py
import torch
import torch.nn as nn

class TextRewriterModel(nn.Module):
    def __init__(self, vocab_size, embedding_dim, hidden_dim):
        super(TextRewriterModel, self).__init__()
        self.embedding = nn.Embedding(vocab_size, embedding_dim)
        self.rnn = nn.LSTM(embedding_dim, hidden_dim, num_layers=2, batch_first=True)
        self.fc = nn.Linear(hidden_dim, vocab_size)

    def forward(self, x):
        x = self.embedding(x)
        output, (hidden, cell) = self.rnn(x)
        x = self.fc(output[:, -1, :])
        return x
