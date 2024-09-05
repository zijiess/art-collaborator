# 艺术创作助手开发环境总结

## 1. 概述
本项目是借助AI生成艺术作品的Web应用程序，旨在辅助非专业人士创作艺术作品。它由Python后端API和React前端组成，采用现代Web开发实践和AI集成。

## 2. 技术栈

### 2.1 后端
- **语言**: Python
  - 原因：Python具有丰富的AI和机器学习库，易于学习和使用。
- **框架**: FastAPI
  - 原因：FastAPI性能高，易于使用，并提供自动API文档。
- **AI集成**: Openrouter API（与OpenAI的API兼容）
  - 原因：Openrouter提供了对多个AI模型的访问，增加了灵活性。
- **主要依赖**:
  - fastapi：用于构建高性能的API
  - uvicorn：ASGI服务器，用于运行FastAPI应用
  - python-dotenv：用于管理环境变量
  - openai：用于与Openrouter API交互

### 2.2 前端
- **框架**: Next.js 13+（使用App Router）
  - 原因：Next.js提供了服务器端渲染和静态站点生成，优化了性能和SEO。
- **语言**: JavaScript (React)
  - 原因：React是一个流行的、高效的UI库，具有大型社区支持。
- **样式**: Tailwind CSS
  - 原因：Tailwind CSS提供了快速开发、一致性设计和高度可定制性。
- **主要依赖**:
  - React：用于构建用户界面
  - Axios：用于进行API调用
  - Tailwind CSS：用于快速样式设计

## 3. API集成
- 使用Openrouter API作为各种AI模型的代理
- 配置使用模型："openai/gpt-4o-mini-2024-07-18"（可自定义）
  - 原因：这个模型提供了良好的性能和成本平衡，适合生成创意提示。

## 4. 开发设置
1. 后端运行在 `http://localhost:8000`
2. 前端运行在 `http://localhost:3000`
3. 环境变量通过 `.env` 文件管理
   - 原因：这种方式可以安全地管理敏感信息，并易于在不同环境中配置。

## 5. 主要功能
- 用于生成艺术提示的RESTful API端点
- 基于React的用户界面，用于输入想法和显示生成的提示
- 使用Tailwind CSS的响应式现代UI

## 6. 部署考虑
- 后端和前端是分离的，可以独立部署
  - 原因：这种架构提高了灵活性和可扩展性。
- 为本地开发配置了CORS；生产环境需要调整
- 通过环境变量管理API密钥和敏感数据

## 7. 版本控制
- 假定使用Git进行版本控制（在提供的说明中未明确设置）
  - 原因：Git是最广泛使用的版本控制系统，适合协作开发。

## 8. 组件选择理由总结
1. **FastAPI**: 选择FastAPI是因为它提供了高性能、易用性和自动文档生成，这对于快速开发和维护API非常有利。
2. **Next.js**: Next.js提供了服务器端渲染和静态站点生成，这对于提高应用性能和搜索引擎优化很有帮助。
3. **Tailwind CSS**: Tailwind CSS允许快速构建自定义设计，无需离开HTML，大大提高了开发效率。
4. **Openrouter API**: 使用Openrouter API使得我们可以灵活地访问多个AI模型，而不局限于单一提供商。
5. **React**: React的组件化思想和虚拟DOM使得构建复杂的用户界面变得更加简单和高效。

## 9. 操作日志

### 9.1 后端设置 (Python with FastAPI and Openrouter)

1. 创建项目目录:
   ```bash
   mkdir art-creation-assistant
   cd art-creation-assistant
   ```

2. 设置虚拟环境:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. 安装所需包:
   ```bash
   pip install fastapi uvicorn python-dotenv openai
   ```

4. 创建 `main.py` 文件:
   ```python
   from fastapi import FastAPI
   from fastapi.middleware.cors import CORSMiddleware
   from pydantic import BaseModel
   from openai import OpenAI
   from dotenv import load_dotenv
   import os

   load_dotenv()

   app = FastAPI()

   # Configure CORS
   app.add_middleware(
       CORSMiddleware,
       allow_origins=["http://localhost:3000"],
       allow_credentials=True,
       allow_methods=["*"],
       allow_headers=["*"],
   )

   # Configure OpenAI client with Openrouter
   client = OpenAI(
       base_url="https://openrouter.ai/api/v1",
       api_key=os.getenv("OPENROUTER_API_KEY"),
   )

   class PromptRequest(BaseModel):
       prompt: str

   @app.post("/generate")
   async def generate_art_prompt(request: PromptRequest):
       completion = client.chat.completions.create(
           extra_headers={
               "HTTP-Referer": "http://localhost:3000",  # Replace with your actual site URL in production
               "X-Title": "Art Creation Assistant",  # Your app name
           },
           model="openai/gpt-4o-mini-2024-07-18",  # You can change this to your preferred model
           messages=[
               {
                   "role": "system",
                   "content": "You are an AI assistant specialized in generating creative art prompts."
               },
               {
                   "role": "user",
                   "content": f"Generate an art prompt based on: {request.prompt}"
               },
           ],
       )
       return {"generated_prompt": completion.choices[0].message.content}

   if __name__ == "__main__":
       import uvicorn
       uvicorn.run(app, host="0.0.0.0", port=8000)
   ```

5. 创建 `.env` 文件:
   ```
   OPENROUTER_API_KEY=your_api_key_here
   ```

### 9.2 前端设置
前端设置保持与之前版本相同。

### 9.3 运行应用程序

1. 启动后端服务器:
   ```bash
   cd art-creation-assistant
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   python main.py
   ```

2. 在新终端中启动前端开发服务器:
   ```bash
   cd frontend
   npm run dev
   ```

3. 在浏览器中访问 `http://localhost:3000` 使用应用程序。