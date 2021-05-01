"""
@author: Johanna Rahm
Research group Heilemann
Institute for Physical and Theoretical Chemistry, Goethe University Frankfurt a.M.

VisualizeDeepSTORM2DLocs functionalities.
"""


import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def xy_loc_vis(frame_locs, pixel_size):
    x = frame_locs["x [nm]"] / pixel_size
    y = frame_locs["y [nm]"] / pixel_size
    return x, y


def confidence_hist(predictions):
    confidences = predictions["confidence [a.u]"]
    fig = plt.figure()
    plt.hist(confidences, density=True)
    plt.xlim(0, 1)
    plt.title("Confidences of predicted localizations")
    plt.xlabel("Confidence [a.u]")
    plt.ylabel("Frequency [%]")
    plt.show()


def vis_density(movies_dim, gt_locs, pred_locs, pixel_size):
    area = (movies_dim[1]*pixel_size/1000)*(movies_dim[2]*pixel_size/1000)  # patch area in ym²
    if len(gt_locs):
        density_gt = [len(gt_locs[gt_locs["frame"] == frame])/area for frame in gt_locs["frame"].unique()]
        density_pred = [len(pred_locs[pred_locs["frame"] == frame])/area for frame in pred_locs["frame"].unique()]
        print("Mean density per frame ground truth: {0:.3f} em/\u00B5m²".format(np.mean(density_gt)))
        print("Mean density per frame prediction: {0:.3f} em/\u00B5m²".format(np.mean(density_pred)))

        fig, (ax1, ax2) = plt.subplots(1, 2, constrained_layout=True)
        sns.boxplot(ax=ax1, data=density_gt, color="cornflowerblue", showmeans=True,
                         meanprops={"marker": "*", "markerfacecolor": "white", "markeredgecolor": "0.25", "markersize": "10"})
        ax1.title.set_text("Density of GT locs per frame")
        ax1.set_ylabel("density [emitters/\u00B5m²]")
        sns.boxplot(ax=ax2, data=density_pred, color="cornflowerblue", showmeans=True,
                         meanprops={"marker": "*", "markerfacecolor": "white", "markeredgecolor": "0.25", "markersize": "10"})
        ax2.title.set_text("Density of predicted locs per frame")
        ax2.set_ylabel("density [emitters/\u00B5m²]")
    else:
        fig = plt.figure(figsize=(3, 5))
        density_pred = [len(pred_locs[pred_locs["frame"] == frame])/area for frame in pred_locs["frame"].unique()]
        print("Mean density prediction: {0:.3f} em/\u00B5m²".format(np.mean(density_pred)))
        sns.boxplot(data=density_pred, color="cornflowerblue", showmeans=True,
                    meanprops={"marker": "*", "markerfacecolor": "white", "markeredgecolor": "0.25", "markersize": "10"})
        plt.title("Density of predicted locs per frame")
        plt.ylabel("density [emitters/\u00B5m²]")
    plt.show()


def vis_wf_predicted_images(widefield_tif, predicted_tif):
    fig, (ax1, ax2) = plt.subplots(1,2)
    fig.tight_layout()
    fig.set_size_inches(14, 14, forward=True)
    ax1.imshow(widefield_tif, interpolation="nearest", cmap="gray")
    ax2.imshow(predicted_tif, interpolation="nearest", cmap="gray")
    ax1.axis("off"); ax2.axis("off");
    ax1.title.set_text("Widefield image (all frames)")
    ax2.title.set_text("Predicted image (all frames)")
    plt.show()
