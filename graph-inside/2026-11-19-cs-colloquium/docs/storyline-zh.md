# 故事线：每页讲什么，怎么讲（11 月 19 日 CS Department Colloquium，主线 29 页）

网址：https://aquastar.github.io/talks/graph-inside/2026-11-19-cs-colloquium/

## 一、整场只回答一个问题

**生成模型里面有没有一张图？** 全场三段，各给一个答案：

| 段落 | 页 | 回答 |
|---|---|---|
| 开场 | 1 到 5 | 两层图：模型图和知识图，在语言、音乐、图像里都有 |
| Part 1 语言 | 6 到 15 | 有，已发表：读出来的图能抓住考试发现不了的坏编辑 |
| Part 2 音乐 | 16 到 28 | 在验证：一张很小的图就能装下风格，听众的大脑可以当裁判 |
| 结尾 | 29 | 开场那张点云回来，画上图的边。"你的模型里有没有图？" |

## 二、最容易讲的方法：记住 8 句话，其余靠画面

不用背讲稿。每页只做两件事：**把标题当一句话说出来，点一下，说那一行要点。** 画面上的字不要念。

全场只需要背下面 8 句过渡话，这就是整场的骨架：

1. （第 2 页后）"And what the network knows is a graph too."
2. （第 3 页后）"And it is not only facts."
3. （第 5 页后）"Part 1, language, the top row. First, one minute inside a language model."
4. （第 12 页后）"What we need is to compare the inside before and after a change."
5. （第 15 页后）"That is language. Part 2: knowledge that is not text."
6. （第 20 页后）"Is there a graph inside the generator that tells us which edges it can draw? Start with the simplest graph of music."
7. （第 25 页后）"To test any graph we draw inside, we need a judge outside the model. In music that judge exists: a listener's brain."
8. （第 28 页后）"So, back to the picture from the start of the talk."

另外三个小习惯：
* **路标**：带 "graph N of 7" 标签的页，开口先说 "graph number N"。观众会觉得整场是一张一张的图串起来的。
* **Part 1 的节奏固定**：第 9 到 12 页都是"结果，然后代价（The catch）"，每页一分半。第一页讲清这个节奏，后面观众自己就跟上了。
* **计时检查点**：第 8 页开始时约 11 分钟，第 17 页约 27 分钟，第 26 页约 44 分钟，讲完约 51 分钟。哪个点晚了两分钟以上，就用第五节的压缩办法。

## 三、每页讲什么

括号里是建议时长（秒）。"说"后面是这页要说出口的一句话，可以直接用。

### 开场（1 到 5 页，约 9 分钟）两层图：模型图（网络本身）和知识图（网络存的东西）

**1. 封面**（45）左边网络里亮起语言（蓝）和音乐（紫）两条路径，右边读成两张带标签的小图。
说："Left, a network. Right, what it knows, read as graphs, in language and in music. Is there such a graph inside a generative model?"

**2. Level 1: a language model is itself a graph**（120，graph 1）模型图。点一下：结构连接（谁能写给谁，架构定死的）。再点：功能连接（哪些块一起激活）。再点：电路，一个 MLP 查事实，一个注意力块把它搬到 Seattle。
说："The network itself is a graph: its wiring is fixed, its circuits change with what it is asked." 可以补一句：脑科学里也这样分，structural 和 functional connectivity。

**3. Change one fact, and the next question goes wrong**（120，graph 2）知识图。全景照，知识图，编辑改到 Paris，再问一步三个问题都答旧的。
说："Change one edge, and every path through it must change. The model does not."

**4. Beyond text: inside a music model, music theory has a shape**（105，graph 3）MusicGen 里音高沿螺旋上升（会转、逐个点亮），调性排在一个圆上（依次点亮）。视觉的例子放在备用页。
说："Pitch climbs a spiral, one turn per octave. Keys sit on a circle where neighbors share 6 of 7 notes. Nobody taught MusicGen music theory."
* 五度圈：把 12 个调排成一圈，相邻两个调的 7 个音里有 6 个相同，比如 C 大调和 G 大调只差一个音（F 和 F♯）。

**5. Two levels, two domains: the map of this talk**（60）2 乘 2 的地图，不写状态。语言：delta graph（第一层）和知识图（第二层）。音乐：MusicGen 里有没有图（第一层，开放问题）和音符图（第二层）。
说："Language has answers. Music is where the open questions are."

### Part 1 语言（6 到 15 页，约 17 分钟）主线：考试都过了，里面却绕了道，编辑的静默失败，一张表总结，我们的两篇工作

**6. Seven kinds of surgery**（60）七张卡片排成 4 加 3。
说："Every one of these is accepted by an exam that only looks at answers."

**7. Today we change and explain models with vectors**（90）放回主线：这七种手术写下来，都是往模型上加一个向量或矩阵。第一次说出主线。
说："Vectors say what we changed. Only a graph can say where it went."

**8. Merging**（105）先说限制：只能合并同一个底座模型微调出来的版本。两个箭头相加，两种技能都有。点一下：混进一个没对齐的专家，所有考试都过，却会回答有害问题。
说："Every skill exam passes, and the merge now answers harmful requests."

**9. Steering**（105）上面一行说明 steering 是什么：模型运行时在某一层加一个方向 r。点一下：平均有效，去掉拒答方向，模型几乎不再拒答（Arditi）。再点：逐个输入看，很多点被推反（Tan）。
说："Right on average, wrong on many single inputs."

**10. Unlearning**（120）三步：找到有毒的 MLP 向量，DPO 没删它们，只学了一个小偏移绕开（紫色箭头），把偏移撤掉，毒性就回来。
说："Unlearning hides, it does not delete."

**11. Editing: the edit adds a shortcut, and the old fact is still inside**（150）这是我们工作针对的失败。编辑没覆盖旧事实，只是加了一条近路。换一种问法旧答案回来（Xie 2025）。改了微软创始人，问"他上的哪所大学"，41% 答 Steve Jobs，编辑前 0.27%（Zhang 2025）。
说："The exam says pass, and nothing tells you which edits are like this. That is a silent failure."

**12. Every surgery: the exam passes, the inside tells another story**（75）一张表：合并、steering、unlearning、编辑，左边"考试说什么"，右边"模型里面其实是什么"。
说："The exam reads answers. What we need is to compare the inside before and after a change, and flag the risky ones."

**13. What is a delta graph?**（150，第一层模型图，SDM 2026）
说："Same questions, same parts. The delta graph is the edit's fingerprint inside the model."

**14. Results**（120）只查 20 个：随机 11 个，按编辑器和模型 14 个，按 delta graph 17 个。
说："Same budget, 17 instead of 11."

**15. A missing path in the record means a worse answer, for every model**（150，第二层知识图，CIKM 2026）
说："A graph tells which questions cannot be answered faithfully, before any model tries. That is language."

### Part 2 音乐（16 到 28 页，约 22 分钟）

**16. Part 2. Knowledge is not only text**（120）五个人，五个角度，一个结论：智能不只在语言里。梅洛-庞蒂 1945（管风琴手一小时适应一台新琴，靠手不靠句子），Gardner 1983，Picard 1997，Minsky 2006，李飞飞 2025。点一下：Meyer 1956，音乐的情感来自被延迟或打破的期待。
说："Five people, five angles, one point: intelligence is more than words. And in music, emotion lives in expectation."

**17. This year's Nobel: a switch for neurons, made of light**（120）左边三步：病毒把藻类的一个基因送进选定的神经元，神经元在膜上造出光控通道（蓝点），蓝光一照通道打开，离子涌入，神经元放电。光本身没用，是基因让细胞"听得见"光，所以精准，但要开刀。右边：不开刀，每秒 40 次的声音从耳朵进去，脑电节律跟着节拍走。向下键有一段 BrainFacts.org 的科普视频。
说："The light alone does nothing, the gene makes the cell listen to light. Through the ear, no gene and no surgery, the brain rhythm follows the beat. A click is the simplest sound, music is the richest one we can design."

**18. Optogenetics in two minutes**（60 到 120，可选）BrainFacts.org 的科普视频，点画面中间的播放键。要联网，要从网址打开（本地双击打开的文件会报 Error 153）。时间紧就只放第一分钟，或者跳过。

**19. Music already acts on the brain, as medicine**（90）动画：帕金森病人跟着节拍器走路。右边四种用途各一行。
说："Nobody knows which part of the music does the work. That is a modeling question."

**20. A new idea is a new edge, and so is a new style of music**（120）四本讲创造力的书和 Uzzi 2013：新想法就是旧想法之间的一条新边。下面是音乐流派家族树和我们 2017 年的 FusionGAN。
说："A new idea is a new edge. In 2017 we asked whether a model can draw one."

**21. A tiny graph is enough to represent a piece of music**（90）Für Elise 动画，小球沿着音符图走，点一下有声音。从开场移到这里。
说："Nine notes, a few arrows. The whole model is the graph."

**22. Fold 88 keys into 12 scale degrees**（105，graph 3）手画的 Für Elise 开头九个音，折成 12 个音级，变成 12 乘 12 的表。两个播放键：原曲和从表里生成的曲子。
说："The right notes with the wrong sentences. That is a graph with one note of memory."

**23. Occam's razor: the simplest graph already names the tradition**（105，进行中）六个曲库，一阶图分类准确率 70.2%，随机是 17%。
说："144 numbers name the corpus."

**24. The longest memory sounds most like the style, because it copies**（150，进行中）现场投票：A 和 B 哪个是真巴赫？
说："The useful graph remembers a little and copies nothing long."

**25. Steering leaves a style easily but rarely enters one**（105，graph 6，合作工作投稿中）去掉一个风格很容易，加进去却很难。
说："A vector cannot explain that. Reachability on a graph could."

**26. A note transition graph predicts the listening brain**（105，graph 7）Di Liberto 2020 原图：IDyOM 给每个音一个意外值，听众的脑电在 350 毫秒内跟着它走。
说："The listening brain tracks a graph of note transitions. So the brain can judge a graph."

**27. Live: what MusicGen expects, next to what listeners' brains do**（135，进行中）现场 demo，全屏，可以直接点：选一首歌播放，乐谱、MusicGen 的意外值、脑电一起滚动。点过 demo 后方向键留在 demo 里，用右下角的 Next slide 按钮翻页。
说："This is the measurement we built. Note by note, it does not yet beat an untrained model, and the next slide is how we test it properly."

**28. Our plan: a graph from inside MusicGen, judged by the brain**（75，计划）从 MusicGen 内部读出图，和 IDyOM、MusicGen 输出一起比谁更能解释大脑。
说："If the graph inside the generator explains the listener, the graph is real."

### 结尾（29 页，约 1.5 分钟）

**29. A vector says what we added. A graph shows where it went.**（90）第 4 页的点云回来，同一支箭头。点一下画出图的边。再点：今天的七张图。最后："Is there a graph inside your model?"
说："Language, published. Music, being tested. If you edit, merge or steer models, or run an EEG or hearing lab, I would love to talk." 不说 thank you。

## 四、这次相对上一版改了什么

* 封面换回 10 月那次的画面（左边网络，右边读成图），标题用这次的。
* 第 3 页 3D 白板、第 5 页 One network, five graphs 从 10 月那次搬回主线。观众先知道模型里面长什么样，再听"模型里的图"。
* 视觉模型那页（Olah 和场景图原图）移到第 5 页下面的备用页。

## 五、超时怎么压

按顺序：
1. 第 17 页五个人只点名，不逐个讲（省 1 分钟）
2. 第 23 页不投票，直接放 B（省 45 秒）
3. 第 27 页只演示一个意外的音（省 45 秒）
4. 第 9 到 11 页每页只说结果和代价各一句（省 1 分钟）

每页的备用页在向下键里，有人问到再翻。
