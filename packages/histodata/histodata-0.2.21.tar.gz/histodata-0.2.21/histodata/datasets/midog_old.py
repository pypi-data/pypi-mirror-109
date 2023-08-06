import os
from typing import Callable
from typing import Optional as O
from typing import Sequence
from typing import Union as U

from ..base import data_readers, df_creators, df_manipulators
from ..base.histo_dataset import HistoDataset


def bach_patches(
    root: str,  # '/data/ldap/histopathologic/original_read_only/BACH/ICIAR2018_BACH_Challenge'
    transformation: O[U[Callable, Sequence[Callable]]] = None,
    pre_transformation: O[U[Callable, Sequence[Callable]]] = None,
    subset: O[str] = "all",
    splitting_seed: int = 69,
    splitting_trainings_percentage: float = 0.8,
    seed: O[int] = None,
    patch_size: O[int] = None,
    overlapping_percentage: float = 0.0,
) -> HistoDataset:
    """
    Creates the Bach dataset and returns it as type HistoDataset, which inherits from torch.utils.data.Dataset.

    Data and further information can be found at the README.md of the git repository (TODO).

    Arguments:
        root: absolute path to the dataset files.
        transformation (Callable): A callable or a list of
                       callable transformations.
        pre_transformation (Callable): A callable or a list of
                       callable transformations. "pre_transformation"
                       is called before "transformation". The transformation
                       is called with a seed and will give always the same
                       result.
        subset: Which part of the dataset should be used.
                One of {"train", "valid", "test", "all"}
        splitting_seed: Seed used for splitting the data set
        splitting_trainings_percentage: Percentage how to split data
        seed:   The seed that is used for the "pre_transformation" and the
                "transformation". If the seed is set, the "pre_transformation"
                will always use the same seed for a data row. If the seed is
                set, the "transformation" will use always the same seed
                depending on the call position. For example:
                    Call-Index,     Seed f.              Seed f.
                                pre_transformation,  transformation
                        0     ,     100           ,    124
                        1     ,     100           ,    512
                        2     ,     100           ,    810
                        3     ,     100           ,    612
                    If we create the exact same dataset the transformation seeds
                    will be the same:
                    Call-Index,     Seed f.              Seed f.
                                pre_transformation,  transformation
                        0     ,     100           ,    124
                        1     ,     100           ,    512
                        2     ,     100           ,    810
                        3     ,     100           ,    612
        patch_size: If the patch size is given the large original image get
                cropped to multiple patches.
        overlapping_percentage: If patch_size is given, you can use this value
                to overlap the cropping areas. 0 <= overlapping_percentage < 1.
                0 means that the cropping areas are not overlapping.
                A value close to 1 means that nearly each pixel are overlapping.

    Returns:
        HistoDataset:
            The dataset that loads the bach patches. You can use this
            as normal pytorch dataset. If you call it, the data will
            be returned as dictionary.
    """

    # TODO what does this exactly do?
    if patch_size:
        manipulators_to_use = [
            df_manipulators.EditDFImageGrid(patch_size, overlapping_percentage, (1536, 2048))
        ]
        data_reader = data_readers.ReadFromImageFile(
            "Photos/{label}/{file_name}", return_image_size=patch_size
        )
    else:
        manipulators_to_use = []
        data_reader = data_readers.ReadFromImageFile("Photos/{label}/{file_name}")

    # handle training, validation and test cases
    if subset:
        subset = subset.lower()
    if subset.startswith("tr"):
        manipulators_to_use.append(
            df_manipulators.RandomFilterByColumnValue(
                "file_name", splitting_trainings_percentage, mode=0, seed=splitting_seed
            )
        )
    elif subset.startswith("val"):
        manipulators_to_use.extend(
            [
                df_manipulators.RandomFilterByColumnValue(
                    "file_name", splitting_trainings_percentage, mode=1, seed=splitting_seed
                ),
                df_manipulators.RandomFilterByColumnValue(
                    "file_name", 0.5, mode=0, seed=splitting_seed + 10000
                ),
            ]
        )
    elif subset.startswith("te"):
        manipulators_to_use.extend(
            [
                df_manipulators.RandomFilterByColumnValue(
                    "file_name", splitting_trainings_percentage, mode=1, seed=splitting_seed
                ),
                df_manipulators.RandomFilterByColumnValue(
                    "file_name", 0.5, mode=1, seed=splitting_seed + 10000
                ),
            ]
        )
    elif subset == "all":
        pass
    else:
        raise NotImplementedError(
            'The parameter "subset" needs to be one of ["train", "valid", "test", "all"].'
        )

    # path to ground truth
    path_to_csv = "Photos/microscopy_ground_truth.csv"

    # create HistoDataset object and pass relevant attributes
    ds = HistoDataset(
        df_creators.CreateDFFromCSV(path_to_csv, header=None, names=["file_name", "label"]),
        root,
        df_manipulators=manipulators_to_use,
        data_readers=data_reader,
        feature_readers=data_readers.ReadValueFromCSV(
            r"{label}", encoded_values=["Benign", "InSitu", "Invasive", "Normal"]
        ),
        seed=seed,
        pre_transfs=pre_transformation,
        da_transfs=transformation,
    )
    return ds


""" TODO: how the offline dataset was generated
from torchvision import transforms

transform = transforms.Compose([
    transforms.ToPILImage(),
    transforms.Resize(423), # (2*299**2)**0.5 => 423
    transforms.ToTensor(),
])

# BACH
from histodata.datasets import bach

path_bach = '/data/ldap/histopathologic/original_read_only/BACH/ICIAR2018_BACH_Challenge'

ds = bach.bach_patches(path_bach,
                       transformation=transform,
                       subset='train',
                       seed=200,
                      )
ds.save('/data/ldap/histopathologic/original_read_only/BACH2/train')
ds = bach.bach_patches(path_bach,
                       transformation=transform,
                       subset='valid',
                       seed=200,
                      )
ds.save('/data/ldap/histopathologic/original_read_only/BACH2/valid')
ds = bach.bach_patches(path_bach,
                       transformation=transform,
                       subset='test',
                       seed=200,
                      )
ds.save('/data/ldap/histopathologic/original_read_only/BACH2/test')
"""


def bach_patches_preprocessed(
    root: str,  # '/data/ldap/histopathologic/original_read_only/BACH2/'
    transformation: O[U[Callable, Sequence[Callable]]] = None,
    pre_transformation: O[U[Callable, Sequence[Callable]]] = None,
    subset: O[str] = "train",
    seed: O[int] = None,
) -> HistoDataset:
    """
    Creates the Bach dataset and returns it as type HistoDataset, which inherits from torch.utils.data.Dataset.

    Data and further information can be found at TODO

    Arguments:
        root: absolute path to the dataset files.
                transformation (Callable): A callable or a list of
                       callable transformations.
        pre_transformation (Callable): A callable or a list of
                       callable transformations. "pre_transformation"
                       is called before "transformation". The transformation
                       is called with a seed and will give always the same
                       result.
        subset: Which part of the dataset should be used.
                One of {"train", "valid", "test"}
        seed:   The seed that is used for the "pre_transformation" and the
                "transformation". If the seed is set, the "pre_transformation"
                will always use the same seed for a data row. If the seed is
                set, the "transformation" will use always the same seed
                depending on the call position. For example:
                    Call-Index,     Seed f.              Seed f.
                                pre_transformation,  transformation
                        0     ,     100           ,    124
                        1     ,     100           ,    512
                        2     ,     100           ,    810
                        3     ,     100           ,    612
                    If we create the exact same dataset the transformation seeds
                    will be the same:
                    Call-Index,     Seed f.              Seed f.
                                pre_transformation,  transformation
                        0     ,     100           ,    124
                        1     ,     100           ,    512
                        2     ,     100           ,    810
                        3     ,     100           ,    612

    Returns:
        HistoDataset:
            The dataset that loads the bach patches. You can use this
            as normal pytorch dataset. If you call it, the data will
            be returned as dictionary.
    """
    if subset:
        subset = subset.lower()
    if subset.startswith("tr"):
        path_to_dataset = os.path.join(root, "train")
    elif subset.startswith("val"):
        path_to_dataset = os.path.join(root, "valid")
    elif subset.startswith("test"):
        path_to_dataset = os.path.join(root, "test")
    else:
        raise NotImplementedError(
            'The parameter "subset" needs to be one of ["train", "valid", "test"].'
        )

    # create HistoDataset object and pass relevant attributes
    ds = HistoDataset(
        df_creators.CreateDFFromCSV("features.csv"),
        path_to_dataset,
        data_readers="data/{id}.tiff",
        feature_readers=data_readers.ReadValueFromCSV(
            r"{feature}", encoded_values=["0", "1", "2", "3"]
        ),
        seed=seed,
        pre_transfs=pre_transformation,
        da_transfs=transformation,
    )
    return ds

