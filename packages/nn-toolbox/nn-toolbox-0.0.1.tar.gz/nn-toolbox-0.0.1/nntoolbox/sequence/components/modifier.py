import torch
from torch import nn
from torch.nn.utils.rnn import pack_padded_sequence, pad_packed_sequence, PackedSequence


class ModifiedStackedRNN(nn.Module):
    def __init__(
            self, base_rnn, num_layers: int, input_size: int, hidden_size: int,
            bidirectional: bool, dropout: float=0.0, **kwargs
    ):
        super(ModifiedStackedRNN, self).__init__()
        layers = [base_rnn(
            num_layers=1, input_size=input_size if l == 0 else hidden_size, hidden_size=hidden_size,
            bidirectional=bidirectional, **kwargs
        ) for l in range(num_layers)]
        self._layers = nn.ModuleList(layers)
        self._dropouts = nn.ModuleList([nn.Dropout(dropout) for _ in range(num_layers - 1) if dropout > 0.0])
        self._num_layers = num_layers
        self._num_directions = 2 if bidirectional else 1

    def forward(self, input, h_0=None, lengths=None): pass


class ResidualRNN(ModifiedStackedRNN):
    '''
    StackedRNN with residual connections:
    i_{l + 1} = o_l + i_l = i_l + f(i_l, h_{l - 1})
    o_{l + 1} = f(i_{l + 1}, h_l)

    '''
    def __init__(self, base_rnn, num_layers: int, input_size: int, bidirectional: bool, dropout: float=0.0, **kwargs):
        assert 'hidden_size' not in kwargs
        assert num_layers > 0
        super(ResidualRNN, self).__init__(
            base_rnn, num_layers, input_size, input_size,
            bidirectional, dropout, **kwargs
        )

    def forward(self, input, h_0=None, lengths=None):
        if isinstance(input, PackedSequence):
            input_unpacked, lengths = pad_packed_sequence(input)
            input_packed = input
        elif isinstance(input, torch.Tensor):
            assert lengths is not None
            assert len(input.shape) == 3

            input_unpacked = input
            input_packed = pack_padded_sequence(input, lengths=lengths)
        else:
            raise ValueError

        if h_0 is None:
            h_0 = torch.zeros(
                size=(self._num_layers, self._num_directions, input_unpacked.shape[1], input_unpacked.shape[2])
            ).to(input_unpacked.device)
        hiddens = []
        for l in range(len(self._layers)):
            if l > 0:
                input_unpacked = input_unpacked + output_unpacked
                if len(self._dropouts) > 0:
                    input_unpacked = self._dropouts[l - 1](input_unpacked)
                input_packed = pack_padded_sequence(input_unpacked, lengths)

            output_packed, hidden = self._layers[l](input_packed, h_0[l])
            output_unpacked, lengths = pad_packed_sequence(output_packed)
            output_unpacked = torch.mean(
                output_unpacked.view(
                    output_unpacked.shape[0], output_unpacked.shape[1], self._num_directions, -1
                ),
                dim=-2
            )

            if l < self._num_layers - 1:
                output_packed = pack_padded_sequence(output_unpacked, lengths)
            hiddens.append(hidden)

        if isinstance(input, PackedSequence):
            return output_packed, torch.cat(hiddens, dim=0)
        else:
            return output_unpacked, torch.cat(hiddens, dim=0)
