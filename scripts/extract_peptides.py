import os
import pandas as pd
from Bio import SeqIO

# 目标文件夹和输出文件名
target_folder = "03.ymlt"
output_file = "LAB_LAN_peptide.xlsx"

# 初始化DataFrame来存储结果
data = {
    "File_Name": [],
    "Core_Sequence": [],
    "Leader_Sequence": []
}

# 遍历目标文件夹下的所有 .gbk 文件
for file_name in os.listdir(target_folder):
    if file_name.endswith(".gbk"):
        file_path = os.path.join(target_folder, file_name)
        for record in SeqIO.parse(file_path, "genbank"):
            for feature in record.features:
                if feature.type == "CDS_motif":
                    if 'prepeptide' in feature.qualifiers:
                        if feature.qualifiers['prepeptide'][0] == "core":
                            core_seq = feature.qualifiers.get('core_sequence', [""])[0]
                            leader_seq = feature.qualifiers.get('leader_sequence', [""])[0]
                            
                            # 存储到 DataFrame
                            data["File_Name"].append(file_name)
                            data["Core_Sequence"].append(core_seq)
                            data["Leader_Sequence"].append(leader_seq)

# 转换为 DataFrame
df = pd.DataFrame(data)

# 导出到 Excel 文件
df.to_excel(output_file, index=False)

print(f"数据已成功导出到 {output_file}")
