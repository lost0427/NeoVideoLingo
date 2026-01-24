import json
import os
import configparser
from openai import OpenAI

# --- 1. 路径初始化 ---
# 获取当前脚本所在的绝对路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def get_path(filename):
    """辅助函数：将文件名拼接为绝对路径"""
    return os.path.join(BASE_DIR, filename)

# --- 2. 读取配置 ---
config_path = get_path('config.ini')
if not os.path.exists(config_path):
    raise FileNotFoundError(f"❌ 找不到配置文件: {config_path}")

config = configparser.ConfigParser()
config.read(config_path, encoding='utf-8')

# 校验 Section
if 'openai' not in config.sections():
    raise KeyError("❌ config.ini 中缺失 [openai] 段落")

API_KEY = config.get('openai', 'api_key')
BASE_URL = config.get('openai', 'base_url')
MODEL = config.get('openai', 'model')
AUTO_DELETE = config.getboolean('settings', 'auto_delete_old_keys')

# 初始化客户端
client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

# 语言映射 (文件名 : 语言全名)
LANG_FILES = {
    "es.json": "Spanish",
    "fr.json": "French",
    "ja.json": "Japanese",
    "ru.json": "Russian",
    "zh-CN.json": "Simplified Chinese",
    "zh-HK.json": "Traditional Chinese (Hong Kong)"
}
MASTER_FILE = "en.json"

# --- 3. 核心逻辑 ---

def load_json(filename):
    path = get_path(filename)
    if not os.path.exists(path): return {}
    with open(path, 'r', encoding='utf-8') as f:
        try: return json.load(f)
        except: return {}

def save_json(filename, data):
    path = get_path(filename)
    with open(path, 'w', encoding='utf-8') as f:
        # ensure_ascii=False 确保非英文不被编码，indent=4 保持格式美观
        json.dump(data, f, ensure_ascii=False, indent=4)

def translate_batch(texts_dict, target_lang):
    if not texts_dict: return {}
    
    prompt = (
        f"You are a professional translator. Translate the following JSON values from English to {target_lang}. "
        "Keep the keys exactly the same. Return ONLY the translated JSON object without any explanation."
    )
    
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that outputs only valid JSON."},
                {"role": "user", "content": f"{prompt}\n\nJSON: {json.dumps(texts_dict)}"}
            ],
            response_format={ "type": "json_object" }
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        print(f"❌ 翻译失败 ({target_lang}): {e}")
        return {}

def sync_all():
    master_data = load_json(MASTER_FILE)
    if not master_data:
        print(f"⚠️ 基准文件 {MASTER_FILE} 未找到或为空，路径: {get_path(MASTER_FILE)}")
        return

    for filename, lang_name in LANG_FILES.items():
        print(f"正在处理 {filename}...")
        current_data = load_json(filename)
        
        # --- A. 自动删除旧 Key ---
        if AUTO_DELETE:
            original_keys = set(current_data.keys())
            # 只保留存在于 master_data 中的 key
            current_data = {k: v for k, v in current_data.items() if k in master_data}
            deleted_count = len(original_keys) - len(current_data)
            if deleted_count > 0:
                print(f"  🗑️ 已从 {filename} 中清理 {deleted_count} 条失效 Key")

        # --- B. 找出缺失的 Key 并翻译 ---
        missing_keys = {k: v for k, v in master_data.items() if k not in current_data}
        
        if missing_keys:
            print(f"  ✨ 发现 {len(missing_keys)} 条新内容，正在调用 AI ({MODEL})...")
            translated_part = translate_batch(missing_keys, lang_name)
            current_data.update(translated_part)
            save_json(filename, current_data)
            print(f"  ✅ {filename} 更新成功")
        elif AUTO_DELETE and deleted_count > 0:
            # 如果没有新增但有删除，也执行一次保存
            save_json(filename, current_data)
            print(f"  ✅ {filename} 已同步删除")
        else:
            print(f"  --- {filename} 已是最新")

if __name__ == "__main__":
    sync_all()