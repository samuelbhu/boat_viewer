import fiftyone as fo
import fiftyone.zoo as foz

dataset = foz.load_zoo_dataset(
    "open-images-v7",
    split="validation",
    max_samples=5,
    seed=51,
    shuffle=True,
)

session = fo.launch_app(dataset.view())
session.wait()