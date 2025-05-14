import json
import pandas as pd
import os
import glob
import argparse

def extract_region_json(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)

    file_stem = os.path.splitext(os.path.basename(json_file))[0]

    try:
        features = data["records"][0]["features"]
        region_feature = next(f for f in features if f["type"] == "region")
        region_type = region_feature["qualifiers"]["product"][0]
        region_location = region_feature["location"].strip("[]").split(":")
        region_from = int(region_location[0])
        region_to = int(region_location[1])

        # 相似簇信息
        cluster_data = data["records"][0]["modules"]["antismash.modules.clusterblast"]
        result_block = cluster_data["knowncluster"]["results"][0]["ranking"][0]
        most_similar_cluster = result_block[0]["description"]
        similarity = result_block[1]["similarity"]

        # 默认空值
        accession = "NA"
        organism = "NA"

        # 尝试 RegionToRegion_RiQ → ProtoToRegion_RiQ
        region_block = cluster_data["knowncluster"]["results"][0]
        for key in ["RegionToRegion_RiQ", "ProtoToRegion_RiQ"]:
            if key in region_block and "reference_regions" in region_block[key]:
                ref_region = region_block[key]["reference_regions"]
                ref_id = list(ref_region.keys())[0]
                accession = ref_region[ref_id].get("accession", "NA")
                organism = ref_region[ref_id].get("organism", "NA")
                break  # 成功就跳出

        return {
            "Region": file_stem,
            "Type": region_type,
            "From": region_from,
            "To": region_to,
            "Most similar known cluster": most_similar_cluster,
            "Similarity": f"{similarity}%",
            "Accession": accession,
            "Organism": organism
        }

    except Exception as e:
        print(f"❗ 跳过文件 {file_stem}: {e}")
        return None

def main(input_folder, output_excel):
    json_files = glob.glob(os.path.join(input_folder, "*.region*.json"))
    all_results = []

    for json_file in json_files:
        result = extract_region_json(json_file)
        if result:
            all_results.append(result)

    df = pd.DataFrame(all_results)
    df.to_excel(output_excel, index=False)
    print(f"✅ 共提取 {len(all_results)} 个区域，结果已保存至: {output_excel}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract antiSMASH region-level JSONs with fallback")
    parser.add_argument("-i", "--input", required=True, help="包含多个 .region*.json 文件的目录")
    parser.add_argument("-o", "--output", required=True, help="输出 Excel 文件路径")
    args = parser.parse_args()
    main(args.input, args.output)
