import json
import warnings
import skimage
from legos.io import open_image
from concurrent.futures import ThreadPoolExecutor
from skimage import io
from legos.utils import is_notebook, num_cpus

def resize_fn(target_size, squared):
    def resize(image):
        if squared:
            new_h = target_size
            new_w = target_size
        else:
            h, w = image.shape[0:2]
            ratio = target_size / min(h, w)

            new_w = round(ratio * w)
            new_h = round(ratio * h)

        image = skimage.transform.resize(image, (new_h, new_w), mode='reflect', anti_aliasing=False)

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            image = skimage.img_as_ubyte(image) # resize outputs float64 but we need uint8
        return image

    return resize

def resize_imgs(file_paths, output_file_paths, target_size, squared=False, fn=None):
    """
    Read, resize images such that the smaller of height or width is equal to the target_size.
    If squared is True, the output will be a square.
    The output will be saved to the output_file_paths.
    Note:
    - This function uses ThreadPoolExecutor to perform in multithread.
    """
    if is_notebook():
        from tqdm import tqdm_notebook as tqdm
    else:
        from tqdm import tqdm

    if fn is None:
        fn = resize_fn(target_size=target_size, squared=squared)

    if len(file_paths) != len(output_file_paths):
        raise ValueError("file_paths and output_file_paths must have the same length")

    errors = {}

    def process(path, new_path):
        try:
            image = open_image(path)
            output = fn(image)
            skimage.io.imsave(new_path, output)
        except Exception as ex:
            errors[path] = str(ex)

    if len(file_paths) > 0:
        with ThreadPoolExecutor(max_workers=num_cpus()) as e:
            out = e.map(lambda paths: process(*paths), zip(file_paths, output_file_paths))
            for _ in tqdm(out, total=len(file_paths)):
                pass

    if errors:
        print("There are errors while resizing")
        print(json.dumps(errors, indent=2))