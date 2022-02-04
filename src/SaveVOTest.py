from utils.DataStore import DataStore


def main():
    print(DataStore().ReadVOs("./data/status.csv"))


if (__name__ == "__main__"):
    main()
