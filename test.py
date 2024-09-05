import re
import json

def main(http_response: str) -> str:
    def extract_key_variables(input_string):
        # 定义要提取的关键词和对应的变量名
        keywords = {
            "concept": r"'concept':\s*'([^']*)'",
            "主体": r"主体（Subject）\s*(.*?)(?=\n\n|$)",
            "Subject": r"Subject[）)]\s*(.*?)(?=\n\n|$)",
            "寓意": r"寓意（Meaning）\s*(.*?)(?=\n\n|$)",
            "Meaning": r"Meaning[）)]\s*(.*?)(?=\n\n|$)",
            "互动": r"互动与应答（Interaction）\s*(.*?)(?=\n\n|$)",
            "Interaction": r"Interaction[）)]\s*(.*?)(?=\n\n|$)",
            "风格": r"风格（Style）\s*(.*?)(?=\n\n|$)",
            "Style": r"Style[）)]\s*(.*?)(?=\n\n|$)",
            "质料": r"质料（Medium）\s*(.*?)(?=\n\n|$)",
            "Medium": r"Medium[）)]\s*(.*?)(?=\n\n|$)"
        }
        
        # 初始化结果字典
        result = {
            "concept": "",
            "subject": "",
            "meaning": "",
            "interaction": "",
            "style": "",
            "medium": ""
        }

        # 使用正则表达式提取内容
        for key, pattern in keywords.items():
            match = re.search(pattern, input_string, re.DOTALL | re.IGNORECASE)
            if match:
                if key == "concept":
                    result["concept"] = match.group(1).strip()
                elif key in ["主体", "Subject"]:
                    result["subject"] = match.group(1).strip()
                elif key in ["寓意", "Meaning"]:
                    result["meaning"] = match.group(1).strip()
                elif key in ["互动", "Interaction"]:
                    result["interaction"] = match.group(1).strip()
                elif key in ["风格", "Style"]:
                    result["style"] = match.group(1).strip()
                elif key in ["质料", "Medium"]:
                    result["medium"] = match.group(1).strip()

        return result

    # 解析 http_response
    data = json.loads(http_response)
    
    # 假设 LLM 的响应在 data['response'] 中
    llm_response = data.get('response', '')
    
    # 提取关键变量
    extracted_data = extract_key_variables(llm_response)
    
    # 返回符合 Dify 要求的格式
    return {
        'concept': extracted_data['concept'],
        'subject': extracted_data['subject'],
        'meaning': extracted_data['meaning'],
        'interaction': extracted_data['interaction'],
        'style': extracted_data['style'],
        'medium': extracted_data['medium']
    }