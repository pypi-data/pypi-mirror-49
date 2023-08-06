import torch
from legos.torch_utils import compare_near, running_mean

def test_running_mean():
    # TODO: list_data may contain integers
    list_data = [1., 2., 3.]
    output = running_mean(list_data, 0.5)
    compare_near(output, torch.tensor(2.25))
