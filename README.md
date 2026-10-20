# USAMI STREAM LOG（開発ブランチ）
宇佐美リトの非公式月次配信カレンダーです。

- 公式チャンネルID: `UCambvP8yxNDot4FzQc9cgiw`
- カラー: `#FAC31E` と `#7DDCFF`
- 表示: 月別、サムネイル、タイトル、JST開始時刻、YouTubeリンク
- 収集: YouTube Data API v3 から公開ライブ配信と予約枠を取得
- 更新: GitHub Actions `update-usami.yml`（6時間ごと＋手動）
- 保存先: `data/usami-streams.json`

## 公開までの設定
1. リポジトリ Settings → Secrets and variables → Actions に `YOUTUBE_API_KEY` を登録。
2. このブランチを main に取り込み、GitHub Pages を main のルートから公開。
3. Actions → Update Usami stream calendar → Run workflow を初回実行（以後6時間ごと）。
4. サイトで取得データと日時を確認。

公開済みのYouTube動画のみ取得します。限定公開・メンバー限定は自動取得できません。配信中・予約枠は表示後に変更される場合があります。コラボ先チャンネルの動画は収集対象外です。過去分は最新の最大約500投稿から探索し、取得済みの過去分はJSONに残します。無料のYouTube Data APIはクォータ制限を受けます。

※ きりんちゃんの公式イラスト画像は未組み込み。権利と使用方法を確認してから追加してください。
