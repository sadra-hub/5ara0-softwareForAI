import matplotlib.pyplot as plt
from sklearn.metrics import ConfusionMatrixDisplay


def plot_data_set(data_set):
    """
    Visualize some properties of the dataset.

    Args:
        data_set (DataFrame): The dataset to be visualized.

    Raises:
        ValueError: If the 'edible' column is not present in the dataset.

    This function creates visualizations based on the edibility feature of the dataset, including:
    1. Mean Cap Diameter by Edibility
    2. Cap Shape Distribution by Edibility
    3. Cap Surface Distribution by Edibility
    4. Histogram of Cap Diameter by Edibility
    """

    # <ASSIGNMENT 3.2: Visualize some properties of the dataset>

    # Since all plots are based on edibility, check if there is such column
    if "edible" not in data_set.columns:
        raise ValueError("❌ The training set must contain the 'edible' column.")

    # Set up a 2x2 grid for the plots
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle("Visualizing Edibility Features", fontsize=16)

    # 1. Mean Cap Diameter by Edibility
    mean_diameter = data_set.groupby("edible")["cap-diameter"].mean()
    mean_diameter.plot(
        kind="bar",
        color=["red", "green"],
        ax=axes[0, 0],
        title="Mean Cap Diameter by Edibility",
    )
    axes[0, 0].set_xlabel("")
    axes[0, 0].set_ylabel("Mean Cap Diameter")
    axes[0, 0].set_xticks([0, 1])  # Correct usage of set_xticks
    axes[0, 0].set_xticklabels(
        ["Poisonous", "Edible"], rotation=0
    )  # Correct usage of set_xticklabels

    # 2. Cap Shape Distribution by Edibility
    cap_shape_counts = data_set.pivot_table(
        index="cap-shape", columns="edible", aggfunc="size", fill_value=0
    )
    cap_shape_counts.plot(
        kind="bar",
        stacked=True,
        color=["red", "green"],
        ax=axes[0, 1],
        title="Cap Shape Distribution by Edibility",
    )
    axes[0, 1].set_xlabel("Cap Shape")
    axes[0, 1].set_ylabel("Count")
    axes[0, 1].legend(["Poisonous", "Edible"], title="Edibility")

    # 3. Cap Surface Distribution by Edibility
    cap_surface_counts = data_set.pivot_table(
        index="cap-surface", columns="edible", aggfunc="size", fill_value=0
    )
    cap_surface_counts.plot(
        kind="bar",
        stacked=True,
        color=["red", "green"],
        ax=axes[1, 0],
        title="Cap Surface Distribution by Edibility",
    )
    axes[1, 0].set_xlabel("Cap Surface")
    axes[1, 0].set_ylabel("Count")
    axes[1, 0].legend(["Poisonous", "Edible"], title="Edibility")

    # 4. Histogram of Cap Diameter by Edibility
    data_set[data_set["edible"] == 1]["cap-diameter"].plot(
        kind="hist", bins=10, alpha=0.5, color="green", label="Edible", ax=axes[1, 1]
    )
    data_set[data_set["edible"] == 0]["cap-diameter"].plot(
        kind="hist", bins=10, alpha=0.5, color="red", label="Poisonous", ax=axes[1, 1]
    )
    axes[1, 1].set_title("Distribution of Cap Diameter by Edibility")
    axes[1, 1].set_xlabel("Cap Diameter")
    axes[1, 1].set_ylabel("Frequency")
    axes[1, 1].legend()

    # Adjust the layout
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.show()


def plot_confusion_matrix(score):
    ConfusionMatrixDisplay(score).plot()
