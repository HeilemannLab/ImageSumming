"""
@author: Johanna Rahm
Research group Heilemann
Institute for Physical and Theoretical Chemistry, Goethe University Frankfurt a.M.

Save binned image results as localization file .csv in DeepSTORM2D format & tif.
"""


import pandas as pd
import tifffile


def merge_random_locs(random_locs):
    """
    Convert into DeepSTORM2D format & return concatenated dataframe.
    frame idx starts at 1
    header = ,frame,x [nm],y [nm],Photon #,Sigma [nm]
    """
    for c, i in enumerate(random_locs, 1):
        i["frame"] = c
    random_locs_concat = pd.concat(random_locs, ignore_index=True)
    random_locs_concat.index += 1

    deep_storm_header = ['frame', 'x [nm]', 'y [nm]', 'Photon #', 'Sigma [nm]']
    mixed_header = ['Photon #', 'Sigma [nm]', 'bkgstd [photon]', 'frame', 'intensity [photon]', 'offset [photon]',
                    'sigma [nm]', 'uncertainty_xy [nm]', 'x [nm]', 'y [nm]']
    picasso_header = ['frame', 'x [nm]', 'y [nm]', 'sigma [nm]', 'intensity [photon]', 'offset [photon]',
                      'bkgstd [photon]', 'uncertainty_xy [nm]']

    if list(random_locs_concat.columns) == picasso_header:  # only picasso format
        random_locs_DS2D_format = random_locs_concat[["frame", "x [nm]", "y [nm]", "intensity [photon]", "sigma [nm]"]]
        random_locs_DS2D_format.columns = deep_storm_header
    elif list(random_locs_concat.columns) == mixed_header:  # both picasso and ds format
        frame = random_locs_concat['frame']
        x = random_locs_concat['x [nm]']
        y = random_locs_concat['y [nm]']
        photons = random_locs_concat['Photon #'].combine_first(random_locs_concat['intensity [photon]'])
        sigma = random_locs_concat['Sigma [nm]'].combine_first(random_locs_concat['sigma [nm]'])
        random_locs_DS2D_format = pd.concat([frame, x, y, photons, sigma], axis=1, names=deep_storm_header)
    else:
        random_locs_DS2D_format = random_locs_concat
    return random_locs_DS2D_format


def save(dir_path, file_name, patches, locs):
    # save patch array as tif
    patches = patches.astype("int16")
    tifffile.imwrite(dir_path + "\\" + file_name + ".tif", patches)
    # save random locs concatenated as one csv file
    merge_random_locs(locs).to_csv(dir_path + "\\" + file_name + ".csv")
