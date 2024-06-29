import pickle
from collections import Counter

# 加载pickle文件
def load_pickle(filename):
    with open(filename, 'rb') as f:
        data = pickle.load(f, encoding='iso-8859-1')
    return data

# 根据qid将数据分为单一和多重数据
def split_data(total_data, qids):
    result = Counter(qids)
    total_data_single = []
    total_data_multiple = []
    for data in total_data:
        if result[data[0][0]] == 1:
            total_data_single.append(data)
        else:
            total_data_multiple.append(data)
    return total_data_single, total_data_multiple

# 处理staqc数据
def data_staqc_processing(filepath, save_single_path, save_multiple_path):
    with open(filepath, 'r') as f:
        total_data = eval(f.read())
    qids = [data[0][0] for data in total_data]
    total_data_single, total_data_multiple = split_data(total_data, qids)

    with open(save_single_path, "w") as f:
        f.write(str(total_data_single))
    with open(save_multiple_path, "w") as f:
        f.write(str(total_data_multiple))

# 处理large数据
def data_large_processing(filepath, save_single_path, save_multiple_path):
    total_data = load_pickle(filepath)
    qids = [data[0][0] for data in total_data]
    total_data_single, total_data_multiple = split_data(total_data, qids)

    with open(save_single_path, 'wb') as f:
        pickle.dump(total_data_single, f)
    with open(save_multiple_path, 'wb') as f:
        pickle.dump(total_data_multiple, f)

# 将未标记的单一数据标记为已标记
def single_unlabeled_to_labeled(input_path, output_path):
    total_data = load_pickle(input_path)
    labels = [[data[0], 1] for data in total_data]
    total_data_sort = sorted(labels, key=lambda x: (x[0], x[1]))
    with open(output_path, "w") as f:
        f.write(str(total_data_sort))

# 主程序
if __name__ == "__main__":
    # 定义文件路径
    staqc_python_path = './ulabel_data/python_staqc_qid2index_blocks_unlabeled.txt'
    staqc_python_single_save = './ulabel_data/staqc/single/python_staqc_single.txt'
    staqc_python_multiple_save = './ulabel_data/staqc/multiple/python_staqc_multiple.txt'
    # 处理staqc python数据
    data_staqc_processing(staqc_python_path, staqc_python_single_save, staqc_python_multiple_save)

    # 定义文件路径
    staqc_sql_path = './ulabel_data/sql_staqc_qid2index_blocks_unlabeled.txt'
    staqc_sql_single_save = './ulabel_data/staqc/single/sql_staqc_single.txt'
    staqc_sql_multiple_save = './ulabel_data/staqc/multiple/sql_staqc_multiple.txt'
    # 处理staqc sql数据
    data_staqc_processing(staqc_sql_path, staqc_sql_single_save, staqc_sql_multiple_save)

    # 定义文件路径
    large_python_path = './ulabel_data/python_codedb_qid2index_blocks_unlabeled.pickle'
    large_python_single_save = './ulabel_data/large_corpus/single/python_large_single.pickle'
    large_python_multiple_save = './ulabel_data/large_corpus/multiple/python_large_multiple.pickle'
    #