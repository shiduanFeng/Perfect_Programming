import pickle
import multiprocessing
from python_structured import *
from sqlang_structured import *

# 定义多进程处理Python查询的函数
def multipro_python_query(data_list):
    return [python_query_parse(line) for line in data_list]

# 定义多进程处理Python代码的函数
def multipro_python_code(data_list):
    return [python_code_parse(line) for line in data_list]

# 定义多进程处理Python上下文的函数
def multipro_python_context(data_list):
    result = []
    for line in data_list:
        if line == '-10000':
            result.append(['-10000'])
        else:
            result.append(python_context_parse(line))
    return result

# 定义多进程处理SQL查询的函数
def multipro_sqlang_query(data_list):
    return [sqlang_query_parse(line) for line in data_list]

# 定义多进程处理SQL代码的函数
def multipro_sqlang_code(data_list):
    return [sqlang_code_parse(line) for line in data_list]

# 定义多进程处理SQL上下文的函数
def multipro_sqlang_context(data_list):
    result = []
    for line in data_list:
        if line == '-10000':
            result.append(['-10000'])
        else:
            result.append(sqlang_context_parse(line))
    return result

# 定义解析函数，将数据列表分割为多个子列表，每个子列表包含split_num个元素
def parse(data_list, split_num, context_func, query_func, code_func):
    pool = multiprocessing.Pool()
    split_list = [data_list[i:i + split_num] for i in range(0, len(data_list), split_num)]
    results = pool.map(context_func, split_list)
    context_data = [item for sublist in results for item in sublist]
    print(f'context条数：{len(context_data)}')

    results = pool.map(query_func, split_list)
    query_data = [item for sublist in results for item in sublist]
    print(f'query条数：{len(query_data)}')

    results = pool.map(code_func, split_list)
    code_data = [item for sublist in results for item in sublist]
    print(f'code条数：{len(code_data)}')

    pool.close()
    pool.join()

    return context_data, query_data, code_data

# 定义主函数，处理语言类型、分割数、源文件路径、保存路径等参数
def main(lang_type, split_num, source_path, save_path, context_func, query_func, code_func):
    with open(source_path, 'rb') as f:
        corpus_lis = pickle.load(f)

    context_data, query_data, code_data = parse(corpus_lis, split_num, context_func, query_func, code_func)
    qids = [item[0] for item in corpus_lis]

    total_data = [[qids[i], context_data[i], code_data[i], query_data[i]] for i in range(len(qids))]

    with open(save_path, 'wb') as f:
        pickle.dump(total_data, f)

# 定义主程序入口
if __name__ == '__main__':
    # 定义文件路径
    staqc_python_path = '.ulabel_data/python_staqc_qid2index_blocks_unlabeled.txt'
    staqc_python_save = '../hnn_process/ulabel_data/staqc/python_staqc_unlabled_data.pkl'

    staqc_sql_path = './ulabel_data/sql_staqc_qid2index_blocks_unlabeled.txt'
    staqc_sql_save = './ulabel_data/staqc/sql_staqc_unlabled_data.pkl'

    # 执行主函数
    main(python_type, split_num, staqc_python_path, staqc_python_save, multipro_python_context, multipro_python_query, multipro_python_code)
    main(sqlang_type, split_num, staqc_sql_path, staqc_sql_save, multipro_sqlang_context, multipro_sqlang_query, multipro_sqlang_code)

    # 定义文件路径
    large_python_path = './ulabel_data/large_corpus/multiple/python_large_multiple.pickle'
    large_python_save = '../hnn_process/ulabel_data/large_corpus/multiple/python_large_multiple_unlable.pkl'

    large_sql_path = './ulabel_data/large_corpus/multiple/sql_large_multiple.pickle'
    large_sql_save = './ulabel_data/large_corpus/multiple/sql_large_multiple_unlable.pkl'

    # 执行主函数
    main(python_type, split_num, large_python_path, large_python_save, multipro_python_context, multipro_python_query, multipro_python_code)
    main(sqlang_type, split_num, large_sql_path, large_sql_save, multipro_sqlang_context, multipro_sqlang_query, multipro_sqlang_code)