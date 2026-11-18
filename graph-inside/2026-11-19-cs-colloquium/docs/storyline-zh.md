# 故事线：每页讲什么，怎么讲（11 月 19 日 CS Department Colloquium，主线 31 页）

网址：https://aquastar.github.io/talks/graph-inside/2026-11-19-cs-colloquium/

## 一、整场只回答一个问题

**生成模型里面有没有一张图？** 全场三段，各给一个答案：

| 段落 | 页 | 回答 |
|---|---|---|
| 开场 | 1 到 8 | 两层图：模型图和知识图，在语言、音乐、图像里都有 |
| Part 1 语言 | 8 到 17 | 有，已发表：读出来的图能抓住考试发现不了的坏编辑 |
| Part 2 音乐 | 16 到 27 | 在验证：一张很小的图就能装下风格，听众的大脑可以当裁判 |
| 结尾 | 28 | 开场那张点云回来，画上图的边。"你的模型里有没有图？" |

## 二、最容易讲的方法：记住 8 句话，其余靠画面

不用背讲稿。每页只做两件事：**把标题当一句话说出来，点一下，说那一行要点。** 画面上的字不要念。

全场只需要背下面 8 句过渡话，这就是整场的骨架：

1. （第 2 页后）"And what the network knows is a graph too."
2. （第 3 页后）"And it is not only facts."
3. （第 5 页后）"Part 1, language, the top row. First, one minute inside a language model."
4. （第 12 页后）"What we need is to compare the inside before and after a change."
5. （第 15 页后）"That is language. Part 2: knowledge that is not text."
6. （第 19 页后）"Is there a graph inside the generator that tells us which edges it can draw? Start with the simplest graph of music."
7. （第 24 页后）"To test any graph we draw inside, we need a judge outside the model. In music that judge exists: a listener's brain."
8. （第 27 页后）"So, back to the picture from the start of the talk."

另外三个小习惯：
* **路标**：带 "graph N of 7" 标签的页，开口先说 "graph number N"。观众会觉得整场是一张一张的图串起来的。
* **Part 1 的节奏固定**：第 9 到 12 页都是"结果，然后代价（The catch）"，每页一分半。第一页讲清这个节奏，后面观众自己就跟上了。
* **计时检查点**：第 8 页开始时约 11 分钟，第 17 页约 27 分钟，第 26 页约 44 分钟，讲完约 51 分钟。哪个点晚了两分钟以上，就用第五节的压缩办法。

## 三、每页讲什么

括号里是建议时长（秒）。"说"后面是这页要说出口的一句话，可以直接用。

### 开场（1 到 8 页，约 9 分钟）两层图：模型图（网络本身）和知识图（网络存的东西）

**1. 封面**（45）左边网络里亮起语言（蓝）和音乐（紫）两条路径，右边读成两张带标签的小图。
说："Left, a network. Right, what it knows, read as graphs, in language and in music. Is there such a graph inside a generative model?"

**2. Level 1: a language model is itself a graph**（120，graph 1）先互动：只给照片和问号，问大家"The Space Needle is in the city of ...?"，答案只能是一个城市名。点一下，各层从左到右依次点亮，一条橙色路径画过去（MLP 查到事实，注意力块搬到答案）。再点，问号变成城市的概率分布，Seattle 最高，其他城市很低（示意）。这就像 1 + 1 = 2，是很确定的知识，用不着"生成"。再点：就算让它随机，也不随机，网上（Reddit 等）广为流传，让聊天机器人在 1 到 30 里挑一个数，它经常说 17。
说："The answer is a distribution, yet much of what a model says is held in place by strong, stored structure, closer to a graph than to a coin."

**3. Change one fact, and the next question goes wrong**（120，graph 2）左边 Space Needle 照片，中间两个小知识图（上：Seattle、Washington、United States、dollar；下：Paris、France、euro）。右边四个问题一开始就在，编辑前四个答案都对、彼此一致。点一下：箭头从 Seattle 摆到 Paris，同时右边更新，第一个问题变成 Paris，其他三个没变，于是互相矛盾，标红，上面的旧路径变红。再点："One answer fixed. Every other question still walks the old graph." 最后一下抛出研究问题："is there a link between the circuit graph of the model and this knowledge graph?"
说："Before the edit, all four agreed. After it, a Space Needle in Paris, in the United States, in Washington, paid in dollars. The edit changed one edge and never looked at the graph around it."

**4. One network, four graphs**（90）四种图 2×2 排列：circuit graph（电路图）、神经元群图、输入图、共激活图。点一下：其余变淡，circuit graph 亮出承载答案的橙色子图并加橙框。底部问题里 "circuit graph" 和 "knowledge graph" 两个词加了底色："Our question: does the circuit graph somehow encode the knowledge graph?"
说："The circuit graph is the small part of the network that carries one answer. Does it encode the knowledge graph?"

**5. Knowledge is not only text**（120，从 Part 2 挪到开场，做文字到音乐的过渡）五个人，五个角度，一个结论：智能不只在语言里。梅洛-庞蒂 1945（管风琴手一小时适应一台新琴，靠手不靠句子），Gardner 1983，Picard 1997，Minsky 2006，李飞飞 2025。点一下：Meyer 1956，音乐的情感来自被延迟或打破的期待。
说："Five people, five angles, one point: intelligence is more than words. And in music, emotion lives in expectation."

**6. A music generator is a language model, with a pitch graph inside**（105，graph 3）上方一行讲编码：音频经过 EnCodec 变成 token（每 20 毫秒 4 个整数，像词一样），交给和 GPT 一样的 transformer 预测下一个 token，再解码成音乐。点一下，左边：乐理的音高图，C D E F G A B 排成一行，每个音和高八度的同名音相连（C 那条边是橙色）。再点，右边：模型学出的螺旋（Yagi 2026）。要说清楚这是模型的向量空间：每个点是一个音输入后的激活向量，投影到三维。螺旋边转边长出来，停下后所有白键音名都标着，C3、C4、C5 竖着对齐，就是左边那条橙色边。底部：模型学出的图和乐理的知识图一致。
说："A music generator is a language model over sound tokens. Music theory links every note to the same note an octave up. Inside the model, in its vector space, those notes line up on a helix: the learned graph matches the knowledge graph."

**7. Do music generation models encode music theory?**（105）标题就是 Wei 2024 那篇论文的题目。左边：Tonnetz 网格（欧拉 1739），动画自己循环播放：从 C 大调出发，依次演示 P（到 C 小调）、R（到 A 小调）、L（到 E 小调），每次只有一个音变成橙色实心，就是动的那个音。最后连走 L、R 两步到 G 大调。下面三本书（Lewin 1987，Tymoczko 2011，Sulzer 2021）说明这是一个完整的研究领域。可以说：我把它读作音乐的知识图谱。注意 Wei 测的是概念读得出来，不是这张网的边。乐理细节见 docs/tonnetz-primer-zh.md。点一下，右边：论文图 1 的实验流程，加上探针准确率：音乐模型 0.93 到 0.98，人工乐理特征 0.88，原始音频 token 0.70。橙色竖线标出"音乐模型"这一组，不再单独突出某一个模型。底部：乐理的概念就在模型里，一层就能读出来，从声音里自己学的。
说："The input tokens give 70 percent, the model's layers give 93 to 98. The knowledge was built inside, from sound alone."

**8. Two levels, two domains: the map of this talk**（60）2 乘 2 的地图，不写状态。语言：delta graph（第一层）和知识图（第二层）。音乐：MusicGen 里有没有图（第一层，开放问题）和音符图（第二层）。
说："Language has answers. Music is where the open questions are."

### Part 1 语言（8 到 17 页，约 17 分钟）主线：考试都过了，里面却绕了道，编辑的静默失败，一张表总结，我们的两篇工作

**9. Seven kinds of surgery**（60）七张卡片排成 4 加 3。
说："Every one of these is accepted by an exam that only looks at answers."

**10. Today we change and explain models with vectors**（90）放回主线：这七种手术写下来，都是往模型上加一个向量或矩阵。第一次说出主线。
说："Vectors say what we changed. Only a graph can say where it went."

**11. Merging**（105）先说限制：只能合并同一个底座模型微调出来的版本。两个箭头相加，两种技能都有。点一下：混进一个没对齐的专家，所有考试都过，却会回答有害问题。
说："Every skill exam passes, and the merge now answers harmful requests."

**12. Steering**（105）上面一行说明 steering 是什么：模型运行时在某一层加一个方向 r。点一下：平均有效，去掉拒答方向，模型几乎不再拒答（Arditi）。再点：逐个输入看，很多点被推反（Tan）。
说："Right on average, wrong on many single inputs."

**13. Unlearning**（120）三步：找到有毒的 MLP 向量，DPO 没删它们，只学了一个小偏移绕开（紫色箭头），把偏移撤掉，毒性就回来。
说："Unlearning hides, it does not delete."

**14. Knowledge editing bypasses the old fact instead of removing it**（整场主打的一点）（150）这是我们工作针对的失败。编辑没覆盖旧事实，只是加了一条近路。换一种问法旧答案回来（Xie 2025）。改了微软创始人，问"他上的哪所大学"，41% 答 Steve Jobs，编辑前 0.27%（Zhang 2025）。
说："The edit adds a bypass, the old fact is never removed. Why: an editor looks at one fact, not at the graph that fact sits in."

**15. Every surgery: the exam passes, the inside tells another story**（75）一张表：合并、steering、unlearning、编辑，左边"考试说什么"，右边"模型里面其实是什么"。
说："The exam reads answers. What we need is to compare the inside before and after a change, and flag the risky ones."

**16. What is a delta graph?**（150，第一层模型图，SDM 2026）
说："Same questions, same parts. The delta graph is the edit's fingerprint inside the model."

**17. Results**（120）只查 20 个：随机 11 个，按编辑器和模型 14 个，按 delta graph 17 个。
说："Same budget, 17 instead of 11."

**18. A missing path in the record means a worse answer, for every model**（150，第二层知识图，CIKM 2026）
说："A graph tells which questions cannot be answered faithfully, before any model tries. That is language."

### Part 2 音乐（16 到 27 页，约 22 分钟）

**19. Two signals that change the brain: light, and music**（75）类比，约一分钟，别在光遗传学上停留。左边（小）：光，今年诺奖的光遗传学，加一个基因让神经元能感光，一闪就放电，但要开刀。点一下，右边（大）：声音，音乐不用开刀，从耳朵进去也确实改变大脑。三个有测量的例子：脑电节律跟着节拍走（Nozaradan 2011），快感高峰时释放多巴胺（Salimpoor 2011），40 Hz 声音改变了小鼠大脑（Tsai 实验室）。大脑图是 Gray 解剖学第 728 图，公有领域，颞叶（听觉皮层）标橙并跟着节拍闪。光遗传学科普视频的链接在本页参考行最后。
说："Light switches neurons, but it needs a gene and surgery. Music already changes the brain, through the ear. Which part of the music does it is the open question."

**20. Music already acts on the brain, as medicine**（90）动画：帕金森病人跟着节拍器走路。右边四种用途各一行。
说："Nobody knows which part of the music does the work. That is a modeling question."

**21. Music and medicine, near us and nationally**（30，只分享，不展开）RIT：Hwan Shim、Sungyoung Kim、Matt Dye、Amanda Picioli。UR：Eastman Performing Arts Medicine，David Greenberg，音乐与老龄化试点基金，Norman-Haignere，Zhiyao Duan。全国：NIH Sound Health，NIH 音乐研究网络，NEA Sound Health Network。
说："Rochester already has the pieces: music, medicine, hearing and AI. If you work on any of them, talk to me."

**22. A new idea is a new edge, and so is a new style of music**（120）四本讲创造力的书和 Uzzi 2013：新想法就是旧想法之间的一条新边。下面是音乐流派家族树和我们 2017 年的 FusionGAN。
说："A new idea is a new edge. In 2017 we asked whether a model can draw one."

**23. A tiny graph is enough to represent a piece of music**（90）Für Elise 动画，小球沿着音符图走，点一下有声音。从开场移到这里。
说："Nine notes, a few arrows. The whole model is the graph."

**24. Fold 88 keys into 12 scale degrees**（105，graph 3）手画的 Für Elise 开头九个音，折成 12 个音级，变成 12 乘 12 的表。两个播放键：原曲和从表里生成的曲子。
说："The right notes with the wrong sentences. That is a graph with one note of memory."

**25. Occam's razor: the simplest graph already names the tradition**（105，进行中）六个曲库，一阶图分类准确率 70.2%，随机是 17%。
说："144 numbers name the corpus."

**26. The longest memory sounds most like the style, because it copies**（150，进行中）现场投票：A 和 B 哪个是真巴赫？
说："The useful graph remembers a little and copies nothing long."

**27. Steering leaves a style easily but rarely enters one**（105，graph 6，合作工作投稿中）去掉一个风格很容易，加进去却很难。
说："A vector cannot explain that. Reachability on a graph could."

**28. A note transition graph predicts the listening brain**（105，graph 7）Di Liberto 2020 原图：IDyOM 给每个音一个意外值，听众的脑电在 350 毫秒内跟着它走。
说："The listening brain tracks a graph of note transitions. So the brain can judge a graph."

**29. Live: what MusicGen expects, next to what listeners' brains do**（135，进行中）现场 demo，全屏，可以直接点：选一首歌播放，乐谱、MusicGen 的意外值、脑电一起滚动。点过 demo 后方向键留在 demo 里，用右下角的 Next slide 按钮翻页。
说："This is the measurement we built. Note by note, it does not yet beat an untrained model, and the next slide is how we test it properly."

**30. Our plan: a graph from inside MusicGen, judged by the brain**（75，计划）从 MusicGen 内部读出图，和 IDyOM、MusicGen 输出一起比谁更能解释大脑。
说："If the graph inside the generator explains the listener, the graph is real."

### 结尾（28 页，约 1.5 分钟）

**31. A vector says what we added. A graph shows where it went.**（90）第 4 页的点云回来，同一支箭头。点一下画出图的边。再点：今天的七张图。最后："Is there a graph inside your model?" 右边有本幻灯片的二维码，下面是外链图标加 zhiqian.ai/talks。讲完就停在这一页，留给大家扫。
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
