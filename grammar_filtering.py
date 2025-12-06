import pandas as pd

def clean_vocabulary_data(input_file, output_file):
    """
    CSVファイルを読み込み、文法解説的な行（'plus sentence'や'+'記号を含む行）を
    削除して新しいファイルに出力します。
    """
    try:
        # パイプ区切りでCSVを読み込む
        df = pd.read_csv(input_file, sep='|')
        
        # 削除前の行数を取得
        initial_count = len(df)
        print(f"処理前の行数: {initial_count}")

        # 文法解説行を特定する条件関数
        def is_grammar_row(row):
            english = str(row['英文']).lower()
            japanese = str(row['日本語訳'])
            
            # 条件1: "plus sentence" というフレーズが含まれる場合
            if "plus sentence" in english:
                return True
            
            # 条件2: 構造を示す "+" や "＋" が含まれる場合
            # (通常の文章でプラス記号が使われることは稀なため、これをフィルタとして使用)
            if "+" in english or "＋" in english or "＋" in japanese:
                return True
            
            return False

        # フィルタリング実行（文法行ではないものを残す）
        # axis=1 は行ごとに処理を行う指定
        mask = df.apply(is_grammar_row, axis=1)
        cleaned_df = df[~mask] # maskがTrueの行を除外
        
        removed_count = initial_count - len(cleaned_df)
        
        # 結果を保存 (パイプ区切りを維持、indexは保存しない)
        cleaned_df.to_csv(output_file, sep='|', index=False)
        
        print(f"処理後の行数: {len(cleaned_df)}")
        print(f"削除された行数: {removed_count}")
        print(f"完了しました。出力ファイル: {output_file}")
        
        # 削除された行の内容を一部表示（確認用）
        if removed_count > 0:
            print("\n--- 削除された行の例 ---")
            print(df[mask][['英文', '日本語訳']].head().to_string(index=False))

    except Exception as e:
        print(f"エラーが発生しました: {e}")

if __name__ == "__main__":
    input_filename = 'vocabulary_data_all.csv'
    output_filename = 'vocabulary_data.csv'
    
    clean_vocabulary_data(input_filename, output_filename)