def merge_files(file_paths, output_path):
    merged_data = []
    for file_path in file_paths:
        with open(file_path, 'r',encoding="utf-8") as file:
            # 跳过标题行
            for line in file:
                # 获取特定列数据
                merged_data.append(line)

    # 写入合并后的数据到新文件
    with open(output_path, 'w',encoding="utf-8") as output_file:
        output_file.write('\n'.join(merged_data))

# 调用函数
file_paths = ['news.txt', 'weapons.txt']
output_path = 'merged_data.txt'
merge_files(file_paths, output_path)