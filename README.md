# 宇佐美リト 配信・動画カレンダー

非公式ファン制作の月次配信・通常動画アーカイブです。GitHub Pages 上で動作します。

- 本人チャンネル：`UCambvP8yxNDot4FzQc9cgiw`
- 自動収集：YouTube Data API v3 から本人チャンネルの配信・通常動画、にじさんじWikiの動画一覧から他チャンネルの出演配信。
- データ：`data/usami-streams.json`（公開済み動画・配信のみ）
- 更新：GitHub Actions `update-usami.yml`、毎日 05:17 / 17:17 JST。手動の Run workflow も可能。
- 月間累計時間：配信開始〜終了までの実績時間を合計。コラボを含むが、にじさんじ公式メインチャンネルの配信と通常動画は集計対象外。

## 手動追加

画面の「＋追加」からURL・日時・タイトル等を登録できます。YouTube URLを貼ると公開メタデータを自動取得し、収集済み動画ならタイトル・日本時間の開始時刻・種類・配信時間を反映します。収集対象外の公開動画はYouTubeのoEmbed（必要時Noembed）からタイトルを取得しますが、開始・終了時刻は取得できない場合があるため手動入力してください。メンバー限定・非公開のメタデータは原則取得できません。

手動データはこのブラウザの `localStorage` に自動保存されます。自動収集データとは別であり、公開リポジトリには保存しません。

## Google Driveとの手動同期（任意）

佐伯カレンダーと同じ `Google Drive appDataFolder` 方式です。公開サイトではなく、ご自身のGoogle Driveの非公開アプリデータ領域に **手動追加した項目のみ** をバックアップします。別端末で復元すると、その端末の手動登録内容をDriveのバックアップで置き換えます。**自動同期・差分マージではありません。**

1. Google Cloudで、サイトのGitHub Pagesのオリジン（例：`https://anna0618xx.github.io`）を許可した **ウェブアプリケーション用OAuth 2.0 クライアントID** を準備。Google Drive APIを有効にします。`drive.appdata` スコープを使用します。
2. カレンダー下部の「☁ クラウド同期（Google Drive）」を開き、クライアントIDを入力します。佐伯カレンダーで使っている同じオリジンのIDを再利用できます。
3. 「Googleに接続」で利用者自身が認可後、「Driveへ保存」をクリック。
4. 別端末で同じクライアントIDとGoogleアカウントを使って接続し、「Driveから復元」。上書き確認が表示されます。

Googleのアクセストークンはメモリ内のみ保持し、GitHubやlocalStorageへ保存しません。手動データのDrive側ファイル名：`usami-calendar-manual-v1-private.json`。佐伯版とは別ファイルです。

## 自動収集セットアップ

GitHub Actions の Secret `YOUTUBE_API_KEY` に YouTube Data API v3 のキーを設定します。GitHub Pages の公開を有効にし、Actions の `Update Usami stream calendar` を実行します。自動収集スクリプト：`scripts/collect_usami.py`。

※ 公式画像やきりんちゃんの専用アセットは未組み込み。
