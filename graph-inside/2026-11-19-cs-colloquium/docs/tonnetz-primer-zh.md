# Tonnetz 与 P、R、L：讲第 7 页前要懂的乐理

给第 7 页准备。从零讲起，不需要乐理基础。

## 1. 最少的乐理

- 钢琴上一个八度有 12 个键（7 白 5 黑），然后重复。音名是 C、D、E、F、G、A、B，黑键用升号（♯）或降号（♭）表示，比如 E♭ 就是 E 左边那个黑键。
- 相邻两个键（包括黑键）的距离叫一个半音。两个音的距离（音程）就数半音：
  - 小三度 = 3 个半音（C 到 E♭）
  - 大三度 = 4 个半音（C 到 E）
  - 纯五度 = 7 个半音（C 到 G）
- 12 个半音以后回到同名音（C 到高八度的 C），所以音高可以看成模 12 的整数：C=0，C♯=1，……，B=11。

## 2. 和弦就是三个数

- 大三和弦：根音，加 4，再加 3。C 大调和弦 = C, E, G = {0, 4, 7}。听起来明亮。
- 小三和弦：根音，加 3，再加 4。A 小调和弦 = A, C, E = {9, 0, 4}。C 小调 = C, E♭, G = {0, 3, 7}。听起来暗。
- 12 个根音乘以大小两种，一共 24 个和弦。流行歌和古典音乐里大部分和弦都是这 24 个。

## 3. Tonnetz 怎么画

欧拉 1739 年在《Tentamen novae theoriae musicae》里画了一张音的网格。今天的标准画法：

- 横向每走一步加 7（五度）：C, G, D, A, E, ……
- 右上每走一步加 4（大三度）：C, E, G♯, C（三步回到 C）
- 于是左上每走一步是减 3（小三度往下）

神奇的地方是：
- 每个**朝上**的小三角形是 {p, p+4, p+7}，正好是一个**大三和弦**。
- 每个**朝下**的小三角形是 {p, p+3, p+7}，正好是一个**小三和弦**。

24 个和弦，每个都是网格上的一个三角形，不多也不少。

## 4. 邻居就是 P、R、L

两个三角形共享一条边，就是两个和弦共享两个音，只有一个音不同。每个三角形有三条边，所以每个和弦正好有三个邻居。以 C 大调（C, E, G）为例：

| 名字 | 英文 | 去哪 | 谁动 |
|---|---|---|---|
| P | Parallel | C 小调 (C, E♭, G) | E 降半音到 E♭ |
| R | Relative | A 小调 (A, C, E) | G 升全音到 A |
| L | Leading tone exchange | E 小调 (E, G, B) | C 降半音到 B |

- 每个操作做两次就回到原处（P 再 P 回到 C 大调）。
- 大调和小调互换，P、R、L 只是方向反过来。

**为什么这样走好听**：想象四个人合唱，从一个和弦换到下一个，每个人都想少挪动。P、R、L 每次只有一个人动一两个半音，其他人原地不动，所以听起来最顺。对比 C 大调到 F♯ 大调：三个音全换，在网格上也离得最远。**网格上的距离近似于耳朵听到的距离**，这就是为什么它像一张知识图谱：节点是概念，边是有意义的关系。

## 5. 黎曼是谁

- 这里是 **Hugo Riemann**（1849 to 1919），德国音乐理论家，不是数学家 Bernhard Riemann，只是同姓。
- 19 世纪下半叶，Riemann 和 Arthur von Oettingen 拿欧拉的网格来分析和声，重点从"和弦是什么"转到"和弦之间怎么变"。
- 1987 年 David Lewin 出版《Generalized Musical Intervals and Transformations》，把这些变化写成作用在和弦集合上的函数，用群论来处理。
- 1990 年代 Richard Cohn 等人发展出一个流派，致敬 Riemann，叫**新黎曼理论**（Neo-Riemannian theory）。P、R、L 这套记号就来自这里。

## 6. 给 CS 听众的数学（可选讲）

- **它是一张图**：24 个节点，每个节点正好 3 条边（3 正则图）。
- **它是一个环面**：音高模 12，网格横着走 12 步、斜着走 3 步都会绕回来，所以整张网铺在一个甜甜圈表面上。
- **它是一个群**：P、R、L 生成的群同构于 24 阶二面体群。它在 24 个和弦上的作用是单一传递的：任意两个和弦之间，正好对应群里的一个元素，所以从任何一个和弦都能走到任何一个和弦。
- **两个好玩的环**：
  - L、R 交替：C → Em → G → Bm → D → ……，每两步移动一个五度，走完全部 24 个和弦才回来。幻灯片动画最后两步就是这个。
  - P、L 交替（Cohn 的六音环 hexatonic cycle）：C → Cm → A♭ → A♭m → E → Em → C。只要 6 步，每步只动一个半音，却跳到了很远的调。19 世纪的作曲家（李斯特、瓦格纳）很爱用这种走法，传统功能和声不好解释，在 Tonnetz 上就是一条直线。

## 7. 三本书，一句话各一本

- David Lewin, *Generalized Musical Intervals and Transformations*, Yale University Press 1987（Oxford 2007 重印）：把 P、R、L 变成数学的源头。
- Dmitri Tymoczko, *A Geometry of Music*, Oxford University Press 2011：和弦是空间里的点，好的和声进行就是短距离移动。
- David Sulzer, *Music, Math, and Mind*, Columbia University Press 2021：音乐背后的物理和神经科学，写给一般读者。
- 参考：Richard Cohn, *Audacious Euphony*, Oxford University Press 2012，讲 Tonnetz 和六音环最完整的一本。

## 8. 台上 30 秒怎么讲（英文）

"Music theory has its own graph. Euler drew it in 1739. Notes are nodes. Every small triangle is a chord: point up is major, point down is minor. Two chords that share an edge share two notes, so you move between them by changing one note. Watch: P moves one note and C major becomes C minor. R, A minor. L, E minor. Music theorists call these the neo-Riemannian moves, after Hugo Riemann, the music theorist, not the mathematician. And there are whole books on this, a field called the mathematics of music. I read this lattice as a knowledge graph of music. The question for the model: are these concepts inside?"

## 9. 可能被问到的问题

- **模型里真的有这张网吗？** Wei 2024 证明的是和弦类型、音程、调性这些概念能从一层读出来，没有测网格的边。测"C 大调和 E 小调在模型里是不是比 C 大调和 F♯ 大调更近"是一个开放问题，我们没有做系统检索，可以说"as far as I know, no one has tested the lattice distances in MusicGen yet"。
- **为什么不用五度圈？** 五度圈只排了 12 个调，是一个环。Tonnetz 同时编码五度和三度，24 个和弦全在上面，邻接关系有明确的声部进行意义，信息更多。
- **这是知识图谱吗？** 原文不这么叫。这是我们的读法：概念（和弦）加上有类型的关系（P、R、L），和知识图谱同构。
