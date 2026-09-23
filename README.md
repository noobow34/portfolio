# noobow portfolio

ぬーぼー（noobow）のポートフォリオサイト。ビルド不要の静的 HTML/CSS/JS を
**Cloudflare Workers Static Assets** で配信する（Worker スクリプトなし）。

```
public/
  index.html   # 本体
  style.css    # ライト/ダーク両対応（prefers-color-scheme + 手動切替）
  main.js      # テーマ切替・パタパタ表示・スクロール表示
  404.html     # not_found_handling = "404-page"
  _headers     # セキュリティヘッダ / CSP
  favicon.svg
wrangler.jsonc
```

## 開発・デプロイ

Node.js 24 以上が必要（`.node-version` / `engines` で指定）。

```bash
npm install
npm run dev      # http://localhost:8787
npm run deploy   # wrangler deploy
```

独自ドメインで出すときは `wrangler.jsonc` の `routes` を有効化する。
Cloudflare Pages に載せる場合も、Build output directory を `public`（Build command 空欄）にすればそのまま動く。

## OGP 画像

`public/images/og.png`（1200×630・搭乗券風）は `tools/make-og-image.py` で生成している。
文言を変えたら再生成する（Pillow が必要）。

```bash
python tools/make-og-image.py
```

公開ドメインを決めたら、`index.html` の `og:image` を絶対 URL に直すこと。
