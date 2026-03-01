import os
import configparser
from concurrent.futures import ThreadPoolExecutor, as_completed
from openai import OpenAI

# --- 1. 路径初始化 ---
# 获取当前脚本所在的绝对路径 /translations
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# 项目根目录
PROJECT_ROOT = os.path.dirname(BASE_DIR)

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

# 初始化客户端
client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

# 语言映射 (文件名后缀 : 语言全名)
# 目标文件将命名为 README.<后缀>.md
TARGET_LANGS = {
    "en": "English",
    "es": "Spanish",
    "fr": "French",
    "ja": "Japanese",
    "ru": "Russian",
    "zh-TW": "Traditional Chinese"
}

SOURCE_FILE = os.path.join(PROJECT_ROOT, "README.md")

# --- 3. 核心逻辑 ---

def read_file(path):
    if not os.path.exists(path):
        return None
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def save_file(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def translate_markdown(content, target_lang, existing_translation=None):
    if not content: return ""
    
    if existing_translation:
        prompt = (
            f"You are a professional translator. Below is a Markdown document in Simplified Chinese (SOURCE) and its existing {target_lang} translation (EXISTING TRANSLATION). "
            "The source may have been updated. Your task is to produce an updated translation.\n"
            "Rules:\n"
            "1. Keep the Markdown format exactly the same (headers, bold, italics, links, images, tables, etc.).\n"
            "2. Do NOT translate URLs, code blocks, or file paths.\n"
            "3. Preserve the existing translation as much as possible. Only modify parts where the source has changed.\n"
            "4. If a section in the source is new or significantly different, translate it fresh.\n"
            "5. Return ONLY the translated Markdown content without any explanation or ```markdown wrappers.\n"
            "6. For the 'English | 简体中文 | ...' navigation bar, keep it as is or adapt appropriately, but don't break the links.\n"
        )
        user_content = f"{prompt}\n\n--- SOURCE ---\n{content}\n\n--- EXISTING TRANSLATION ---\n{existing_translation}"
    else:
        prompt = (
            f"You are a professional translator. Translate the following Markdown content from Simplified Chinese to {target_lang}. "
            "Rules:\n"
            "1. Keep the Markdown format exactly the same (headers, bold, italics, links, images, tables, etc.).\n"
            "2. Do NOT translate URLs, code blocks, or file paths.\n"
            "3. Translate image alt texts and link descriptions if applicable.\n"
            "4. Return ONLY the translated Markdown content without any explanation or ```markdown wrappers.\n"
            "5. For the 'English | 简体中文 | ...' navigation bar, keep it as is or adapt appropriately, but don't break the links.\n"
        )
        user_content = f"{prompt}\n\nContent:\n{content}"
    
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that translates Markdown documents."},
                {"role": "user", "content": user_content}
            ],
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"❌ 翻译失败 ({target_lang}): {e}")
        return None

def _translate_one(source_content, lang_code, lang_name):
    """翻译单个语言，返回 (lang_code, lang_name, target_filename, translated_content)"""
    target_filename = f"README.{lang_code}.md"
    target_path = get_path(target_filename)

    existing_translation = read_file(target_path)
    mode = "增量更新" if existing_translation else "全新翻译"
    print(f"  ⏳ 正在{mode} {lang_name} ({target_filename})...")

    translated_content = translate_markdown(source_content, lang_name, existing_translation)
    return lang_code, lang_name, target_filename, target_path, translated_content

def sync_readme():
    print(f"📄 读取源文件: {SOURCE_FILE}")
    source_content = read_file(SOURCE_FILE)
    if not source_content:
        print("❌ 源文件未找到或为空")
        return

    print(f"🚀 开始并发翻译 README (使用模型: {MODEL}, 共 {len(TARGET_LANGS)} 个语言)...\n")

    with ThreadPoolExecutor(max_workers=len(TARGET_LANGS)) as executor:
        futures = {
            executor.submit(_translate_one, source_content, lang_code, lang_name): lang_code
            for lang_code, lang_name in TARGET_LANGS.items()
        }

        success_count = 0
        fail_count = 0
        for future in as_completed(futures):
            lang_code, lang_name, target_filename, target_path, translated_content = future.result()
            if translated_content:
                save_file(target_path, translated_content)
                print(f"  ✅ 已保存: {target_filename}")
                success_count += 1
            else:
                print(f"  ⚠️ 跳过: {target_filename}")
                fail_count += 1

    print(f"\n🎉 翻译完成！成功: {success_count}, 失败: {fail_count}")

if __name__ == "__main__":
    sync_readme()

