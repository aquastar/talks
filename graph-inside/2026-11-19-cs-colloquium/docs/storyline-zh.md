# 故事线：每页讲什么，怎么讲（11 月 19 日 CS Department Colloquium，主线 30 页）

网址：https://aquastar.github.io/talks/graph-inside/2026-11-19-cs-colloquium/

## 一、整场只回答一个问题

**生成模型里面有没有一张图？** 全场三段，各给一个答案：

| 段落 | 页 | 回答 |
|---|---|---|
| 开场 | 1 到 7 | 问题是什么：我们用向量改模型，向量只说加了什么，不说影响到了哪里 |
| Part 1 语言 | 8 到 16 | 有，已发表：读出来的图能抓住考试发现不了的坏编辑 |
| Part 2 音乐 | 17 到 29 | 在验证：一张很小的图就能装下风格，听众的大脑可以当裁判 |
| 结尾 | 30 | 开场那张点云回来，画上图的边。"你的模型里有没有图？" |

## 二、最容易讲的方法：记住 8 句话，其余靠画面

不用背讲稿。每页只做两件事：**把标题当一句话说出来，点一下，说那一行要点。** 画面上的字不要念。

全场只需要背下面 8 句过渡话，这就是整场的骨架：

1. （第 2 页后）"To see why, one minute inside a language model."
2. （第 4 页后）"But the network itself is a graph, and there is more than one way to draw it."
3. （第 7 页后）"Part 1, language. First, all the ways we change a model after release."
4. （第 13 页后）"So the exam reads answers only. Our work asks one thing: read the change as a graph."
5. （第 16 页后）"That is language. Part 2: knowledge that is not text."
6. （第 21 页后）"Is there a graph inside the generator that tells us which edges it can draw? Start with the simplest graph of music."
7. （第 26 页后）"To test any graph we draw inside, we need a judge outside the model. In music that judge exists: a listener's brain."
8. （第 29 页后）"So, back to the picture from the start of the talk."

另外三个小习惯：
* **路标**：带 "graph N of 7" 标签的页，开口先说 "graph number N"。观众会觉得整场是一张一张的图串起来的。
* **Part 1 的节奏固定**：第 9 到 12 页都是"结果，然后代价（The catch）"，每页一分半。第一页讲清这个节奏，后面观众自己就跟上了。
* **计时检查点**：第 8 页开始时约 11 分钟，第 17 页约 27 分钟，第 27 页约 45 分钟，讲完约 51 分钟。哪个点晚了两分钟以上，就用第五节的压缩办法。

## 三、每页讲什么

括号里是建议时长（秒）。"说"后面是这页要说出口的一句话，可以直接用。

### 开场（1 到 7 页，约 11 分钟）

**1. 封面**（45）左边一张普通的神经网络，右边把它读成一张图，题目 Is There a Graph Inside Generative Models?
说："Left, a network everyone has seen. Right, the same network read as a graph. Is there such a graph inside a generative model?"

**2. Change one fact, and the next question goes wrong**（120，graph 1）先是 Space Needle 的照片，然后是它的知识图（Seattle，Washington，United States，dollar）。编辑把它改到 Paris，再问一步：哪个国家？模型还说 United States。
说："Change one edge, and every path through it must change. The edited model does not."

**3. What is inside a language model? One shared whiteboard**（120）3D 白板：每个词是一行数字，注意力在词之间搬信息，MLP 像一张查找表，最后一行读出 Seattle。来自 10 月那次。
说："A fact like this lives in fixed numbers, the weights, and every word reads and writes one shared whiteboard."

**4. Today we change and explain models with vectors**（120）上面一排四种手术画成它们加进去的矩阵：steer 是一个向量，edit 是秩 1，LoRA 是 B 乘 A，fine tune 是整块。下面点云里一支箭头把 Space Needle 推到 Paris，旁边的点悄悄动了。
说："The arrow says what we added. Nothing says what else moved, or should have."

**5. One network, five graphs**（120，graph 2）同一个网络，五种画法：权重图、关系图、输入图、共激活图、电路。来自 10 月那次。向下键是视觉模型里的电路和场景图原图。
说："Five graphs, one network. Which one you draw depends on what change you want to understand."

**6. A tiny graph is enough to represent a piece of music**（90，graph 3）Für Elise 动画，小球沿着音符图走，点一下有声音。
说："Nine notes, a few arrows, and this little graph already names the tradition a melody comes from, 70 percent of the time."

**7. Two claims for the rest of this talk**（45）主线一句，两个主张：语言（已发表），音乐（进行中）。
说："Vectors say what we changed. Only a graph can say where it went. Two claims, one per part."

### Part 1 语言（8 到 16 页，约 16 分钟）

**8. Seven kinds of surgery**（60）发布后的模型会被编辑、拼接、合并、剪枝、steering、去学习、微调。
说："Take them one at a time, each with its best known result and the catch."

**9. Merging**（105）两个微调加起来就有两种技能。点一下：Hammoud 的原图，混进一个没对齐的专家，所有考试都过，却会回答有害问题。剪枝在向下键里。
说："Every skill exam passes, and the merge now answers harmful requests."

**10. Steering**（105）一个方向就能关掉拒答（Arditi），但同一个向量会把很多单个输入推错方向（Tan）。下面是两篇的原图。
说："Right on average, wrong on many single inputs."

**11. Unlearning**（105）Lee 2024 原图：DPO 之后有毒的区域还在，只是绕开了。
说："One small push brings it back. Bypassed, not deleted."

**12. Where a fact lives is not where editing works**（105）Hase 2023 的原图：大多数事实几乎不住在第 6 层，可在第 6 层编辑照样成功。
说："Where a fact lives does not tell you where to edit it."

**13. Every surgery, three lessons**（75）每种手术都是一支箭头，考试过了里面却绕开了，任何内部分数都需要和随机对照比。
说："So we need a tool that compares the inside before and after a change."

**14. A missing path in the record means a worse answer, for every model**（150，CIKM 2026 已发表）左边病历知识图缺一条 allergy 边。点一下：论文 Table 9，5 个模型在有路径时都更准，差 20 到 30 分。再点：32.3% 的临床问题根本没有路径。
说："A graph tells which questions cannot be answered faithfully, before any model tries. That was the graph outside the model."

**15. What is a delta graph?**（150，graph 4，SDM 2026）编辑前后问同样的问题，看模型各部分之间的协同怎么变，前后相减就是这次编辑的指纹。
说："Same questions, same parts. The delta graph is the edit's fingerprint inside the model."

**16. Results: same checking budget, more bad edits caught**（120）100 个满分编辑里 56 个暗中是坏的，只查 20 个：随机抓到 11 个，按编辑器和模型 14 个，按 delta graph 17 个。右边是论文原图。
说："Same checking budget: at random 11 bad edits, by editor and model 14, by the delta graph 17."

### Part 2 音乐（17 到 29 页，约 23 分钟）

**17. Knowledge is not only text**（60）Gardner 和李飞飞：智能有很多种，语言只是一种。
说："Of these kinds, music is the one that carries emotion."

**18. Music is where emotion can be measured**（90）Picard、Minsky、Meyer 三张人物卡。Meyer 1956：音乐的情感来自被延迟或打破的期待。
说："Emotion lives in expectation: what comes next, and whether it arrives."

**19. This year's Nobel: a switch for neurons, made of light**（120）动画：蓝光一闪，神经元放电。右边：40 Hz 的声音让脑电节律跟着走。
说："A click is the simplest sound. Music is the richest one we can design. Could it be the switch?"

**20. Music already acts on the brain, as medicine**（90）动画：帕金森病人跟着节拍器走路。右边四种用途各一行。
说："Nobody knows which part of the music does the work. That is a modeling question."

**21. A new idea is a new edge, and so is a new style of music**（120）四本讲创造力的书和 Uzzi 2013：新想法就是旧想法之间的一条新边。下面是音乐流派家族树和我们 2017 年的 FusionGAN。
说："A new idea is a new edge. In 2017 we asked whether a model can draw one."

**22. Fold 88 keys into 12 scale degrees**（105，graph 3）手画的 Für Elise 开头九个音，折成 12 个音级，变成 12 乘 12 的表。两个播放键：原曲和从表里生成的曲子。
说："The right notes with the wrong sentences. That is a graph with one note of memory."

**23. Occam's razor: the simplest graph already names the tradition**（105，进行中）六个曲库，一阶图分类准确率 70.2%，随机是 17%。
说："144 numbers name the corpus."

**24. The longest memory sounds most like the style, because it copies**（150，进行中）现场投票：A 和 B 哪个是真巴赫？
说："The useful graph remembers a little and copies nothing long."

**25. Inside a music generator, music theory has a shape**（105，graph 5）探针能在 MusicGen 里读出乐理，音高在螺旋上，调性在五度圈上。
说："A probe tells us what is stored, not how the states move."

**26. Steering leaves a style easily but rarely enters one**（105，graph 6，合作工作投稿中）去掉一个风格很容易，加进去却很难。
说："A vector cannot explain that. Reachability on a graph could."

**27. A note transition graph predicts the listening brain**（105，graph 7）Di Liberto 2020 原图：IDyOM 给每个音一个意外值，听众的脑电在 350 毫秒内跟着它走。
说："The listening brain tracks a graph of note transitions. So the brain can judge a graph."

**28. Live: what MusicGen expects, next to what listeners' brains do**（135，进行中）现场 demo：选一首歌播放，乐谱、MusicGen 的意外值、脑电一起滚动。
说："This is the measurement we built. Note by note, it does not yet beat an untrained model, and the next slide is how we test it properly."

**29. Our plan: a graph from inside MusicGen, judged by the brain**（75，计划）从 MusicGen 内部读出图，和 IDyOM、MusicGen 输出一起比谁更能解释大脑。
说："If the graph inside the generator explains the listener, the graph is real."

### 结尾（30 页，约 1.5 分钟）

**30. A vector says what we added. A graph shows where it went.**（90）第 4 页的点云回来，同一支箭头。点一下画出图的边。再点：今天的七张图。最后："Is there a graph inside your model?"
说："Language, published. Music, being tested. If you edit, merge or steer models, or run an EEG or hearing lab, I would love to talk." 不说 thank you。

## 四、这次相对上一版改了什么

* 封面换回 10 月那次的画面（左边网络，右边读成图），标题用这次的。
* 第 3 页 3D 白板、第 5 页 One network, five graphs 从 10 月那次搬回主线。观众先知道模型里面长什么样，再听"模型里的图"。
* 视觉模型那页（Olah 和场景图原图）移到第 5 页下面的备用页。

## 五、超时怎么压

按顺序：
1. 第 17 页只说一句（省 30 秒）
2. 第 24 页不投票，直接放 B（省 45 秒）
3. 第 28 页只演示一个意外的音（省 45 秒）
4. 第 9 到 11 页每页只说结果和代价各一句（省 1 分钟）

每页的备用页在向下键里，有人问到再翻。
