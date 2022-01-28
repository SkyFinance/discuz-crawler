from data_store.DataStore import DataStore
from vo.PostStatus import PostStatus

def main():
    postStatus = PostStatus()
    print(DataStore().ReadVOs("./data/status.csv"))
if(__name__ == "__main__"):
    main()