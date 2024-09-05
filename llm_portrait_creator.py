from typing import Dict, Any, List, Optional
from pydantic import BaseModel
import json
import re
from llm_base import LLMBase, LLMConfig

class PortraitSettings(BaseModel):
    concept: str
    mainSubject: Optional[str] = None
    gender: Optional[str] = None
    age: Optional[str] = None
    ethnicity: Optional[str] = None
    hairStyle: Optional[str] = None
    expression: Optional[str] = None
    clothing: Optional[str] = None
    background: Optional[str] = None
    composition: Optional[str] = None
    lighting: Optional[str] = None
    additionalDetails: Optional[str] = None
    artStyle: Optional[str] = None
    negativePrompt: Optional[str] = None
    seed: Optional[int] = 0
    size: Optional[str] = "1024x1024"
    steps: Optional[int] = 40
    samples: Optional[int] = 2
    cfg_scale: Optional[float] = 7.0
    model_type: Optional[int] = 2
    style_preset: Optional[str] = None
    useWeights: Optional[bool] = False

class PortraitCreator(LLMBase):
    def __init__(self, config: LLMConfig):
        super().__init__(config)  # Call the parent class constructor

    async def generate_elements_old(self, input_data: PortraitSettings) -> str:
        system_message = """
        你是一位艺术史学家，擅长使用 Michael Baxandall 的"The period eye"（时代之眼）透视艺术作品，即用文字阐释艺术作品。
        你的任务是根据给定的肖像概念及细节，创建一个结构化的描述，全面阐释肖像作品。
        """

        user_message = f"""
        肖像画作的概念及基本设定如下：
        - 画作概念：{input_data.concept}
        - 画作主体: {input_data.mainSubject or '肖像'}
        - 性别：{input_data.gender or '未指定'}
        - 年龄：{input_data.age or '未指定'}
        - 种族：{input_data.ethnicity or '未指定'}
        - 发型：{input_data.hairStyle or '未指定'}
        - 表情：{input_data.expression or '未指定'}
        - 服装：{input_data.clothing or '未指定'}
        - 背景：{input_data.background or '未指定'}
        - 构图：{input_data.composition or '未指定'}
        - 光线：{input_data.lighting or '未指定'}
        - 额外细节：{input_data.additionalDetails or '未指定'}
        - 艺术风格：{input_data.artStyle or '未指定'}

        肖像画作的技术参数及取值如下：
        - seed: {input_data.seed or '未指定'}
        - width: {input_data.size.split('x')[0] if input_data.size else '未指定'}
        - height: {input_data.size.split('x')[1] if input_data.size else '未指定'}
        - steps: {input_data.steps or '未指定'}
        - samples: {input_data.samples or '未指定'}
        - cfg_scale: {input_data.cfg_scale or '未指定'}
        - model_type: {input_data.model_type or '未指定'}
        - style_preset: {input_data.style_preset or '未指定'}

        请基于画作的概念和设定，生成肖像画作品的结构化描述，包括：
        - 主体（subject）：将画作概念表现为人物肖像。
        - 寓意（meaning）：要传达何种文化和社会含义。
        - 互动与应答（interaction）：要将画作交付给谁？试图回应他们的何种期望、需求和挑战。
        - 风格（style）：画作的形式特征。可简化为艺术流派或艺术家风格，如古典主义风格，达达主义的 Marcel Duchamp 风格等。
        - 质料（medium）：完成画作涉及的物理材料和工艺手段。如摄影、油画、插画、雕塑、艺术品、纸上作品、3D 等。
        - 技术执行（technicalExecution）：合并参数及取值，跳过“未指定”的参数。格式如：width:1024 height:1024 steps:40 samples:2 cfg_scale:7.0 model_type:2 style_preset:"digital-art" 。 
        """

        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ]

        try:
            self.logger.info(f"为概念生成肖像描述：{input_data.concept}")
            response = await self.call_llm(messages)
            self.logger.info("成功生成肖像描述")
            return response
        except Exception as e:
            self.logger.error(f"生成肖像描述时出错：{e}", exc_info=True)
            raise
    
    async def generate_elements(self, input_data: PortraitSettings) -> str:
        system_message = """
        你是一位艺术史学家，擅长使用 Michael Baxandall 的"The period eye"（时代之眼）透视艺术作品，即用文字阐释艺术作品。
        你的任务是根据给定的肖像概念及细节，创建一个结构化的描述，全面阐释肖像作品。
        """

        user_message = f"""
        肖像画作的概念及基本设定如下：
        - 创作概念：{input_data.concept}
        - 表现形式: {input_data.mainSubject or '肖像'}
        - 性别：{input_data.gender or '未指定'}
        - 年龄：{input_data.age or '未指定'}
        - 种族：{input_data.ethnicity or '未指定'}
        - 发型：{input_data.hairStyle or '未指定'}
        - 表情：{input_data.expression or '未指定'}
        - 服装：{input_data.clothing or '未指定'}
        - 背景：{input_data.background or '未指定'}
        - 构图：{input_data.composition or '未指定'}
        - 光线：{input_data.lighting or '未指定'}
        - 额外细节：{input_data.additionalDetails or '未指定'}
        - 艺术风格：{input_data.artStyle or '未指定'}

        请基于画作的概念和设定，生成肖像画作品的结构化描述，包括：
        - 主体（subject）：将画作概念表现为人物肖像。
        - 寓意（meaning）：要传达何种文化和社会含义。
        - 互动与应答（interaction）：要将画作交付给谁？试图回应他们的何种期望、需求和挑战。
        - 风格（style）：画作的形式特征。可简化为艺术流派或艺术家风格，如古典主义风格，达达主义的 Marcel Duchamp 风格等。
        - 质料（medium）：完成画作涉及的物理材料和工艺手段。如摄影、油画、插画、雕塑、艺术品、纸上作品、3D 等。
        """

        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ]

        try:
            self.logger.info(f"为概念生成肖像描述：{input_data.concept}")
            response = await self.call_llm(messages)
            self.logger.info("成功生成肖像描述")
            return response
        except Exception as e:
            self.logger.error(f"生成肖像描述时出错：{e}", exc_info=True)
            raise

    async def reflect_on_elements(self, concept: str, elements: str) -> dict:
        system_message = """
        你是一位艺术史大师，擅长使用 Michael Baxandall 的"The period eye"（时代之眼）透视艺术作品，即用文字阐释艺术。
        你的任务是分析给定的肖像画概念及其描述，反思描述对画作概念的表现效果，进而保留或更新画作描述，增强画作的表现力和艺术感。
        """

        user_message = f"""        
        画作概念：{concept}
        画作描述：
        {elements}

        请审视画作描述，确保每项描述均能凸显画作概念的表现力和艺术感。更新后的画作描述格式如下：
        {{
            "concept": "画作概念原文",
            "elements": {{
                "subject": "人物的姿态、表情、眼神和衣着等关键特征",
                "meaning": "肖像画所象征的深层含义，包括文化、社会或个人寓意",
                "interaction": "画作的目标受众，以及它是如何回应社会需求的",
                "style": "艺术风格、技法特点，包括构图、色彩运用、光影处理等",
                "medium": "创作材料，包括画布类型、颜料种类、镜头型号、保存状况等"
            }}
        }}
        """

        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ]

        try:
            self.logger.info("反思肖像描述")
            response = await self.call_llm(messages)
            self.logger.info(f"完成反思: {response}")

            # 使用新方法格式化 LLM 响应
            formatted_response = self.format_llm_response(response)
            
            return formatted_response
        except Exception as e:
            self.logger.error(f"反思肖像描述时出错：{e}", exc_info=True)
            return {"error": "处理过程中出现未知错误", "details": str(e)}

    async def generate_final_prompts(self, elements: str) -> str:
        system_message = """
        你是一位擅长应用 Stable Diffusion 进行视觉创作的艺术家。
        你的任务是提炼给定的画作描述，创作 SD 提示词，供 SD 生成富有表现力和艺术感的肖像作品。
        """

        user_message = f"""
        提炼以下画作描述，生成符合 SD 语法的精简提示词。

        画作描述：
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

    async def generate_final_prompts_other(self, elements: str) -> str:
        system_message = """
        你是一位擅长应用 Stable Diffusion 进行视觉创作的艺术家。你的任务是根据给定的画作描述，生成符合 SD 语法的简洁提示词及必要的技术参数，用于生成高质量的图像。请确保提示词简短精准，仅包含必要信息。
        
        响应应简洁明了，并避免冗长。保持提示词简短（最多150个字符），避免不必要的冗余描述。输出应为 SD 模型能直接使用的格式。
        """

        user_message = f"""
        根据以下画作描述，生成符合 SD 语法的简洁提示词及技术参数：

        画作描述：
        {elements}

        响应格式：
        {{
            "en": "英文提示词及技术参数",
            "zh": "中文提示词及技术参数"
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

    async def generate(self, input_data: PortraitSettings) -> str:
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