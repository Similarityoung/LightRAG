import json
from openai import OpenAI
from transformers import GPT2Tokenizer


def openai_complete_if_cache(
    model="gpt-4o", prompt=None, system_prompt=None, history_messages=[], **kwargs
) -> str:
    """
    调用 OpenAI API 生成文本。
    """
    openai_client = OpenAI()

    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.extend(history_messages)
    messages.append({"role": "user", "content": prompt})

    response = openai_client.chat.completions.create(
        model=model, messages=messages, **kwargs
    )
    return response.choices[0].message.content


# 加载 GPT-2 tokenizer
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")


def get_summary(context, tot_tokens=2000):
    """
    截取文本的开头和结尾部分作为摘要，以适应 token 限制。
    """
    tokens = tokenizer.tokenize(context)
    half_tokens = tot_tokens // 2

    # 获取开头和结尾的 token
    start_tokens = tokens[1000 : 1000 + half_tokens]
    end_tokens = tokens[-(1000 + half_tokens) : 1000]

    summary_tokens = start_tokens + end_tokens
    summary = tokenizer.convert_tokens_to_string(summary_tokens)

    return summary


clses = ["agriculture"]
for cls in clses:
    # 读取去重后的上下文数据
    with open(f"../datasets/unique_contexts/{cls}_unique_contexts.json", mode="r") as f:
        unique_contexts = json.load(f)

    # 生成每个上下文的摘要
    summaries = [get_summary(context) for context in unique_contexts]

    total_description = "\n\n".join(summaries)

    # 构建 Prompt，要求 LLM 生成用户、任务和问题
    prompt = f"""
    Given the following description of a dataset:

    {total_description}

    Please identify 5 potential users who would engage with this dataset. For each user, list 5 tasks they would perform with this dataset. Then, for each (user, task) combination, generate 5 questions that require a high-level understanding of the entire dataset.

    Output the results in the following structure:
    - User 1: [user description]
        - Task 1: [task description]
            - Question 1:
            - Question 2:
            - Question 3:
            - Question 4:
            - Question 5:
        - Task 2: [task description]
            ...
        - Task 5: [task description]
    - User 2: [user description]
        ...
    - User 5: [user description]
        ...
    """

    # 调用 LLM 生成结果
    result = openai_complete_if_cache(model="gpt-4o", prompt=prompt)

    # 将生成的问题保存到文件
    file_path = f"../datasets/questions/{cls}_questions.txt"
    with open(file_path, "w") as file:
        file.write(result)

    print(f"{cls}_questions written to {file_path}")
