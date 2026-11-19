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

**3. Change one fact, and the next question goes wrong**（120，graph 2）左边 Space Needle 照片，中间两个小知识图（上：Seattle、Washington、United States、dollar。下：Paris、France、euro）。右边四个问题一开始就在，编辑前四个答案都对、彼此一致。点一下：箭头从 Seattle 摆到 Paris，同时右边更新，第一个问题变成 Paris，其他三个没变，于是互相矛盾，标红，上面的旧路径变红。再点："One answer fixed. Every other question still walks the old graph." 最后一下抛出研究问题："is there a link between the circuit graph of the model and this knowledge graph?"
顶部第一行（灰）：为什么需要知识编辑。事实经常变，每次都重新 fine-tune 大模型很贵，知识编辑只改少量权重，很便宜。第二行：同一个工具也能拿来攻击。核心观点：事实是三元组（subject, predicate, object），比如 (Space Needle, located in, Seattle)。攻击只改了一个三元组，但三元组不是独立存在的，改一个而不管周围的，模型就自相矛盾。结论框写的就是这句。这是一个攻击的例子：知识编辑本来用来修正错误的事实，同一个工具也能把假事实写进模型，这里写的是 Space Needle 在巴黎。左边标签写 the attack: located in Paris，顶部一行写 An attack: knowledge editing writes one false fact into the model, and leaves the related facts untouched.
动画顺序：进来时只有图和第一个问题（城市，✓ Seattle）。点一下，Seattle 到 Washington 的边亮起来（橙色），出现第二个问题（州，✓ Washington）。再点，Washington 到 United States 亮，出现国家问题。再点，United States 到 dollar 亮，出现货币问题。再点：攻击，箭头摆到 Paris，城市变成 Paris，其他三个一起变成红叉，上面的路径变红。最后一下：Before the edit all four agreed. Now they contradict. 加结论框。
说："Before the edit, all four agreed. After it, a Space Needle in Paris, in the United States, in Washington, paid in dollars. The edit changed one edge and never looked at the graph around it."

**4. One network, four graphs**（90）四种图 2×2 排列：circuit graph（电路图）、神经元群图、输入图、共激活图。点一下：其余变淡，circuit graph 亮出承载答案的橙色子图并加橙框。底部问题里 "circuit graph" 和 "knowledge graph" 两个词加了底色："Our question: does the circuit graph somehow encode the knowledge graph?"
说："The circuit graph is the small part of the network that carries one answer. Does it encode the knowledge graph?"

**5. Knowledge is not only text**（120，从 Part 2 挪到开场，做文字到音乐的过渡）五个人，五个角度，一个结论：智能不只在语言里。梅洛-庞蒂 1945（管风琴手一小时适应一台新琴，靠手不靠句子），Gardner 1983，Picard 1997，Minsky 2006，李飞飞 2025。点一下：Meyer 1956，音乐的情感来自被延迟或打破的期待。
说："Five people, five angles, one point: intelligence is more than words. And in music, emotion lives in expectation."

**6. A music generator is a language model, with a pitch graph inside**（105，graph 3）上方一行讲编码：音频经过 EnCodec 变成 token（每 20 毫秒 4 个整数，像词一样），交给和 GPT 一样的 transformer 预测下一个 token，再解码成音乐。点一下，左边：乐理的音高图，C D E F G A B 排成一行，每个音和高八度的同名音相连（C 那条边是橙色）。再点，右边：模型学出的螺旋（Yagi 2026）。要说清楚这是模型的向量空间：每个点是一个音输入后的激活向量，投影到三维。螺旋边转边长出来，一直慢慢转，白键音名跟着点走，C3、C4、C5 竖着对齐，就是左边那条橙色边。底部：模型学出的图和乐理的知识图一致。再点：右边三本书（Lewin 1987，Tymoczko 2011，Sulzer 2021），一句话带过：音乐背后的数学是一个完整的研究领域。
说："A music generator is a language model over sound tokens. Music theory links every note to the same note an octave up. Inside the model, in its vector space, those notes line up on a helix: the learned graph matches the knowledge graph."

**7. Do music generation models encode music theory?**（105，graph 3）左边：Tonnetz 网格（欧拉 1739），动画自己循环：从 C 大调出发，P 到 C 小调，R 到 A 小调，L 到 E 小调，最后连走 L、R 到 G 大调，每一步只有一个音变成橙色实心。亮着的三角形三条边上标着音程：横边 +7，右上斜边 +4，左上斜边 +3。下面两行图例：横向箭头是五度（+7），右上箭头是大三度（+4）。尖朝上的三角形是大调（根音、+4、+7），尖朝下是小调（根音、+3、+7）。
说："Music theory already has a knowledge graph of chords: every triangle is a chord, and two chords that share an edge differ by one note."
点一下，右边：Ebrahimzadeh, Bernardes, Stober，ISMIR 2026，word2vec 在贝多芬和披头士的和弦序列上学出的 24 个和弦地图（按他们 Figure 1a 重画）。同时开始第一节动画：五度是共同的骨架，左边从左往右走 D、A、E、B，每步一个五度，右边光圈沿着圆环同步一格一格走同样的和弦。
再点，第二节动画：一个调在两边都是一块连续区域。C 大调的六个和弦 Dm、F、Am、C、Em、G，在左边是一条连在一起的三角形带，在右边是圆环上的一段弧。
再点：结论框。
说："The fifths are the shared backbone. And a key is one strip on the lattice, one arc in the model."
诚实的边界：这是一个在和弦符号上训练的小模型，不是从声音学的生成模型。右下角写着 Open question：像 MusicGen 这样从声音学的模型，有没有同样的和弦距离，据你所知还没人测过。被问到时可以补充 Wei 2024：从 MusicGen 一层能读出和弦、音程、调（93% 到 98%），但他们没有测距离。乐理细节见 docs/tonnetz-primer-zh.md。

**8. Two levels, two domains: the map of this talk**（60）2 乘 2 的地图，不写状态。语言：delta graph（第一层）和知识图（第二层）。音乐：MusicGen 里有没有图（第一层，开放问题）和音符图（第二层）。
说："Language has answers. Music is where the open questions are."

### Part 1 语言（8 到 17 页，约 17 分钟）主线：考试都过了，里面却绕了道，编辑的静默失败，一张表总结，我们的两篇工作

**9. Seven kinds of surgery**（60）七张卡片排成 4 加 3。
说："Every one of these is accepted by an exam that only looks at answers."

**10. Today we change and explain models with vectors**（120）上面四种改模型的方式都是"加一个东西"（steer、edit、LoRA、fine-tune）。下面是示意点云（不是真数据）。点一下：橙色箭头把 Space Needle 推到 Paris，右边 "The arrow says what we added."。再点：Ripple effect（高亮）：相关事实（国家、货币）本该跟着动到 France、euro（虚线），但没动。再点：Locality（高亮）：一个无关的事实被顺带推偏了。
说："The arrow says what we added. It says nothing about the ripple effect, the facts that should move, or about locality, the facts that should stay."
被问到是否已解决：没有。2026 年做得更好的方法（circuit-aware editing、joint neighborhood optimization）都是从改一个点转向沿着结构改。
**11. Merging**（105）先说限制：只能合并同一个底座模型微调出来的版本。两个箭头相加，两种技能都有。点一下：混进一个没对齐的专家，所有考试都过，却会回答有害问题。
说："Every skill exam passes, and the merge now answers harmful requests."

**12. Steering: clean for some behaviors, unreliable for others**（120）上面：什么是 steering，推理时在某一层加一个方向 αr，不改权重。点一下，左边：干净的例子，Arditi 2024，13 个聊天模型里的拒绝方向，去掉它模型几乎不再拒绝。拒绝是一个干净的方向，所以向量能控制它。再点，右边：一般情况，Tan 2024，每种行为单独做一个 steering 向量，40 种行为里的 13 种，条形是被推反方向的输入比例（从他们 Figure 1 读出，四舍五入）：有的约为 0，有的接近一半（myopic-reward 49%，像抛硬币）。注意：右边不是拒绝向量失效，是同一种方法用在别的行为上。再点：A vector works when the behavior is one clean direction. It cannot tell you when it is not.
说："Steering works beautifully when the behavior is one clean direction, like refusal. For many other behaviors, close to half the inputs go the wrong way, and the vector alone cannot tell you which case you are in."
**13. Removing a behavior: hidden, not deleted**（120）三格图，每格一行字（Lee et al. 2024，GPT-2 medium，数字来自 Table 2 和 4）。
第 1 格：用 56 万条评论训练一个检测有毒文本的线性探针，它的权重就是"有毒方向"，找出和它最像的 7 个 MLP 神经元，它们一亮就写脏话。毒性 0.45。
点一下，第 2 格：用 DPO 训练，毒性降到 0.21。但这 7 个神经元几乎没变，前面的层学会了让输入绕过去（橙色绕行）。
再点，第 3 格：不训练，只把这 7 个神经元的 key 放大 10 倍，毒性回到 0.46。
再点：底部，unlearning 也一样（Hu 2025），少量无害微调就能让"遗忘"的事实回来。
注意：Lee 这篇是对齐（去毒），不是 unlearning。key 和 value 指 MLP 的，不是 attention 的。
说："The swear neurons were never removed. Training just learned a detour around them. Turn their keys up and the swearing is back."
**14. Knowledge editing bypasses the old fact instead of removing it**（150，全场重点，慢慢说）和第 13 页同一个机制，换成知识编辑。灰线是训练时学到的旧路径（Space Needle 到 Seattle）。编辑没碰它，只在第 2 层加了一条橙色捷径到 Paris。
点一下：考试题走捷径，答 Paris，pass。再点：换个问法（先提 Seattle），旧路径变红亮起，Seattle 回来了，"still there"。再点：实测。Xie 2025：精心设计的提示能找回旧答案（旧路径还在）。Zhang 2025：把微软创始人编辑成 Steve Jobs，再问"微软创始人上的哪所大学"，模型答 Steve Jobs 的比例从 0.27% 升到 41%（编辑是一条捷径，见到主语就触发）。最后：结论框 "The edit adds a bypass. The old path is still there."
口头补一句原因："An editor looks at one fact, not at the knowledge graph that fact sits in." 这句引出 delta graph。
**15. Every surgery: the exam passes, the inside tells another story**（90）四行表格，对应第 11 到 14 页。合并：两门技能考试都过，失对齐也一起带进来。Steering：对拒绝很干净，别的行为最多一半输入被推反。Removing（去毒和遗忘）：毒性 0.45 降到 0.21，脏话神经元还在，只是绕开了。Editing（我们的主题）：新事实通过，旧路径还在。点一下：考试只看答案，失败是没人看的内部变化。再点：结论框，我们需要比较改动前后的内部，把有风险的标出来。
说："Four surgeries, one pattern: the exam passes, and the inside tells another story."
**16. What is a delta graph?**（120，graph 4）只讲一个概念。同一组探针问题，编辑前问一遍，编辑后问一遍。节点是每层的 attention 块和 MLP 块。两个块在这些问题上一起升一起降，就连一条边（partial correlation）。左边编辑后的图，减去中间编辑前的图（6 层，含跨层连接），等于右边的 delta graph（论文定义 ΔA = A_post − A_pre）。after 图里已经标出变化：橙色变强，虚线变弱。
点一下：delta graph 出现。再点：一行流程，delta graph → 几个数 → 风险分 → 先查最可疑的（结果见下一页）。再点：结论框，delta graph 是这次编辑的指纹。
被问到"几个数"是什么：拓扑（总变化量、哪几层、集中程度）和谱（以编辑前的图为形状，把每个块的变化量做图傅里叶变换，看低频平滑还是高频尖锐）。论文 Table 5.2，新事实上 AUC：只用编辑器和模型 0.840，加拓扑 0.862，加谱 0.878，完整行为评测 0.984 但贵得多。
说："After minus before. What is left is the edit's fingerprint inside the model."
**17. Reading the delta graph: smooth or sharp**（90，graph 4）这一页讲谱分解，实现细节里唯一值得上台的一步，因为它是"图"的部分。四张卡片，点一下出前两张，再点出后两张：
1. 形状：编辑前的图（邻接取绝对值）的归一化 Laplacian，L = I − D^(−½)|A_before|D^(−½)。
2. 信号：每个块的变化量，c_i = Σ_j |ΔA_ij|（来自 delta graph）。
3. 图傅里叶变换：L = UΛUᵀ，ĉ = Uᵀc。特征向量是图上的"波"，特征值是频率。
4. 抽出的数：低、中、高频能量占比，谱熵，谱重心，Dirichlet 能量 cᵀLc。
再点：低频是变化沿原有连线平滑散开，高频是相连的块一个变一个不变，局部尖锐补丁。再点：论文 Table 5.2，在没用于拟合的新事实上，AUC 只用编辑器和模型 0.840，加 delta graph 数 0.862，加谱特征 0.878。
注意：基是编辑前的图，信号来自 delta。不是对 delta 本身做谱分解。
说："We read the change against the wiring before the edit. Smooth along the wiring, or a sharp local patch."
**18. Results: same checking budget, more bad edits caught**（120）小恶魔版。先讲清什么是坏编辑：考试全部满分，但换一批没用过的问法，成功率不到一半。页面第二行有例子（示意）：The Space Needle is in ___ 答 Paris ✓，但 Where would you go to see the Space Needle? 答 Seattle ✗。论文里 1,761 个满分编辑中 987 个是坏的（56%）。每排 20 个小恶魔就是查的 20 次，查到坏编辑的点亮，没查到的灰色。论文是 1,761 个满分编辑里 987 个坏的（56%），这里按 100 个来说。查最可疑的 20%，被查的里面坏的比例：随机 56%，按编辑器和模型 69.9%，按 delta graph 85.5%（Table 5.1），乘以 20 得 11.2、14.0、17.1。随机挑约 11 个，点一下，按编辑器和模型挑约 14 个（论文基线 model + editor prior：只看用了哪个编辑方法 ROME、MEMIT、WISE 和哪个模型 Qwen、Llama，不看内部），再点，按 delta graph 挑约 17 个（橙色）。再点：结论框 "Same 20 checks: 11, 14, 17. The extra catches come only from how the inside changed."
数字来自论文比率（被查的 20 个里坏的分别占 56%、70%、86%）。被问到排序质量：AUC 0.703 到 0.797，第二个数据集 0.853 到 0.904。十月版的卡片图在下箭头备用页。
**19. A missing path in the record means a worse answer, for every model**（150，第二层知识图，CIKM 2026）
右上角（替换了论文标题截图）是 QGC 的三步原理：问题 → 一个带类型的小图（最后一个节点是要找的答案）→ 能不能映射进病历（每个节点对应同类型的节点，每条边对应一条边，叫 typed homomorphism）。能，QGC = 1，可以基于证据回答。不能，QGC = 0，任何模型都给不出忠于病历的答案，只能靠记忆猜。生成之前就能检查，每个问题不到 0.1 毫秒。
说："A graph tells which questions cannot be answered faithfully, before any model tries. That is language."

### Part 2 音乐（16 到 27 页，约 22 分钟）

**20. Part 2. Hearing loss: a quiet epidemic**（90）第二部分的动机，数字慢慢说。四张卡片一张一张出：全球超过 15 亿人有听力损失，2050 年约 25 亿，每 4 人 1 个（WHO 2021）。听力损失轻度、中度、重度，痴呆风险约 2 倍、3 倍、5 倍（Lin 2011，639 人追踪约 12 年，重度组人很少）。听力损失约占全部痴呆病例的 7%，14 个可改变因素里并列最大（柳叶刀委员会 2024）。听力损失者抑郁几率高 47%（35 项研究，14.7 万老人，Lawrence 2020）。这些都是相关，不是因果。再点：希望，如实说，ACHIEVE（Lancet 2023）助听器让高风险老人 3 年认知下降慢 48%，但全体样本没有显著效果。最后：结论框。NIH 那条已移到第 22 页，这页只讲听力损失。 ×2、×3、×5 分开写，下面分别标 mild、moderate、severe。 11 月 19 日：去掉底部结论框。新加最后一步：可是很少人用，70 岁以上能从助听器受益的人里只有 30% 用过，20 到 69 岁约 16%（NIDCD，NHANES 2015 到 2020）。
**21. Music acts on the brain, and works as medicine**（90）原第 21、22 页合并，进度条第 2 步改名 Music on brain and body。上面一行：左边喇叭里飘出音符飞进大脑（颞叶闪动）。大脑里能测到的三件事（脑电跟拍 Nozaradan 2011，快感高峰多巴胺 Salimpoor 2011，40 Hz 声音减少小鼠淀粉样蛋白 Martorell 2019）。点一下：五张医学卡片（帕金森、手术、抑郁、痴呆、疼痛），如实说大多数试验规模小。再点：结论框，没人知道是音乐里的哪部分起作用，这是一个建模问题。原来两页在备用页。 11 月 19 日加数字：每张卡片写试验数和人数（帕金森 5 个试验 209 人，手术 73 个试验 Lancet 2015，抑郁 9 个试验 421 人，痴呆 11 个试验 503 人，疼痛 97 个试验 9,147 人，0 到 10 分疼痛低约 1 分）。手术来源换成 Hole 2015。再点：Gabby Giffords 的故事，2011 年头部中枪失去语言，音乐治疗里先唱出词（旋律语调疗法），再说出来。结论框移到第 3 步。 11 月 19 日：去掉结论框，Giffords 一栏展开：左脑语言区受损，唱歌走别的通路；治疗师先让她唱 Happy Birthday，再念，再说，旋律语调疗法是回到说话的一条绕道。“没人知道是音乐里哪部分起作用”改成口头说。

**22. How NIH came to fund music and health**（60）新页，进度条第 3 步 NIH builds the field。时间线四个点一个个出：1950 美国音乐治疗师成立全国协会（NAMT，现 AMTA），音乐治疗成为一门职业。2017 Sound Health 启动，NIH、肯尼迪中心和 NEA，起因是歌唱家 Renée Fleming 和 NIH 院长 Francis Collins（会弹吉他）相识，2017 年 1 月 NIH 研讨会开始（Fleming and Collins, JAMA 2017）。2019 第一批资助，5 年 2,000 万美元，10 个 NIH 研究所和中心出钱。2023 NCCIH 和 NIA 资助疼痛和痴呆方向的音乐干预研究网络，任务是统一测量、培养人、做小型预试验。再点：结论框，音乐很老，资助很新，这个领域缺方法，这正是计算能帮忙的地方。第 20 页底部 NIH 那条保持不变。 2017 卡片放大，配两人的照片（都是美国政府公版照片）：Renée Fleming，美国女高音，格莱美得主，2023 年肯尼迪中心荣誉奖；Francis Collins，2009 到 2021 年 NIH 院长，领导人类基因组计划，会弹吉他。各卡片上有机构标签：NAMT、NIH、Kennedy Center、NEA、NCCIH、NIA。 1950 卡片：1950 年 85 名会员，今天 10,699 名认证音乐治疗师（CBMT 2026）。2023 卡片：招标书第一年 150 万美元，3 个网络，每个预算的三分之一到一半必须用于预试验（RFA-AT-23-009）。 11 月 19 日：去掉结论框，卡片加细节。1950：两次世界大战后音乐家到退伍军人医院演奏，病人有反应，医院开始雇音乐家；1944 年密歇根州立大学开出第一个音乐治疗学位。2017：2015 年两人在一次晚宴上认识，Collins 带了吉他；2017 年 1 月第一次 NIH 研讨会。2019：项目举例，帕金森与运动、癌症压力与免疫、自闭症儿童的节奏与社交。2023：同年 NIH 发布音乐干预研究工具包（Neurology 2023），统一测量。 2017 卡片再加细节：两张照片并排，下面一条小时间线：2015 两人在晚宴上认识，他带了吉他；2017 年 1 月 NIH 研讨会，音乐治疗师和脑科学家一起盘点已知；2017 年 6 月在肯尼迪中心公开启动，有国家交响乐团音乐会；同月两人在 JAMA 写明缺什么：大型试验少，最大的几个大多没有定论，需要标准方法和生物标志物。2017 之前 NIH 和国家交响乐团已经有一个小的 Sound Health 项目（讲稿里说）。 2015 晚宴的细节：2015 年夏天华盛顿的一次晚宴，刚好在最高法院同性婚姻判决之后，在座有三位大法官（Scalia、Ginsburg、Kennedy）。气氛紧张时 Fleming 提议唱歌，Collins 带了吉他，两人唱了英国民谣 The Water Is Wide。Fleming 刚被任命为肯尼迪中心的特邀艺术顾问，问他科学对音乐知道多少。来源没说主人是谁，也没说是不是公开活动，台上只说 a dinner party。之后每一步都是两人一起推动：2017 年 1 月一起用 NIH 研讨会启动 Sound Health，6 月在肯尼迪中心两天的启动活动，同月一起在 JAMA 写评论，同一周还在 NPR 采访里合唱。 11 月 19 日再改：每条都压成一行。

**23. Music, hearing and health, a few miles from here**（30）不点名，只说哪里有什么、在做什么，不提全国。左边是示意地图：安大略湖在上，Genesee 河从南往北，市中心是 Eastman 音乐学院，沿河是 UR 和医学中心（URMC），城南是 RIT。右边：UR 有 Eastman Performing Arts Medicine（Eastman 和 URMC 合办的音乐与医学中心，2024 年起），音乐与老龄化的小额种子基金（和 UR Aging Institute），医学中心研究大脑如何响应音乐，电子与计算机工程系做音乐 AI。点一下：RIT 有工程技术学院（音乐和音频认知、助听器、空间音频），心理学系的认知科学（有博士项目），NTID（聋人认知和听力学）。再点：结论框，罗切斯特已经有了音乐、医学、听力和 AI，我们把它们连起来。说一句"如果你在做相关的事，来找我"就走。
**24. A new idea is a new edge, and so is a new style of music**（120）四本讲创造力的书和 Uzzi 2013：新想法就是旧想法之间的一条新边。下面是音乐流派家族树和我们 2017 年的 FusionGAN。 右侧 FusionGAN 卡片里 jazz、folk、fusion 旁边各有一个橙色播放按钮，播放论文发表时放在 SoundCloud 上的 demo（Jazz 和 Folk 是原始数据样本，Fusion 是 FusionGAN 生成的），再点一下暂停，翻页自动停。需要联网。
说："A new idea is a new edge. In 2017 we asked whether a model can draw one."

**25. A tiny graph is enough to represent a piece of music**（60）只放 demo，放大居中，没有别的。动画先边听 Für Elise 边画箭头（学习：数哪个音后面跟哪个音），再沿着箭头随机走（作曲）。点一下动画开声音，再点一下静音。这就是一阶 Markov 链，下一页用同一个模型做分类。
**26. Fold 88 keys into 12 scale degrees**（105，graph 3）手画的 Für Elise 开头九个音，折成 12 个音级，变成 12 乘 12 的表。两个播放键：原曲和从表里生成的曲子。
新动画（第 3 下）：12 × 12 矩阵的 12 行依次滑下去、首尾相接排成一条长条，就是 144 个数的向量，下面写 → logistic regression → which of 6 traditions?。第 4 下出现两个播放按钮。和第 25 页的区别：第 25 页的图用的是具体音高（带八度），每首曲子节点不同。这里折叠成 12 个音级，每首曲子都是同样的 144 个格子，才能放进同一个分类器。
说："The right notes with the wrong sentences. That is a graph with one note of memory."

**27. Occam's razor: the simplest graph already names the tradition**（105，进行中）六个曲库，一阶图分类准确率 70.2%，随机是 17%。
说："144 numbers name the corpus."

（原第 28 页生成实验已移到第 27 页下面的备用页。被问到生成效果时再按 ↓ 打开。）
**28. Steering leaves a style easily but rarely enters one**（105，graph 6，合作工作投稿中）去掉一个风格很容易，加进去却很难。
说："A vector cannot explain that. Reachability on a graph could."

**29. A note transition graph predicts the listening brain**（105，graph 7）Di Liberto 2020 原图：IDyOM 给每个音一个意外值，听众的脑电在 350 毫秒内跟着它走。 11 月 19 日：右侧文字收紧，最后一步在右下放 Für Elise 的静态 Markov 图做呼应，Remember this graph? IDyOM 是同一类图，记忆更长，背后的音乐更多。
说："The listening brain tracks a graph of note transitions. So the brain can judge a graph."

**30. Live: what MusicGen expects, next to what listeners' brains do**（135，进行中）现场 demo，全屏，可以直接点：选一首歌播放，乐谱、MusicGen 的意外值、脑电一起滚动。点过 demo 后方向键留在 demo 里，用右下角的 Next slide 按钮翻页。
Meyer 卡片多了一行：意外程度 = 一个音在前文之后出现的不可能程度，音符转移图能算它（IDyOM，上一页），这里用的是 MusicGen 自己的意外程度。然后问：大脑是不是在跟踪它？demo 嵌入时强制浅色（?theme=light），不随电脑深色模式变黑。
demo 用 view=talk 布局：上面是随时间变化的乐谱、模型意外程度、脑电曲线和此刻头皮图，下面只留两张分析卡：Average evidence（意外的音和预期的音之后的平均脑电）和 After this note（音后 0 到 0.3 秒的头皮图）。浅红色带是固定的 0.1 到 0.35 秒窗口，就是统计上意外效应出现的时间段。
说："This is the measurement we built. Note by note, it does not yet beat an untrained model, and the next slide is how we test it properly."演讲视图里小字收进每张卡右上角的 i 图标，点开看。上下两行卡片等高。After this note 卡片里两行的第三张图（+0.2 s）各有橙色框，是重点：下一行是 29 个听众、全部歌曲的回归估计，每多一个标准差的意外，头皮电位额外变化多少。+0.2 s 时前中部变红，意思是意外的音符让前中部头皮电位更正。这是头皮电压，不等于某个脑区“被激活”。

**31. The brain is read as a graph, too**（75，领域现状，不是我们的结果）两张图都是我们用公开数据和标准工具算出来的，不是手画：左边 EEG，PhysioNet 10 人静息，62 电极，alpha 波相位滞后指数最强的 4% 连边。右边 fMRI，nilearn 公开数据 10 人，MSDL 图谱 39 个脑区，偏相关最强的 8%。做法见 docs/brain-graphs.md。点一下，大家拿它做什么。EEG：医院脑电里找癫痫发作（图神经网络，AUROC 0.875，Tang ICLR 2022），读情绪（DGCNN 自己学边，SEED 上 90.4%），还有睡眠分期、脑机接口。fMRI：像指纹一样认人（126 人里认出 117 个，92.9%，同样的边还能预测流体智力 r = 0.50，Finn 2015），找疾病打在哪里（26 种脑疾病的损伤更常落在枢纽上，Crossley 2014），音乐（听最喜欢的歌时默认模式网络连接最强，Wilkins 2014）。再点：结论框，我们的 delta graph 用的是同一个配方，偏相关。 11 月 19 日重排：不用列表，一行一行字，每段不超过两行。顶部问题：一个音只有 0.2 到 0.4 秒，哪种工具跟得上？左 EEG（when）：每秒几百个采样，能看到每个音；安静、便宜、便携，人能正常听音乐。右 fMRI（where）：定位到毫米，但每 1 到 2 秒一张图，还滞后约 5 秒；扫描仪很吵，和音乐抢耳朵。各配一张图和两行建图方法。点一下，用途各两行：EEG 找癫痫（AUROC 0.875）、读情绪（SEED 90.4%）；fMRI 认人（126 人认出 117）、最喜欢的歌让默认模式网络连接更强。再点：做音乐、一个音一个音地看，大家偏爱 EEG，fMRI 适合整首歌。fMRI 图来自 Hong et al. 2013（Wikimedia Commons，CC BY-SA 3.0）。

（原第 32 页 Our plan 已移到备用页，11 月 19 日，内容太少。）

### 结尾（28 页，约 1.5 分钟）

**32. Look for the graph, in language and in music**（90）结尾，两栏各一句。语言：事实是三元组，互相支撑。编辑加了一条绕行，旧路径还在。我们的结果（橙色）：delta graph 查 20 个找到 17 个坏编辑（SDM 2026），QGC：缺一条路径，每个模型都更差（CIKM 2026）。点一下，音乐：乐理是一张图，模型学到了它的几何。我们的结果：144 个数的音符图认出风格，约 70%，听众的意外程度可以计算，大脑在跟踪它（live demo）。下一步：读出 MusicGen 内部的图。再点：结论框 Is there a graph inside your model?。底部是二维码和 zhiqian.ai/talks，讲完停在这一页答问。原来的点云版结尾在下箭头备用页。 11 月 19 日：左右各 3 条。语言：事实是三元组，编辑加了绕行旧路还在；delta graph（SDM 2026）；QGC（CIKM 2026）。音乐：乐理是图，模型学到它的几何；小小的音符图能认出风格，大脑跟踪它的意外（live demo），不标 our；我们的 FusionGAN，新风格是两种风格之间的新边（ICDM 2017）。去掉 Next 那条和结论框。底部二维码放大，右边 zhiqian.ai/talks，下面两行：Coming next: my keynote at AI4BioSig, IEEE BIBM 2026 / The Music That Plays the Brain，整组和二维码垂直居中 再改：不用橙色，我们发表的三条用浅灰色字，卡片去掉橙色顶条、缩矮。二维码右边两行（网址，加一行 Coming next: my keynote at AI4BioSig, IEEE BIBM 2026, The Music That Plays the Brain，不断行），和二维码上下居中。。