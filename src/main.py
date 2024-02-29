import pandas as pd
from pathlib import Path, PurePath
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def read_data(path: str) -> pd.DataFrame:
    data = pd.read_csv(Path(PurePath(path).parents[1], "transactions.csv"))
    data["Date"] = pd.to_datetime(data["Date"])
    return data


def group_by_month(data: pd.DataFrame) -> pd.DataFrame:
    return data.groupby([data["Date"].dt.to_period("M"), "Item Name"])["Transaction #"].count().unstack("Item Name")


def split_into_groups(unstacked_data) -> list:
    split_point = 1000
    sorted_values = unstacked_data.sum().sort_values(ascending=False)
    group1 = sorted_values[sorted_values > split_point].index.tolist()
    group2 = sorted_values[sorted_values <= split_point].index.tolist()
    return [group1, group2]


def filter_and_plot(data: pd.DataFrame, items: list, i: int, ax: plt.Axes) -> None:
    items = [item for item in items if item in data.columns]
    subset_data = data.loc[:, items]
    for column in subset_data.columns:
        ax.plot(subset_data.index.to_timestamp(), subset_data[column], label=column)
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_minor_locator(mdates.WeekdayLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    ax.set_title("Sales over time (Chart {})".format(i + 1), fontsize=22)
    ax.set_xlabel("Time", fontsize=16)
    ax.set_ylabel("Number of sales / month", fontsize=16)
    ax.legend(fontsize="large")


def main():
    data = read_data(__file__)
    unstacked_data = group_by_month(data)
    groups = split_into_groups(unstacked_data)
    fig, axes = plt.subplots(len(groups), 1)
    for i, items in enumerate(groups):
        filter_and_plot(unstacked_data, items, i, axes[i])
    plt.show()


if __name__ == "__main__":
    main()
