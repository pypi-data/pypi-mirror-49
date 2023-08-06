import torch
import operator
import numpy as np

def weighted_smooth(values, weight):
    '''
    Create a smoothed values by using the running mean
    '''
    if len(values) == 0:
        return []
    outputs = [0.] * len(values)
    outputs[0] = values[0]
    for i in range(1, len(values)):
        outputs[i] = exp_moving_average(outputs[i - 1], values[i], weight)
    return outputs

def get_module_names(model):
    return [name for name, m in model.named_modules()]

def get_named_modules_by_name(model, module_names):
    modules = []
    for name, m in model.named_modules():
        if name in module_names:
            modules.append((name, m))
    return modules

def get_device():
    return torch.device("cuda" if torch.cuda.is_available() else "cpu")

def get_param_to_learn(model):
    params = dict()
    for name, param in model.named_parameters():
        if param.requires_grad:
            params[name] = param
    return params

def exp_moving_average(a1, a2, alpha):
    return a1 * alpha + (1. - alpha) * a2

def running_mean(data, alpha):
    assert len(data) > 0
    alpha = torch.tensor(alpha)
    output = torch.tensor(data[0])

    for i in range(1, len(data)):
        a = torch.tensor(data[i])
        output = exp_moving_average(output, a, alpha)
    return output

def compare(a, b, cmp, cname=None):
    if cname is None:
        cname = cmp.__name__
    assert cmp(a, b), f"{cname}:\n{a}\n{b}"

def compare_eq(a, b):
    compare(a, b, operator.eq, '==')

def near(a, b):
    return torch.allclose(a, b, rtol=1e-3, atol=1e-5)

def compare_near(a, b):
    compare(a, b, near)

def rgb_from_tensor(image: torch.Tensor, mean=None, std=None, max_pixel_value=255.0) -> np.ndarray:
    image = to_numpy(image)
    if mean is not None and std is not None:
        image = (max_pixel_value * (image * std + mean)).astype(np.uint8)
    return image

def to_numpy(image: torch.Tensor) -> np.ndarray:
    image = image.permute(1, 2, 0)  # CHW -> HWC
    image = image.detach().cpu().numpy()
    return image.squeeze()

def to_device(device, t):
    return t.to(device)
