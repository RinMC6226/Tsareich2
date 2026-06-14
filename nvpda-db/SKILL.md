---
name: nvpda-db
description: NVPDA海軍艦艇データベース（NSDB.db）への問い合わせスキル。艦艇クラス、個艦情報、国別データの検索・集計に使用する。ユーザーが艦艇・軍艦・海軍に関するデータを質問したとき、または DB からデータを取得したいときに自動で読み込まれる。
allowed-tools: Bash(sqlite3:*), Bash(python3:*), Bash(.venv/bin/python:*), Read, Grep
---

# NVPDA 海軍艦艇データベース クエリスキル

このスキルを使い、同梱された SQLite データベース `NSDB.db` から海軍艦艇データを検索・集計する。

## インストール方法

このスキルフォルダ（`nvpda-db/`）を任意のプロジェクトの `.claude/skills/` にコピーするだけで使える。

```
<任意のプロジェクト>/
  .claude/
    skills/
      nvpda-db/
        SKILL.md        ← このファイル
        NSDB.db         ← 海軍艦艇データベース（約850MB）
        query_db.py     ← クエリヘルパースクリプト
```

### 設定の追加

コピー先プロジェクトの `.claude/settings.local.json` に以下の権限を追加する:

```json
{
  "permissions": {
    "allow": [
      "Bash(python3:*)",
      "Bash(sqlite3:*)"
    ]
  }
}
```

## データベースのパス

```
.claude/skills/nvpda-db/NSDB.db  （このスキルフォルダ内に同梱）
```

## データベーススキーマ

### COUNTRIES テーブル（181件）
国・海軍の一覧。

| カラム | 型   | 説明                    |
|--------|------|-------------------------|
| Short  | TEXT | 国コード（例: JP, US, GB）|
| Long   | TEXT | 国名（英語）             |
| URL    | TEXT | 参照URL                  |

### CLASS テーブル（10,727件）
艦艇クラス（型）の詳細情報。

| カラム                | 型   | 説明                           |
|-----------------------|------|--------------------------------|
| CLASS_NAME            | TEXT | クラス名（例: Takao Class）     |
| TYPE                  | TEXT | 艦種（例: destroyers, frigates）|
| COUNTRY               | TEXT | 国コード                       |
| Photo                 | TEXT | メイン写真（Base64）            |
| Displacement_normal   | TEXT | 基準排水量（トン）              |
| Displacement_full     | TEXT | 満載排水量（トン）              |
| Length                | TEXT | 全長（m）                      |
| Breadth               | TEXT | 全幅（m）                      |
| Draught               | TEXT | 喫水（m）                      |
| No_of_shafts          | TEXT | 軸数                           |
| Machinery             | TEXT | 機関                           |
| Power                 | TEXT | 出力（馬力）                   |
| speed                 | TEXT | 最大速力（ノット）              |
| Fuel                  | TEXT | 燃料搭載量（トン）              |
| Endurance             | TEXT | 航続距離（海里）                |
| Armour                | TEXT | 装甲                           |
| Armament              | TEXT | 兵装                           |
| Electronic_equipment  | TEXT | 電子装備                       |
| Complement            | TEXT | 乗員数                         |
| images                | TEXT | スケール画像（Base64）          |
| Graphics              | TEXT | 図面（Base64）                  |
| Project_history       | TEXT | 計画経緯                       |
| Modernizations        | TEXT | 近代化改装                     |
| Naval_service         | TEXT | 軍歴                           |
| sections              | TEXT | 追加セクション（JSON）          |
| source_url            | TEXT | データ取得元URL                 |
| fetched_at            | TEXT | データ取得日時（ISO8601）       |

### SHIPS テーブル（107,764件）
個々の艦艇の建造・運用情報。

| カラム     | 型   | 説明                     |
|-----------|------|--------------------------|
| NAME      | TEXT | 艦名                     |
| CLASS     | TEXT | 所属クラス名              |
| COUNTRY   | TEXT | 国コード                  |
| NO        | TEXT | 艦番号（ペナントナンバー） |
| Yard_No   | TEXT | 造船所番号                |
| Builder   | TEXT | 建造所                    |
| Laid_down | TEXT | 起工日                    |
| Launched  | TEXT | 進水日                    |
| Fate_WHY  | TEXT | 最終運命（沈没・解体等）    |
| Fate_WHEN | TEXT | 運命の日付                 |
| TYPE      | TEXT | 艦種                      |
| SID       | TEXT | 艦識別子                  |
| WHEN_DATE | TEXT | 建造期間                  |
| source_url| TEXT | データ取得元URL            |

### TRANSLATIONS テーブル（翻訳キャッシュ）
英語テキストの日本語翻訳を保持。

| カラム        | 型   | 説明                    |
|--------------|------|-------------------------|
| source_url   | TEXT | 艦艇クラスページのURL    |
| section_name | TEXT | セクション名             |
| translated   | TEXT | 日本語翻訳テキスト       |

PRIMARY KEY: (source_url, section_name)

## 艦種（TYPE）の主な値

| 英語                        | 日本語       |
|----------------------------|-------------|
| battleships                | 戦艦        |
| aircraft carriers          | 航空母艦    |
| cruisers                   | 巡洋艦      |
| destroyers                 | 駆逐艦      |
| frigates                   | フリゲート  |
| submarines                 | 潜水艦      |
| corvettes                  | コルベット  |
| torpedo boats              | 水雷艇      |
| minesweepers               | 掃海艇      |
| minelayers                 | 機雷敷設艦  |
| gunboats                   | 砲艦        |
| patrol vessels             | 哨戒艦艇    |
| landing ships              | 揚陸艦      |
| auxiliaries                | 補助艦艇    |

## クエリ実行方法

### 方法1: ヘルパースクリプト（推奨）

同梱の `query_db.py` を使う。画像カラムの自動除外や長文の切り詰めを行う:

```bash
python3 .claude/skills/nvpda-db/query_db.py "SELECT CLASS_NAME, TYPE FROM CLASS WHERE COUNTRY = 'JP'"
python3 .claude/skills/nvpda-db/query_db.py --schema      # スキーマ表示
python3 .claude/skills/nvpda-db/query_db.py --stats        # レコード数
python3 .claude/skills/nvpda-db/query_db.py --types        # 艦種一覧
python3 .claude/skills/nvpda-db/query_db.py --countries    # 国一覧
```

### 方法2: sqlite3 コマンド

```bash
sqlite3 -header -column .claude/skills/nvpda-db/NSDB.db "SELECT ..."
```

**注意:** Photo, images, Graphics カラムは巨大な Base64 文字列のため、SELECT * は避け、必要なカラムのみ指定すること。

## よく使うクエリパターン

### 国の一覧
```sql
SELECT Short, Long FROM COUNTRIES ORDER BY Long;
```

### 特定の国の艦艇クラス一覧
```sql
SELECT CLASS_NAME, TYPE FROM CLASS WHERE COUNTRY = 'JP' ORDER BY TYPE, CLASS_NAME;
```

### 艦種別のクラス数を集計
```sql
SELECT TYPE, COUNT(*) as cnt FROM CLASS GROUP BY TYPE ORDER BY cnt DESC;
```

### 国別の艦艇数を集計
```sql
SELECT c.Long, COUNT(s.rowid) as ship_count
FROM SHIPS s JOIN COUNTRIES c ON s.COUNTRY = c.Short
GROUP BY s.COUNTRY ORDER BY ship_count DESC LIMIT 20;
```

### 特定クラスの諸元を取得
```sql
SELECT CLASS_NAME, TYPE, Displacement_normal, Displacement_full,
       Length, Breadth, Draught, speed, Armament, Complement
FROM CLASS WHERE CLASS_NAME LIKE '%Yamato%';
```

### 特定クラスに属する個艦の一覧
```sql
SELECT NAME, NO, Builder, Laid_down, Launched, Fate_WHY, Fate_WHEN
FROM SHIPS WHERE CLASS LIKE '%Yamato%' ORDER BY Laid_down;
```

### 特定の艦名で検索
```sql
SELECT s.NAME, s.CLASS, s.COUNTRY, c.Long as Country_Name, s.NO, s.Builder, s.Fate_WHY
FROM SHIPS s JOIN COUNTRIES c ON s.COUNTRY = c.Short
WHERE s.NAME LIKE '%Enterprise%' ORDER BY s.NAME;
```

### 特定の建造所で建造された艦を検索
```sql
SELECT NAME, CLASS, COUNTRY, Laid_down, Launched
FROM SHIPS WHERE Builder LIKE '%Mitsubishi%' ORDER BY Laid_down;
```

### クラスの歴史テキストを取得（テキストのみ、画像を除外）
```sql
SELECT CLASS_NAME, Project_history, Modernizations, Naval_service
FROM CLASS WHERE CLASS_NAME LIKE '%Iowa%';
```

## 重要な注意事項

1. **Base64 画像カラムを避ける**: `Photo`, `images`, `Graphics` は巨大なため、`SELECT *` ではなく必要なカラムを明示的に指定すること。
2. **LIKE 検索**: 艦名・クラス名は英語表記。部分一致は `LIKE '%keyword%'` を使う。
3. **国コード**: COUNTRY は短縮コード（JP, US, GB 等）。国名が必要なら COUNTRIES テーブルと JOIN する。
4. **TEXT 型**: 数値データ（排水量、速力等）も TEXT で格納されているため、数値比較には CAST が必要。
5. **sections カラム**: JSON 形式の追加セクション。`json_extract()` で値を取り出せる。
6. **出力言語**: ユーザーが日本語で質問した場合は日本語で回答する。データ自体は英語で格納されている。
