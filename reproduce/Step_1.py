import os
import json
import time
import asyncio

from lightrag import LightRAG


def insert_text(rag, file_path):
    """
    将文件中的文本数据插入到 LightRAG 实例中。
    """
    with open(file_path, mode="r") as f:
        unique_contexts = json.load(f)

    retries = 0
    max_retries = 3
    while retries < max_retries:
        try:
            # 尝试插入数据
            rag.insert(unique_contexts)
            break
        except Exception as e:
            retries += 1
            print(f"Insertion failed, retrying ({retries}/{max_retries}), error: {e}")
            time.sleep(10)
    if retries == max_retries:
        print("Insertion failed after exceeding the maximum number of retries")


cls = "agriculture"
WORKING_DIR = f"../{cls}"

# 如果工作目录不存在，则创建
if not os.path.exists(WORKING_DIR):
    os.mkdir(WORKING_DIR)


async def initialize_rag():
    """
    初始化 LightRAG 实例。
    """
    rag = LightRAG(working_dir=WORKING_DIR)

    await rag.initialize_storages()  # 自动初始化 pipeline_status
    return rag


def main():
    # 初始化 RAG 实例
    rag = asyncio.run(initialize_rag())
    # 插入数据
    insert_text(rag, f"../datasets/unique_contexts/{cls}_unique_contexts.json")


if __name__ == "__main__":
    main()
