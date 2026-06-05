# 生成AI追加質問票 Webアプリ

健診で使用する生成AI追加質問票のWebデモです。  
Streamlitで動作します。

## セットアップ

```bash
pip install -r requirements.txt
```

## 起動

```bash
streamlit run app.py
```

## 回答データ

回答は以下に保存されます。

```
data/responses.csv
```

## 注意

- チェックボックスは使わず、すべてボタン選択式です。
- Q1の回答によって、以降の質問が分岐します。
- ID No. と全回答がそろうまで保存できません。
