import csv
import sys
import re

# 標準入力・出力のエンコーディングをUTF-8に設定
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

# 【修正1】普通の文に出てきそうな単語（somebody, something, 文, 句, カッコなど）を削除しました
# 文法説明特有の表現のみを残しています
keywords = [
    'plus sentence', 'plus noun', "one's", 'A and B',
    '＋', 'Subject', 'Verb', 'Adjective', 'Adverb', 
    'Preposition', 'Noun'
]

# ID 24, 148, 149, 262, 309, 732, 913, 1130, 1439, 1770, 1882 を除外リストに追加
excluded_ids = {24, 148, 149, 262, 309, 732, 913, 1130, 1439, 1770, 1882}

def is_grammar_explanation(row):
    if len(row) < 3:
        return False

    try:
        row_id = int(row[0].strip())
        if row_id in excluded_ids:
            return True # 除外リストに入っているものはTrue（削除対象）
    except (ValueError, IndexError):
        pass

    english_text = row[1].strip()
    japanese_text = row[2].strip()

    # 【修正2】キーワード判定を少し厳密に
    # 文法用語が英語・日本語のどちらかに含まれていたら削除
    for keyword in keywords:
        if keyword in english_text or keyword in japanese_text:
            # ただし、キーワードが文の一部として自然に使われている場合は除外したいが
            # 今回のリストはかなり絞ったので、ヒット＝削除で概ねOKとします
            return True

    # 【修正3】「文法説明っぽい日本語」の判定ロジックを修正
    # 「～」で始まり、かつ句読点がないものは文法説明の可能性が高い
    if japanese_text.startswith('～') and '。' not in japanese_text:
        return True

    # 【修正4】英文の構造チェック（短すぎてピリオド等がないものは怪しい）
    # ただし、単語数が4未満の短いものに限定（長い文は巻き添えにしない）
    is_punctuation_end = english_text.endswith('.') or english_text.endswith('?') or english_text.endswith('!') or english_text.endswith('"')
    if not is_punctuation_end:
        if len(english_text.split()) < 4:
            return True

    # 【修正5】日本語に「文」「句」などの単語が単独で入っているかチェック（"文化"などは除外）
    # 正規表現で "名詞" "形容詞" などが単語として使われているか確認
    grammar_terms_jp = r'(名詞|動詞|形容詞|副詞|助動詞|前置詞|接続詞|不定詞)'
    if re.search(grammar_terms_jp, japanese_text):
        # 文中に「名詞」という言葉が出てくる普通の例文（例：「名詞という言葉の意味は？」）も
        # 消えるリスクはありますが、文法項目の可能性が高いのでここは残します。
        # もしこれも残したい場合は、このif文ブロックを削除してください。
        return True

    return False

try:
    # ファイル名を vocabulary_data_all.csv に合わせました（必要に応じて変更してください）
    input_filename = 'vocabulary_data_all.csv'
    output_filename = 'vocabulary_data.csv'

    with open(input_filename, 'r', encoding='utf-8') as infile, \
         open(output_filename, 'w', encoding='utf-8', newline='') as outfile:

        reader = csv.reader(infile, delimiter='|') # パイプ区切りを指定
        writer = csv.writer(outfile, delimiter='|')

        try:
            # ヘッダー処理（ファイルが空でないか確認）
            first_row = next(reader, None)
            if first_row:
                writer.writerow(first_row)
                
            original_count = 0
            filtered_count = 0

            for row in reader:
                original_count += 1
                if not is_grammar_explanation(row):
                    writer.writerow(row)
                    filtered_count += 1
                else:
                    # デバッグ用：どんな行が消されたか確認したい場合はコメントアウトを外す
                    # print(f"削除: {row[0]} | {row[1]} | {row[2]}")
                    pass

            print(f"元の行数: {original_count}")
            print(f"削除された行数: {original_count - filtered_count}")
            print(f"残った行数: {filtered_count}")
            print(f"{output_filename} に保存しました。")

        except Exception as e:
            print(f"処理中にエラーが発生しました: {e}")

except FileNotFoundError:
    print(f"エラー: {input_filename} が見つかりません。")
except Exception as e:
    print(f"予期せぬエラーが発生しました: {e}")