
import csv
import sys

# 標準入力・出力のエンコーディングをUTF-8に設定
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

keywords = [
    'plus sentence', 'somebody', 'something', "one's", 'A and B',
    '～', '＋', '動詞', '名詞', '形容詞', '副詞', '文', '句',
    '（', '）', '「', '」'
]

# ID 24, 148, 149, 262, 309, 732, 913, 1130, 1439, 1770, 1882 を除外リストに追加
excluded_ids = {24, 148, 149, 262, 309, 732, 913, 1130, 1439, 1770, 1882}

def is_grammar_explanation(row):
    if len(row) < 3:
        return False

    try:
        row_id = int(row[0].strip())
        if row_id in excluded_ids:
            return False
    except (ValueError, IndexError):
        # IDが数値でない、またはID列が存在しない場合はスキップ
        pass

    english_text = row[1].strip()
    japanese_text = row[2].strip()

    # キーワードが含まれているか
    for keyword in keywords:
        if keyword in english_text or keyword in japanese_text:
            return True

    # 英文が文として不完全か（感嘆符やピリオドで終わるが短いものも含む）
    if not (english_text.endswith('.') or english_text.endswith('?') or english_text.endswith('!')):
         # Ends with a punctuation but is likely not a full sentence
        if len(english_text.split()) < 4:
            return True

    # 日本語訳が説明的か
    if '。' not in japanese_text and ('（' in japanese_text or '）' in japanese_text):
        return True


    return False

try:
    with open('data.csv', 'r', encoding='utf-8') as infile, \
         open('data_filtered.csv', 'w', encoding='utf-8', newline='') as outfile:

        reader = csv.reader(infile, delimiter='|')
        writer = csv.writer(outfile, delimiter='|')

        try:
            header = next(reader)
            writer.writerow(header)
            original_count = 1
            filtered_count = 1

            for row in reader:
                original_count += 1
                if not is_grammar_explanation(row):
                    writer.writerow(row)
                    filtered_count += 1
                # else:
                #     print(f"削除された行: {row}")


            print(f"元の行数: {original_count-1}") #ヘッダー分を引く
            print(f"削除された行数: {(original_count-1) - (filtered_count-1)}")
            print(f"新しい行数: {filtered_count-1}")
            print("data_filtered.csv に保存しました。")

        except StopIteration:
            print("エラー: data.csv が空か、ヘッダーがありません。")

except FileNotFoundError:
    print("エラー: data.csv が見つかりません。")
except Exception as e:
    print(f"予期せぬエラーが発生しました: {e}")
