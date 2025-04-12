import fiftyone as fo

# A name for the dataset
name = "open-images-v7"

# The directory containing the dataset to import
dataset_dir = "/Users/samuel/fiftyone/open-images-v7/test"

# The type of the dataset being imported
dataset_type = fo.types.OpenImagesV7Dataset  # for example

dataset = fo.Dataset.from_dir(
    dataset_dir=dataset_dir,
    dataset_type=dataset_type,
    name=name,
)