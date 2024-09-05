from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
from pydantic import BaseModel, ValidationError
import json
from llm_base import LLMConfig
from llm_portrait_creator import PortraitCreator, PortraitSettings
from llm_sculpture_creator import SculptureCreator, SculptureSettings
from unified_logging import backend_logger as logger

# 加载环境变量
load_dotenv()

app = FastAPI(title="Art Creation Assistant API", version="1.0.0")

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # 允许的源，在生产环境中应该更严格
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有方法
    allow_headers=["*"],  # 允许所有头
)

# 创建LLMConfig实例
llm_config = LLMConfig(api_key=os.getenv("OPENROUTER_API_KEY"))

# 创建PortraitCreator实例
portrait_creator = PortraitCreator(llm_config)

# 创建SculptureCreator实例
sculpture_creator = SculptureCreator(llm_config)

def clean_json_string(json_str):
    # 查找第一个 '{' 和最后一个 '}'，���保留这之间的内容
    start = json_str.find('{')
    end = json_str.rfind('}') + 1
    if start != -1 and end != -1:
        return json_str[start:end]
    return json_str


@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# 肖像画 Prompt 生成器
@app.post("/api/generate-portrait-elements")
async def generate_portrait_elements(portrait: PortraitSettings):
    try:
        logger.info(f"收到生成肖像元素的请求：{portrait}")
        elements = await portrait_creator.generate_elements(portrait)
        logger.info(f"成功生成肖像元素")
        return {"elements": elements}
    except ValidationError as e:
        logger.error(f"输入数据验证错误：{str(e)}")
        raise HTTPException(status_code=422, detail=f"无效的输入数据：{str(e)}")
    except Exception as e:
        logger.error(f"生成肖像元素时出错：{str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/reflect-on-portrait-elements")
async def reflect_on_portrait_elements(data: dict):
    try:
        logger.info(f"收到反思请求：{data}")
        concept = data.get('concept', '')
        elements = data.get('elements', '')

        reflected_elements = await portrait_creator.reflect_on_elements(concept, elements)
        logger.info(f"成功反思画作描述")

        return {"reflection": reflected_elements}
    except Exception as e:
        logger.error(f"反思画作描述时出错：{str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/generate-final-portrait-prompts")
async def generate_final_portrait_prompts(data: dict):
    try:
        logger.info(f"收到生成最终提示词的请求：{data}")
        prompts = await portrait_creator.generate_final_prompts(data['elements'])
        logger.info(f"成功生成最终提示词: {prompts}")

        # 解析 JSON 字符串为 Python 字典
        parsed_prompts = json.loads(prompts)
        return {"prompts": parsed_prompts}
    except json.JSONDecodeError as e:
        logger.error(f"解析提示词 JSON 时出错：{str(e)}")
        return {"error": "无效的提示词格式", "raw_prompts": prompts}
    except Exception as e:
        logger.error(f"生成最终提示词时出错：{str(e)}", exc_info=True)
        return {"error": str(e)}

# 雕塑 Prompt 生成器
@app.post("/api/generate-sculpture-portrait-elements")
async def generate_sculpture_portrait_elements(sculpture: SculptureSettings):
    try:
        logger.info(f"收到生成雕塑元素的请求：{sculpture}")
        elements = await sculpture_creator.generate_elements(sculpture)
        logger.info(f"成功生成雕塑元素")
        return {"elements": elements}
    except ValidationError as e:
        logger.error(f"输入数据验证错误：{str(e)}")
        raise HTTPException(status_code=422, detail=f"无效的输入数据：{str(e)}")
    except Exception as e:
        logger.error(f"生成雕塑元素时出错：{str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/reflect-on-sculpture-elements")
async def reflect_on_sculpture_elements(data: dict):
    try:
        logger.info(f"收到雕塑反思请求：{data}")
        concept = data.get('concept', '')
        elements = data.get('elements', '')

        reflected_elements = await sculpture_creator.reflect_on_elements(concept, elements)
        logger.info(f"成功反思雕塑描述")

        return {"reflection": reflected_elements}
    except Exception as e:
        logger.error(f"反思雕塑描述时出错：{str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/generate-final-sculpture-prompts")
async def generate_final_sculpture_prompts(data: dict):
    try:
        logger.info(f"收到生成最终雕塑提示词的请求：{data}")
        prompts = await sculpture_creator.generate_final_prompts(data['elements'])
        logger.info(f"成功生成最终雕塑提示词: {prompts}")

        # 解析 JSON 字符串为 Python 字典
        parsed_prompts = json.loads(prompts)
        return {"prompts": parsed_prompts}
    except json.JSONDecodeError as e:
        logger.error(f"解析雕塑提示词 JSON 时出错：{str(e)}")
        return {"error": "无效的雕塑提示词格式", "raw_prompts": prompts}
    except Exception as e:
        logger.error(f"生成最终雕塑提示词时出错：{str(e)}", exc_info=True)
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)