import shutil
import pandas as pd
import os

def clean_trailing_pipes(filename):
    """
    1. 行末のパイプ(|)を削除
    2. 空行（何も書かれていない行）を削除
    3. .bakバックアップを作成
    """
    backup_filename = filename + '.bak'
    
    if not os.path.exists(filename):
        print(f"Error: {filename} が見つかりません。")
        return False

    shutil.copy(filename, backup_filename)
    print(f"Backed up {filename} to {backup_filename}")

    with open(backup_filename, 'r', encoding='utf-8') as infile, \
         open(filename, 'w', encoding='utf-8') as outfile:
        
        for line in infile:
            # strip()で前後の空白と改行を全部取る
            # その後 rstrip('|') で末尾のパイプを取る
            content = line.strip().rstrip('|')
            
            # 中身がある場合だけ書き込む（＝空行はスキップされる）
            if content:
                outfile.write(content + '\n')
    
    print(f"Cleaned {filename}")
    return True

def main_process():
    target_csv = 'vocabulary_data_all.csv'

    print("--- Cleaning Process ---")
    success = clean_trailing_pipes(target_csv)

    if success:
        print("\n--- Loading Process ---")
        try:
            # 空行を削除したので、かなり読み込みやすくなっているはずです
            df = pd.read_csv(target_csv, sep='|', on_bad_lines='warn') 
            
            print("データの読み込みに成功しました:")
            print(df.head())
            print(f"\n読み込み完了: 全 {len(df)} 行")
            
        except Exception as e:
            print(f"読み込みエラーが発生しました: {e}")

if __name__ == "__main__":
    main_process()