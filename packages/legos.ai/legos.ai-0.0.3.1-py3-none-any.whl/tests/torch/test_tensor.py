import torch
import hypothesis.strategies as st
from hypothesis import given
from legos.torch_utils import compare_near, running_mean

def test_lerp():
    a = torch.tensor(1.)
    b = torch.tensor(2.)
    c = torch.tensor(3.)

    t1 = b.lerp(a, 0.5)
    assert t1 == torch.tensor(1.5)

    t2 = t1.lerp(c, 0.5)
    assert t2 == torch.tensor(2.25)

def lerp_list(list_data, alpha):
    assert len(list_data) > 0
    output = torch.tensor(list_data[0])

    for i in range(1, len(list_data)):
        a = torch.tensor(list_data[i], dtype=torch.float32)
        output.lerp_(a, alpha)
    return output

# The following test shows that lerp_list is not the same as running_mean
# @given(st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1),
#        st.floats(allow_infinity=False, allow_nan=False))
# def test_lerp_list_auto(list_data, alpha):
#     output = lerp_list(list_data, alpha)
#     running = running_mean(list_data, alpha)

#     assert output == running
