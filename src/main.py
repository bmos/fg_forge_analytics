import pandas as pd
from pathlib import Path, PurePath
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def read_data(path: str) -> pd.DataFrame:
    data = pd.read_csv(Path(PurePath(path).parents[1], "transactions.csv"))
    data["Date"] = pd.to_datetime(data["Date"])
    return data


def group_data(data: pd.DataFrame) -> pd.DataFrame:
    return data.groupby([data["Date"].dt.to_period("M"), "Item Name"])["Transaction #"].count().unstack("Item Name")


def split_into_groups(n: int, unstacked_data) -> list:
    sorted_items = unstacked_data.sum().sort_values(ascending=False).index.tolist()
    group_size = len(sorted_items) // n
    return [sorted_items[i * group_size: len(sorted_items) if i == n - 1 else (i + 1) * group_size] for i in range(n)]


def filter_and_plot(data: pd.DataFrame, items: list, i: int) -> None:
    items = [item for item in items if item in data.columns]
    subset_data = data.loc[:, items]
    fig, ax = plt.subplots()
    for column in subset_data.columns:
        ax.plot(subset_data.index.to_timestamp(), subset_data[column].cumsum(), label=column)
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_minor_locator(mdates.WeekdayLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    plt.title("Cumulative Sales over time (Chart {})".format(i + 1), fontsize=22)
    plt.xlabel("Time", fontsize=16)
    plt.ylabel("Cumulative number of sales / month", fontsize=16)
    plt.legend(fontsize="large")


def main():
    data = read_data(__file__)
    unstacked_data = group_data(data)
    groups = split_into_groups(3, unstacked_data)
    for i, items in enumerate(groups):
        filter_and_plot(unstacked_data, items, i)
    plt.show()


if __name__ == "__main__":
    main()
