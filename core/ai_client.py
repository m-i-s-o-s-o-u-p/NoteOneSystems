import os
import json

class AIClient:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        self.client = None
        
        # google-genai または google-generativeai の安全な読み込み
        if self.api_key:
            try:
                from google import genai
                self.client = genai.Client(api_key=self.api_key)
                self.sdk_type = "genai"
            except ImportError:
                try:
                    import google.generativeai as legacy_genai
                    legacy_genai.configure(api_key=self.api_key)
                    self.client = legacy_genai.GenerativeModel("gemini-1.5-flash")
                    self.sdk_type = "legacy"
                except ImportError:
                    print("Notice: google-genai package not installed yet. Running in demo simulation mode.")
                    self.client = None
            except Exception as e:
                print(f"Gemini Client Init Error: {e}")
                self.client = None

    def is_configured(self) -> bool:
        return bool(self.client and self.api_key)

    def generate_text(self, system_instruction: str, prompt: str, temperature: float = 0.7) -> str:
        """AIモデルによるテキスト生成"""
        if not self.is_configured():
            return None
        
        try:
            if hasattr(self, 'sdk_type') and self.sdk_type == "genai":
                from google.genai import types
                response = self.client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=system_instruction,
                        temperature=temperature,
                    )
                )
                return response.text
            elif hasattr(self, 'sdk_type') and self.sdk_type == "legacy":
                full_prompt = f"{system_instruction}\n\n{prompt}"
                response = self.client.generate_content(full_prompt)
                return response.text
        except Exception as e:
            print(f"API Call Failed: {e}")
            return None
