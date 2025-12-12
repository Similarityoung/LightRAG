import re
import json
from lightrag import LightRAG, QueryParam
from lightrag.utils import always_get_an_event_loop


def extract_queries(file_path):
    """
    从生成的问题文件中提取问题文本。
    """
    with open(file_path, "r") as f:
        data = f.read()

    data = data.replace("**", "")

    # 使用正则表达式提取问题
    queries = re.findall(r"- Question \d+: (.+)", data)

    return queries


async def process_query(query_text, rag_instance, query_param):
    """
    使用 LightRAG 实例处理单个查询。
    """
    try:
        result = await rag_instance.aquery(query_text, param=query_param)
        return {"query": query_text, "result": result}, None
    except Exception as e:
        return None, {"query": query_text, "error": str(e)}


def run_queries_and_save_to_json(
    queries, rag_instance, query_param, output_file, error_file
):
    """
    运行所有查询并将结果保存到 JSON 文件。
    """
    loop = always_get_an_event_loop()

    with (
        open(output_file, "a", encoding="utf-8") as result_file,
        open(error_file, "a", encoding="utf-8") as err_file,
    ):
        result_file.write("[\n")
        first_entry = True

        for query_text in queries:
            # 执行查询
            result, error = loop.run_until_complete(
                process_query(query_text, rag_instance, query_param)
            )

            if result:
                if not first_entry:
                    result_file.write(",\n")
                json.dump(result, result_file, ensure_ascii=False, indent=4)
                first_entry = False
            elif error:
                json.dump(error, err_file, ensure_ascii=False, indent=4)
                err_file.write("\n")

        result_file.write("\n]")


if __name__ == "__main__":
    cls = "agriculture"
    mode = "hybrid"
    WORKING_DIR = f"../{cls}"

    # 初始化 LightRAG
    rag = LightRAG(working_dir=WORKING_DIR)
    # 设置查询参数（模式：混合检索）
    query_param = QueryParam(mode=mode)

    # 提取问题并运行查询
    queries = extract_queries(f"../datasets/questions/{cls}_questions.txt")
    run_queries_and_save_to_json(
        queries, rag, query_param, f"{cls}_result.json", f"{cls}_errors.json"
    )
