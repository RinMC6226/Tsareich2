---
id: 1930s_three-bloc-order
title: 1930年代の三陣営への再編
type: event
date_start: 1936.0.0
tags: [GER, RUS, ITA, FRA, SPR, ENG, USA]
canon: canon
implements: []
related:
  - 1918_italy-postwar-nationalist-turn
  - 1920_spanish-second-republic
  - 1929_great-depression
  - 1936_us-presidential-election
to_do:
  - "原文は『1930年代後半』とあり確定年が曖昧。date_start を 1936.0.0（ゲーム開始年）と仮置きしている。"
  - "三陣営それぞれの faction 実装（独露伊大陸同盟・インターナショナル・英米海洋陣営）の faction 名・加盟国・初期外交関係が未確定。ENTITIES.md の派閥表と整合させること。"
  - "この構造は1936年初期の世界情勢そのもの。history/countries や common/ の初期同盟・guarantee・opinion 設定に落とし込む必要がある。"
sources: []
---

# 1930年代の三陣営への再編

## 概要

1930年代後半、世界は三つの陣営に再編された。ドイツ（GER）・ロシア（RUS）・イタリア（ITA）は大陸秩序の維持を目指し、フランス（FRA）とスペイン（SPR）はインターナショナルとして革命輸出を掲げ、イギリス（ENG）とアメリカ（USA）は海洋通商秩序の再建を目的に接近した。世界は次なる大戦へ向かっていく。

## 経緯

1930年代後半、世界は思想と利害により三つの陣営へ再編された。

- **独露大陸同盟（GER・RUS・ITA）:** 大陸秩序の維持を目指す。
- **インターナショナル（FRA・SPR）:** [フランス・コミューン](1917_french-revolution.md)と[スペイン共和国](1920_spanish-second-republic.md)が協調し、革命輸出を掲げる。
- **英米海洋陣営（ENG・USA）:** [ノックス政権成立後の米国](1936_us-presidential-election.md)とイギリスが、海洋通商秩序の再建を目的に接近する。

英米とインターナショナルは思想的には対立していたが、独露による大陸覇権を阻止する点で利害が一致した。こうして世界は、インターナショナルおよび英米海洋陣営と、独露大陸同盟の対立を軸に、次なる大戦へ向かっていった。

## 帰結 / ゲームへの反映

- これは1936年初期の世界情勢の骨格そのもの。三陣営の対立構造 → 初期 faction・外交関係・陣営加盟の設計基盤。
- 独露大陸同盟（GER・RUS・ITA）は大陸覇権側、インターナショナル（FRA・SPR）は革命輸出側、英米海洋陣営（ENG・USA）は海洋通商側、という三つ巴 → AIの陣営行動・宣戦傾向の設計指針。
- 「英米とインターナショナルは思想対立だが反独露で利害一致」という捻れ → 中盤以降の外交イベント・同盟組み替えの種。

<!-- TODO: 三陣営の faction 実装（faction 定義、初期加盟国、guarantee/opinion、AI戦略）が未着手。ENTITIES.md の派閥表と本ファイルを正として設計すること。 -->

関連: [イタリアの戦後処理と国家主義王国化](1918_italy-postwar-nationalist-turn.md) / [スペイン第二共和政の前倒し成立とインターナショナル形成](1920_spanish-second-republic.md) / [世界恐慌の発生](1929_great-depression.md) / [1936年米大統領選とノックス政権](1936_us-presidential-election.md)
