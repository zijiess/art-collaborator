from typing import Dict, Any, List, Optional
from pydantic import BaseModel
import json
import re
from llm_base import LLMBase, LLMConfig

class SculptureSettings(BaseModel):
    concept: str
    mainSubject: Optional[str] = None
    material: Optional[str] = None
    size: Optional[str] = None
    style: Optional[str] = None
    texture: Optional[str] = None
    baseOrPedestal: Optional[str] = None
    installationEnvironment: Optional[str] = None
    additionalDetails: Optional[str] = None
    negativePrompt: Optional[str] = None
    seed: Optional[int] = -1
    steps: Optional[int] = 40
    samples: Optional[int] = 2
    cfg_scale: Optional[float] = 7.0
    model_type: Optional[int] = 2

class SculptureCreator(LLMBase):
    def __init__(self, config: LLMConfig):
        super().__init__(config)

    async def generate_elements(self, input_data: SculptureSettings) -> str:
        system_message = """
        你是一位艺术史学家，擅长使用 Michael Baxandall 的"The period eye"（时代之眼）透视艺术作品，特别是雕塑作品。
        你的任务是根据给定的概念及细节设定，创建一个结构化的描述，全面阐释雕塑作品。
        """

        user_message = f"""
        雕塑作品的创作概念及设定如下：
        - 创作概念：{input_data.concept}
        - 表现形式：{input_data.mainSubject or '雕塑'}
        - 材料：{input_data.material or '未指定'}
        - 尺寸：{input_data.size or '未指定'}
        - 风格：{input_data.style or '未指定'}
        - 质地：{input_data.texture or '未指定'}
        - 底座或基座：{input_data.baseOrPedestal or '未指定'}
        - 安装环境：{input_data.installationEnvironment or '未指定'}
        - 额外细节：{input_data.additionalDetails or '未指定'}

        请基于雕塑的概念和设定，生成雕塑作品的结构化描述，包括：
        - 主体（subject）：将概念表现为雕塑作品。突出主要对象。
        - 寓意（meaning）：要传达何种文化和社会含义。
        - 互动与应答（interaction）：作品的潜在买家是谁？试图回应何种期望、需求和挑战。
        - 风格（style）：作品的形式特征。可简化为艺术流派或艺术家风格。如古希腊风格，雕塑家 Myron 风格等。
        - 质料（medium）：完成作品涉及的物理材料（如石材、金属、陶瓷、玻璃、混凝土、聚合物、冰、沙、水、空气等）和工艺手段（如雕刻、塑造、铸造、组合、焊接、浮雕等）。
        """

        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ]

        try:
            self.logger.info(f"为概念生成雕塑描述：{input_data.concept}")
            response = await self.call_llm(messages)
            self.logger.info("成功生成雕塑描述")
            return response
        except Exception as e:
            self.logger.error(f"生成雕塑描述时出错：{e}", exc_info=True)
            raise

    async def reflect_on_elements(self, concept: str, elements: str) -> dict:
        system_message = """
        你是一位艺术史大师，擅长使用 Michael Baxandall 的"The period eye"（时代之眼）透视艺术作品，即用文字阐释艺术。你的任务是分析给定的创作概念及其描述，反思描述对创作概念的表现效果，进而保留或更新雕塑作品的描述，增强其表现力和艺术感。
        """

        user_message = f"""        
        创作概念：{concept}
        作品描述：
        {elements}

        请审视作品描述，确保每项描述均能凸显雕塑概念的表现力和艺术感。更新后的作品描述格式如下：
        {{
            "concept": "创作概念原文",
            "elements": {{
                "subject": "作品的主体、尺寸、比例、姿态、表情、眼神和衣着等关键特征",
                "meaning": "雕塑所象征的深层含义，包括文化、社会或个人寓意",
                "interaction": "作品的潜在买家，以及它是如何回应买家需求的",
                "style": "艺术风格、技法特点，包括形态处理、质感表现等",
                "medium": "创作材料，包括主要材质、辅助材料、加工工艺等"
            }}
        }}
        """

        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ]

        try:
            self.logger.info("反思雕塑描述")
            response = await self.call_llm(messages)
            self.logger.info(f"完成反思: {response}")

            # 使用新方法格式化 LLM 响应
            formatted_response = self.format_llm_response(response)
            
            return formatted_response
        except Exception as e:
            self.logger.error(f"反思雕塑描述时出错：{e}", exc_info=True)
            return {"error": "处理过程中出现未知错误", "details": str(e)}

    async def generate_final_prompts(self, elements: str) -> str:
        system_message = """
        你是一位擅长应用 Stable Diffusion 进行视觉创作的艺术家，特别专注于生成雕塑作品。
        你的任务是提炼给定的雕塑描述，创作 SD 提示词，供 SD 生成富有表现力和艺术感的雕塑作品。
        """

        user_message = f"""
        提炼以下雕塑描述，生成符合 SD 语法的精简提示词。

        作品描述：
        {elements}

        响应格式：
        {{
            "en_prompt": "英文提示词",
            "zh_prompt": "中文提示词"
        }}
        """

        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ]

        try:
            self.logger.info("生成最终提示词...")
            response = await self.call_llm(messages)
            self.logger.info(f"成功生成最终提示词: {response}")

            # 使用新方法格式化 LLM 响应
            formatted_response = self.format_llm_response(response)

            return json.dumps(formatted_response)
        except Exception as e:
            self.logger.error(f"生成最终提示词时出错：{e}", exc_info=True)
            return json.dumps({"error": str(e)})

    async def generate(self, input_data: SculptureSettings) -> str:
        # 此方法保留向后兼容性
        elements = await self.generate_elements(input_data)
        reflected_elements = await self.reflect_on_elements(input_data.concept, elements)
        final_prompts = await self.generate_final_prompts(reflected_elements)
        return final_prompts

    def format_llm_response(self, response: str) -> dict:
        """
        格式化 LLM 返回的响应，确保它是一个有效的 JSON 对象。
        """
        # 移除可能的 markdown 代码块标记
        response = re.sub(r'```json\s*', '', response)
        response = re.sub(r'\s*```', '', response)

        # 尝试直接解析 JSON
        try:
            parsed_response = json.loads(response)
            if isinstance(parsed_response, dict) and ('en_prompt' in parsed_response or 'zh_prompt' in parsed_response):
                return {
                    'en': parsed_response.get('en_prompt', ''),
                    'zh': parsed_response.get('zh_prompt', '')
                }
            return parsed_response
        except json.JSONDecodeError:
            pass

        # 如果直接解析失败，尝试提取并解析嵌套的 JSON
        try:
            match = re.search(r'\{.*\}', response, re.DOTALL)
            if match:
                parsed_response = json.loads(match.group())
                if isinstance(parsed_response, dict) and ('en_prompt' in parsed_response or 'zh_prompt' in parsed_response):
                    return {
                        'en': parsed_response.get('en_prompt', ''),
                        'zh': parsed_response.get('zh_prompt', '')
                    }
                return parsed_response
        except json.JSONDecodeError:
            pass

        # 如果仍然失败，尝试将响应转换为字典格式
        cleaned_response = re.sub(r'(\w+):', r'"\1":', response)
        cleaned_response = cleaned_response.replace("'", '"')
        try:
            parsed_response = json.loads(f'{{{cleaned_response}}}')
            if isinstance(parsed_response, dict) and ('en_prompt' in parsed_response or 'zh_prompt' in parsed_response):
                return {
                    'en': parsed_response.get('en_prompt', ''),
                    'zh': parsed_response.get('zh_prompt', '')
                }
            return parsed_response
        except json.JSONDecodeError:
            pass

        # 如果所有尝试都失败，返回原始响应作为字符串值的字典
        return {"raw": response}