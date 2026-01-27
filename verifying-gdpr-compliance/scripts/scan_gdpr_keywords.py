import os
import re

# 定義要搜尋的關鍵字類別及其正則表達式
KEYWORD_CATEGORIES = {
    "Consent & Cookie (同意與 Cookie)": [
        r"cookie[_\-\s]?consent",
        r"accept[_\-\s]?cookies",
        r"privacy[_\-\s]?policy",
        r"terms[_\-\s]?of[_\-\s]?service",
        r"同意",
        r"條款",
    ],
    "Right to Erasure (刪除權)": [
        r"delete[_\-\s]?user",
        r"delete[_\-\s]?account",
        r"remove[_\-\s]?data",
        r"forget[_\-\s]?me",
        r"刪除帳號",
        r"刪除資料",
    ],
    "Data Portability (資料可攜權)": [
        r"export[_\-\s]?data",
        r"download[_\-\s]?data",
        r"user[_\-\s]?dump",
        r"匯出",
        r"下載資料",
    ],
    "Security & Encryption (安全與加密)": [
        r"encrypt",
        r"hash",
        r"salt",
        r"bcrypt",
        r"argon2",
        r"audit[_\-\s]?log",
        r"加密",
    ],
}

# 忽略的目錄與檔案
IGNORE_DIRS = {
    ".git",
    "node_modules",
    "__pycache__",
    "venv",
    ".venv",
    "dist",
    "build",
    ".agent",
}
IGNORE_EXTS = {
    ".pyc",
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".svg",
    ".ico",
    ".woff",
    ".ttf",
    ".eot",
    ".mp4",
    ".pdf",
    ".zip",
    ".tar",
    ".gz",
}


def scan_files(start_path="."):
    results = {category: [] for category in KEYWORD_CATEGORIES}

    print(f"正在掃描目錄: {os.path.abspath(start_path)} (忽略大型與二進位目錄)...")

    for root, dirs, files in os.walk(start_path):
        # 修改 dirs 列表以其移除忽略的目錄
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]

        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in IGNORE_EXTS:
                continue

            file_path = os.path.join(root, file)
            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()

                    for category, patterns in KEYWORD_CATEGORIES.items():
                        for pattern in patterns:
                            if re.search(pattern, content, re.IGNORECASE):
                                # 找到匹配，記錄下來 (只記錄檔案路徑，避免過多雜訊)
                                results[category].append(file_path)
                                break  # 該檔案在此類別只需記錄一次
            except Exception as e:
                # 忽略讀取錯誤
                pass

    return results


def print_report(results):
    print("\n=== GDPR 關鍵字掃描報告 ===\n")
    found_any = False
    for category, files in results.items():
        if files:
            found_any = True
            print(f"## {category}")
            # 只顯示前 5 個檔案，避免洗版
            for f in files[:5]:
                print(f"  - {f}")
            if len(files) > 5:
                print(f"  - ... (共 {len(files)} 個檔案)")
            print("")
        else:
            print(f"## {category}")
            print("  - ⚠️ 未發現明顯關鍵字 (可能主要由前端處理或使用不同命名)")
            print("")

    if not found_any:
        print("未掃描到任何常見的 GDPR 關鍵字。請確認專案是否包含相關實作。")


if __name__ == "__main__":
    results = scan_files()
    print_report(results)
