"""
Google Vertex AI Cover Generator
使用 Google Imagen 生成封面

需要：
- Google Cloud Service Account JSON
- 启用 Vertex AI API
- 项目ID和区域
"""

import os
import json
import base64
from datetime import datetime
from typing import Optional


class GoogleAICoverGenerator:
    """
    Google Vertex AI / Imagen 封面生成器
    
    模型：Imagen (Google)
    特点：高质量图像生成，企业级服务
    """
    
    def __init__(self, 
                 service_account_path: str = None,
                 project_id: str = None,
                 location: str = "us-central1"):
        """
        初始化
        
        Args:
            service_account_path: Service Account JSON 文件路径
            project_id: Google Cloud 项目ID
            location: 区域 (默认 us-central1)
        """
        self.service_account_path = service_account_path or os.getenv("GOOGLE_SERVICE_ACCOUNT_PATH")
        self.project_id = project_id or os.getenv("GOOGLE_PROJECT_ID")
        self.location = location or os.getenv("GOOGLE_LOCATION", "us-central1")
        
        if not self.service_account_path or not os.path.exists(self.service_account_path):
            raise ValueError("请提供有效的 Service Account JSON 文件路径")
        
        if not self.project_id:
            raise ValueError("请提供 Google Cloud 项目ID")
        
        # 加载凭证
        self.credentials = self._load_credentials()
    
    def _load_credentials(self):
        """加载 Service Account 凭证"""
        with open(self.service_account_path, 'r') as f:
            return json.load(f)
    
    def _get_access_token(self) -> str:
        """获取访问令牌"""
        from google.oauth2 import service_account
        from google.auth.transport.requests import Request
        
        credentials = service_account.Credentials.from_service_account_file(
            self.service_account_path,
            scopes=['https://www.googleapis.com/auth/cloud-platform']
        )
        
        credentials.refresh(Request())
        return credentials.token
    
    def generate(self, title: str, style: str = "professional") -> str:
        """
        生成封面图
        
        Args:
            title: 文章标题
            style: 风格 (professional/artistic/tech/minimal)
            
        Returns:
            图片本地路径
        """
        try:
            import requests
            
            # 构建提示词
            prompt = self._create_prompt(title, style)
            
            print(f"🎨 使用 Google Imagen 生成封面...")
            print(f"   标题: {title}")
            
            # 获取访问令牌
            access_token = self._get_access_token()
            
            # Vertex AI API 端点
            url = f"https://{self.location}-aiplatform.googleapis.com/v1/projects/{self.project_id}/locations/{self.location}/publishers/google/models/imagegeneration:predict"
            
            # 请求体
            payload = {
                "instances": [
                    {
                        "prompt": prompt
                    }
                ],
                "parameters": {
                    "sampleCount": 1,
                    "aspectRatio": "16:9",  # 横向封面
                    "guidanceScale": 7.5,   # 控制与提示词的匹配度
                    "seed": None            # 随机种子
                }
            }
            
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
            
            # 发送请求
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            
            data = response.json()
            
            # 解析返回的图片数据
            if "predictions" in data and len(data["predictions"]) > 0:
                # Imagen 返回 base64 编码的图片
                image_base64 = data["predictions"][0].get("bytesBase64Encoded")
                
                if image_base64:
                    # 解码并保存
                    img_data = base64.b64decode(image_base64)
                    img_path = f'/tmp/cover_google_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png'
                    
                    with open(img_path, 'wb') as f:
                        f.write(img_data)
                    
                    print(f"✅ Google Imagen 封面生成成功")
                    print(f"   路径: {img_path}")
                    return img_path
            
            raise Exception(f"API返回异常: {data}")
            
        except ImportError as e:
            raise ImportError(f"需要安装依赖: pip install google-auth google-auth-oauthlib requests ({e})")
        except Exception as e:
            print(f"❌ Google Imagen 生成失败: {e}")
            raise
    
    def _create_prompt(self, title: str, style: str) -> str:
        """创建 Imagen 提示词"""
        
        style_prompts = {
            "professional": """
Professional business/technology blog cover image.
Modern, clean, minimalist design.
Wide banner format, 16:9 aspect ratio.
Abstract or conceptual representation.
High quality, polished look.
Corporate color palette: blues, teals, professional tones.
No text, no watermarks, no logos.
            """,
            "artistic": """
Artistic and creative blog cover image.
Stylish, unique, eye-catching design.
Wide banner format, 16:9 aspect ratio.
Artistic interpretation with flowing shapes and colors.
Warm, inviting color palette.
No text, no watermarks, no logos.
            """,
            "tech": """
High-tech, futuristic blog cover image.
Digital, innovative, cutting-edge design.
Wide banner format, 16:9 aspect ratio.
Abstract technology elements, geometric patterns.
Cool colors: blues, cyans, electric accents.
No text, no watermarks, no logos.
            """,
            "minimal": """
Minimalist, elegant blog cover image.
Simple, clean, sophisticated design.
Wide banner format, 16:9 aspect ratio.
Subtle gradients, soft colors, negative space.
Neutral or pastel color palette.
No text, no watermarks, no logos.
            """
        }
        
        base_style = style_prompts.get(style, style_prompts["professional"])
        
        prompt = f"""
Create a cover image for a WeChat article titled: "{title}"

Theme: {title}
{base_style}

Mood: Professional, engaging, high quality.
        """.strip()
        
        return prompt


class MultiProviderCoverGenerator:
    """
    多提供商封面生成器
    
    自动选择最佳生成方案：
    1. Google Imagen (Vertex AI)
    2. OpenAI DALL-E 3
    3. 本地高级模板
    """
    
    def __init__(self, 
                 google_service_account: str = None,
                 google_project_id: str = None,
                 openai_api_key: str = None):
        """
        初始化多提供商生成器
        
        优先级：Google Imagen > OpenAI DALL-E > 本地模板
        """
        self.google_service_account = google_service_account or os.getenv("GOOGLE_SERVICE_ACCOUNT_PATH")
        self.google_project_id = google_project_id or os.getenv("GOOGLE_PROJECT_ID")
        self.openai_api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        
        # 检查可用的提供商
        self.available_providers = self._check_providers()
    
    def _check_providers(self) -> list:
        """检查可用的提供商"""
        providers = []
        
        # 检查 Google
        if (self.google_service_account and os.path.exists(self.google_service_account) and 
            self.google_project_id):
            providers.append("google")
        
        # 检查 OpenAI
        if self.openai_api_key:
            providers.append("openai")
        
        # 本地模板总是可用
        providers.append("local")
        
        return providers
    
    def generate(self, title: str, provider: str = "auto", style: str = "professional") -> str:
        """
        生成封面，自动选择最佳提供商
        
        Args:
            title: 文章标题
            provider: 指定提供商 (google/openai/local/auto)
            style: 风格
            
        Returns:
            图片路径
        """
        if provider == "auto":
            # 按优先级选择
            for prov in ["google", "openai", "local"]:
                if prov in self.available_providers:
                    provider = prov
                    break
        
        print(f"🎨 使用提供商: {provider.upper()}")
        
        if provider == "google":
            generator = GoogleAICoverGenerator(
                service_account_path=self.google_service_account,
                project_id=self.google_project_id
            )
            return generator.generate(title, style)
        
        elif provider == "openai":
            from .cover_generator import AdvancedCoverGenerator
            generator = AdvancedCoverGenerator(openai_api_key=self.openai_api_key)
            return generator.generate(title, style="ai")
        
        else:  # local
            from .cover_generator import AdvancedCoverGenerator
            generator = AdvancedCoverGenerator()
            return generator.generate(title, style="local")


# 快捷函数
def generate_cover_google(title: str, 
                          service_account_path: str = None,
                          project_id: str = None) -> str:
    """
    使用 Google Imagen 生成封面
    
    环境变量：
    - GOOGLE_SERVICE_ACCOUNT_PATH: Service Account JSON 路径
    - GOOGLE_PROJECT_ID: 项目ID
    """
    generator = GoogleAICoverGenerator(
        service_account_path=service_account_path,
        project_id=project_id
    )
    return generator.generate(title)
