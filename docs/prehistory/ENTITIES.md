---
id: entities
title: 前史 エンティティ・レジストリ
type: faction
canon: draft
related: []
---

# エンティティ・レジストリ (ENTITIES)

前史に登場する **国家・人物・派閥** の名称を、**ゲーム内ID** に対応づける表。
AIが「この国/人物は実装上どのTAG・どのオブジェクトか」を一意に解決できるようにする。

新しい主体が前史に登場したら、まずここに登録する。

---

## 国家 (Nations)

| lore名 | TAG | 1936時点の政体 | 前史ファイル | 主要実装の所在 |
|---|---|---|---|---|
| <!-- ドイツ帝国 --> | <!-- GER --> | <!-- 立憲君主制 --> | <!-- nations/GER.md --> | <!-- common/national_focus/GER_*, 帝国議会システム --> |

<!--
記入例:
| ドイツ帝国 | GER | 立憲君主制 | nations/GER.md | common/national_focus/GER_*, docs/plan/done/parliament_system_v2.md |
| セルビア王国 | SER | 王制 | nations/SER.md | docs/plan/skelton_contents/balkan_war.md |
-->

---

## 人物 (Characters)

`history/characters/` の token と対応づける。重要人物のみ。

| lore名 | 所属TAG | 役割 | character token | 前史ファイル |
|---|---|---|---|---|
| <!-- 氏名 --> | <!-- TAG --> | <!-- 君主/宰相/将官など --> | <!-- token --> | <!-- characters/xxx.md または nations/TAG.md --> |

---

## 派閥・ブロック (Factions / Blocs)

同盟、条約機構、経済圏など。

| lore名 | 中心TAG | 構成 | 前史ファイル | ゲーム上の表現 |
|---|---|---|---|---|
| <!-- ミッテルオイローパ --> | <!-- GER --> | <!-- 構成国 --> | <!-- factions/mitteleuropa.md --> | <!-- faction / idea / 外交関係など --> |
