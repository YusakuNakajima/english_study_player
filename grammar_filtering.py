import pandas as pd
import csv
import os

def clean_vocabulary_data(input_file, output_file):
    """
    CSVファイルを読み込み、文法解説的な行（'plus sentence'や'+'記号を含む行）を
    削除して新しいファイルに出力します。
    また、列の数が7でない行を修正します。
    """
    try:
        with open(input_file, 'r', encoding='utf-8') as infile:
            reader = csv.reader(infile, delimiter='|', quoting=csv.QUOTE_NONE)
            header = [h.strip() for h in next(reader)]
            num_columns = len(header)
            
            data = [header]
            for i, row in enumerate(reader, 2):
                if len(row) != num_columns:
                    # print(f"Line {i}: Found {len(row)} fields, expected {num_columns}. Row content: {row}")
                    row = (row + [''] * num_columns)[:num_columns]
                data.append(row)

        df = pd.DataFrame(data[1:], columns=data[0])
        
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

        # フィルタリング実行
        # 1. 文法解説行を特定
        mask_grammar = df.apply(is_grammar_row, axis=1)

        # 2. 空行を特定 (ID列が空か、あるいはスペースのみかをチェック)
        #    これにより '||||||' のような行が削除される
        mask_empty = df['ID'].astype(str).str.strip() == ''
        
        # 両方のマスクを組み合わせて、不要な行を除外
        cleaned_df = df[~(mask_grammar | mask_empty)]
        
        removed_count = initial_count - len(cleaned_df)
        
        # 結果を保存 (パイプ区切りを維持、indexは保存しない)
        cleaned_df.to_csv(output_file, sep='|', index=False)
        
        print(f"処理後の行数: {len(cleaned_df)}")
        print(f"削除された行数: {removed_count}")
        print(f"完了しました。出力ファイル: {output_file}")
        
        # 削除された行の内容を一部表示（確認用）
        if removed_count > 0:
            print("\n--- 削除された行の例 ---")
            print(df[mask_grammar][['英文', '日本語訳']].head().to_string(index=False))

    except Exception as e:
        print(f"エラーが発生しました: {e}")

if __name__ == "__main__":
    input_filename = 'vocabulary_data_all.csv'
    output_filename = 'vocabulary_data.csv'
    
    clean_vocabulary_data(input_filename, output_filename)