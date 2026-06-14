# マップエラー修正計画

> 対象ログ: `~/Documents/Paradox Interactive/Hearts of Iron IV/crashes/hoi4_20260613_153644/logs/error.log`
> ブランチ: `feature/_map_bsr` / 作成: 2026-06-13 / 状態: **ステージ1〜4実装済み（ステージ5は任意・未実装）**

実装メモ（2026-06-13）:

- `descriptor.mod` とデプロイ先 `Tsareich2.mod` に `replace_path="map/strategicregions"` を追加。
- 州ファイルの大小文字recase、`765-Qatar` のカテゴリ追加、1058〜1061の人口ゼロ修正、未定義ownerタグ7種の既存タグ置換、`763-Königsberg` の建物ブロック統合を実施。
- ライブ `map/strategicregions` は `definition.csv` の13,994プロヴィンスを重複0・未割当0で被覆することを確認。

---

## 1. error.log 全体像（全2,910件）

| 区分 | ソース | 件数 | 内容 |
|---|---|---:|---|
| **A. 戦略地域 重複** | `strategicregion.cpp:333` | 1,448 | 1プロヴィンスが2つの戦略地域に所属 |
| **A. 戦略地域 未割当** | `gamestate.cpp:2896` | 1,197 | プロヴィンスがどの戦略地域にも未所属 |
| **A. 州が地域跨ぎ** | `gamestate.cpp` | 76 | 1つの州が複数の戦略地域に跨る |
| B. 州ID重複(大小文字) | `statetemplate.cpp:690` | 9 | git index旧名と実ファイル名の不一致 |
| B. カテゴリ未定義 | `statetemplate.cpp:239` | 1 | 州#765 |
| B. 人口ゼロ | `statetemplate.cpp:241` | 4 | 州#1058–1061 |
| C. 未定義国家タグ | `statehistory.cpp:153` | 20 | owner未定義タグ(7種) |
| C. 建物ブロック重複 | `statehistory.cpp:245` | 1 | 州763 prov6332 |
| D. rivers.bmp パレット | `map.cpp:665` | 1 | 警告（非ブロッキング） |
| D. 極小プロヴィンス | `map.cpp:1842` | 17 | 8px未満（描画警告） |
| （対象外）非マップ系 | 各種 | 約120 | special_projects/MIO/AI/BOM 等 |

**区分Aだけで2,721件＝マップエラーの93%。単一原因で、`descriptor.mod` の1行追加で全消滅する。**

---

## 2. 根本原因（実証済み）

`descriptor.mod` に **`replace_path="map/strategicregions"` が無い。**

Modはマップを全面再定義（13,994プロヴィンス）し、戦略地域も自前で364ファイル用意しているが、`replace_path` が無いため HOI4 は**バニラの戦略地域304ファイルも同時ロード**する。うち**94ファイルはModが同名で上書きしていない**ため漏れ込む（bleed-through）。

決定打は**戦略地域IDの衝突**。Modはバニラと同じID 211〜304を**全く別の地理に流用**している:

| ID | Mod定義 | バニラ定義（漏れ込み） |
|---|---|---|
| 211 | 211-Central Balkans | 211-Gulf Coast |
| 217 | 217-Hokkaido | 217-Lake Victoria |
| 218 | 218-Kyushu | 218-California |
| 220 | 220-East Prussia | 220-Labrador and Newfoundland |
| 274 | 274-Northern China | 274-Ogaden |

…という具合に**94件すべてのIDが衝突**。HOI4は同一IDに戦略地域オブジェクトを1つしか保持しないため:

- ID 211〜304帰属の**Mod側プロヴィンスが弾き出されて未割当** → 1,197件（全件がMod ID 211〜304帰属と確認）
- 漏れ込んだバニラ地域が別プロヴィンスを横取り → **重複** 1,448件

**検証:** 重複6件をサンプルし全て「バニラ専用ファイルが片側」と確認。例 prov638 は Mod `117-East Coast` のみに所属するのに、バニラ `211-Gulf Coast` も列挙 → ログの「東海岸(117) overridden by ガルフ海岸(211)」と完全一致。Mod自前364ファイルは内部完全（全13,994prov を重複0・隙間0で被覆）。よってバニラを締め出せば残課題ゼロ。

---

## 3. 修正計画（段階別）

### ⭐ ステージ1 — 戦略地域（区分A・2,721件を一掃）｜最優先・最小リスク

`replace_path="map/strategicregions"` を**2ファイル両方**に追加（既存のreplace_path群と同位置）:

1. リポジトリ `descriptor.mod` … バージョン管理上の真実
2. デプロイ先 `~/Documents/Paradox Interactive/Hearts of Iron IV/mod/Tsareich2.mod` … **ゲームが実際に読むのはこちら**（`path=`Mod のため必須）

> 検証済み: `map/supplyareas`（バニラ専用0件）・`map/terrain` は対応不要。`map/strategicregions` のみ要対応。`definition.csv` 等の単一ファイルは単体上書きで正常。

### ステージ2 — 州ファイル（区分B・14件）

- **大小文字ID重複（9件）**: 物理ファイルは1つ（macOS=case-insensitive、同一inode）。**`rm`厳禁**。git index の旧小文字名を実ファイル名へ recase:
  ```sh
  git rm --cached "history/states/223-tula.txt" && git add "history/states/223-Tula.txt"
  ```
  対象: 223 / 238 / 250 / 258 / 301 / 624 / 83 / 844 / 862
  （624 = "islands→Islands"、862 = "ouest du quebec→Ouest du Quebec" は内部語の大小文字）
- **カテゴリ未定義（1件）**: `765-Qatar.txt` の `name=` 直後に `state_category=town` を追加（海軍基地2・VP有りに整合）
- **人口ゼロ（4件）**: `manpower=0` を非ゼロへ
  - `1058-Batavia`（rural）/ `1059-Limbang`（rural）/ `1060-Johor`（pastoral）/ `1061-Perlis-Kedah`（large_city — 工業+海軍基地10 でゼロは明らかに異常、30万+目安）

### ステージ3 — 未定義国家タグ（区分C・20件）｜方針: **既存タグへ置換**

全7タグがBSR由来の未登録placeholder。`owner` 行が原因（`add_core_of` 行の同タグも併せて置換）。

| タグ | owner件数 | 置換先（既存タグ） | 地域 |
|---|---:|---|---|
| SZH | 6 | **SIC**（四川） | 四川 |
| HSI | 6 | **TIB**（チベット） | 西康/カム |
| NEA | 4 | **XIC**（西安） | 陝西/華北 |
| TUG | 1 | **SIK** or ETR | 東トルキスタン |
| TNG | 1 | **MOR**/SPR | タンジール |
| DAN | 1 | **DNZ**（実質重複） | ダンツィヒ |
| NSI | 1 | **NXM** or XSM | 寧夏 |

各置換先は同州群で既にcore登録済み（地理整合）。新規国家定義は行わない。

### ステージ4 — 建物ブロック重複（区分C・1件）

`763-Königsberg.txt`: prov6332 の `{bunker=1}` と `{naval_base=5}` を1ブロックに統合:

```
6332 = { bunker = 1 naval_base = 5 }
```

### ステージ5 — グラフィック（区分D・18件）｜任意・非ブロッキング

- **rivers.bmp**: パレット色自体はバニラと完全一致。ヘッダ `biClrUsed/biClrImportant=256` が警告原因。正規エクスポータで再保存し0にすれば消える（描画は正常動作中）
- **極小プロヴィンス17件**: `516, 2560, 5475, 6157, 7381, 8435, 10870, 11290, 13012, 13015, 13278, 13286, 13307, 13309, 13317, 13410, 13474`。provinces.bmp で各領域を8px以上へ拡張、または隣接へ統合。スタッキング/選択の軽微な不具合のみ

---

## 4. 推奨着手順

```
ステージ1（最小リスク・最大効果）
  → ステージ2 → ステージ4 → ステージ3 → ステージ5（任意）
```

---

## 5. 検証手順

1. HOI4 再起動
2. 新しい `error.log` で `strategicregion.cpp` / `gamestate.cpp MAP_ERROR` の消滅を確認
3. 続いて `statetemplate.cpp` / `statehistory.cpp` 各行の消滅を確認

※ このマシン上からゲーム起動検証は不可。手動確認が必要。

---

## 6. 対象外（非マップ系・約120件）

`special_projects` のスコープ変数、MIO不一致、AI strategy template、localisation BOM 等。本計画には含めない（必要なら別途棚卸し）。
