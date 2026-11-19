# 逐页讲稿和关键词（CS 系 colloquium，11 月 19 日）

每页一段约 100 词的英文讲稿，下面是这页会说到的关键词：英文、中文、一句话意思。发音提示写在方括号里。讲稿是口语版，可以照着说，也可以只看关键词。

---

## 1. Is There a Graph Inside Generative Models?

Left is a neural network, the picture everyone has seen. Right is the same network read as a graph: a few parts that matter and the links between them. That is the question of this talk. Is there such a graph inside a generative model, and what does it show that our usual tools miss? Short answer up front: for language, we have published answers. For music, we have a tested hypothesis and a live demo. Let me start with something everyone can answer.

- generative model 生成模型：能生成文字、图像、音乐的模型，比如 ChatGPT、MusicGen
- graph 图：节点加边，这里指"哪些部件之间有联系"

## 2. Level 1: a language model is itself a graph

Quick question for the room: the Space Needle is in the city of what? Seattle. Inside the model, layers light up one after another. An MLP block in layer 2 looks up the fact, an attention block in layer 4 moves it to the last word. The wiring is fixed, that is the structural graph. What lights up depends on the question, that is the functional graph. And the answer is a distribution over cities, with Seattle far ahead. Even when we ask for randomness, a chatbot asked for a number from 1 to 30 very often says 17.

- layer 层，attention block 注意力模块，MLP block 前馈模块（存知识的地方）
- structural / functional 结构的 / 功能的：线路本身 vs 某个问题实际用到的线路
- probability distribution 概率分布：每个候选答案一个概率
- residual stream 残差流：各层共用的那条"主干道"（被问到再说）

## 3. Change one fact, and the next question goes wrong

Two small knowledge graphs: Seattle, Washington, United States, dollar, and Paris, France, euro. Ask which city: Seattle. Which state: Washington. Which country, which currency: each question is one more hop. Now an attack. Knowledge editing exists because facts change and retraining is expensive, so we change a few weights instead. The same tool can write a false fact: the Space Needle is in Paris. The first answer becomes Paris, but the other three stay Washington, United States, dollar. A fact is a triple, and no triple stands alone.

- knowledge graph 知识图谱：事实连成的网
- triple 三元组：(subject 主语, predicate 关系, object 宾语)，如 (Space Needle, located in, Seattle)
- hop 跳：沿着一条边走一步
- knowledge editing 知识编辑：只改少量权重来改一个事实
- ROME, MEMIT：两种常用编辑方法 [ROME 读 "rome"，MEMIT 读 "mem-it"]
- ripple effect 连锁效应：相关事实应该跟着变却没变

## 4. One network, four graphs

The network itself can be drawn as a graph in more than one way: the weights, groups of neurons, the inputs, and which blocks fire together. Our focus is the circuit graph, the small subgraph of weights that carries one answer. So the question sharpens: does the circuit graph encode the knowledge graph? If the Space Needle is now in Paris, does the circuit know it is in France? When it does not, we call that a silent failure. Our work compares the circuit before and after an edit.

- circuit 电路 / 回路：模型里完成一个任务的那一小块子网络
- subgraph 子图
- silent failure 静默失败：考试通过了，但里面已经错了

## 5. Knowledge is not only text

Five people, five angles, one point. Merleau-Ponty, a philosopher: an organist learns a new organ in an hour, with the hands, not with words. Gardner, a psychologist: intelligence is plural, and music is its own kind. Picard: computers need to recognize and express emotion. Minsky: emotions are how the mind turns resources on and off. Fei-Fei Li: spatial intelligence goes beyond language. These are paraphrases, not quotes. Click: intelligence is more than words, and music is the kind that carries emotion.

- Merleau-Ponty [mer-LOH pon-TEE] 梅洛-庞蒂，法国哲学家
- multiple intelligences 多元智能（Gardner）
- affective computing 情感计算（Picard 创立）
- spatial intelligence 空间智能
- paraphrase 转述（不是原话）

## 6. A music generator is a language model, with a pitch graph inside

For a CS audience, one idea: MusicGen is a language model. EnCodec, a neural audio codec, turns every 20 milliseconds of sound into 4 integers, so a song becomes a sequence of tokens, like words. A transformer predicts the next token. Music theory has a graph for pitch: seven notes in a row, and every note linked to the same note one octave up. Yagi and colleagues fed single notes into music models and found the internal states form a helix, one turn per octave. The model was never told about octaves.

- pitch 音高：声音的高低
- note 音符 / 音：C D E F G A B（do re mi fa sol la si）
- octave 八度：同名的高一组音，频率正好翻倍，C4 到 C5
- C3, C4, C5：字母是音名，数字是第几个八度，C4 是钢琴中央 C
- token 词元，codec 编解码器
- helix 螺旋：转一圈 = 一个八度
- activation 激活值：模型内部的数字向量

## 7. Do music generation models encode music theory?

Left is the Tonnetz, a lattice going back to Euler in 1739. Across is a fifth, seven half steps, C to G. Up right is a major third, four half steps, C to E. Every small triangle is a chord: pointing up is major, pointing down is minor. Neighbors share two notes, so you move by changing one note: P, R and L. Right: a word2vec model trained on chord sequences places the 24 chords on a ring in circle of fifths order, zero ordering errors. A key is one connected region on both sides.

- Tonnetz [TONE-nets] 音网，德语"音的网"
- half step / semitone 半音：钢琴上相邻两个键
- fifth 五度（7 个半音），major third 大三度（4 个半音），minor third 小三度（3 个半音）
- chord 和弦，triad 三和弦（三个音）
- major / minor chord 大三和弦 / 小三和弦：听起来亮 / 暗
- Cm, Am：m 表示小和弦，B♭ 是降 B，F♯ 是升 F
- P, R, L：Parallel, Relative, Leading-tone，三种"只动一个音"的变换
- neo-Riemannian [REE-mahn] 新黎曼理论，来自音乐理论家 Hugo Riemann，不是数学家
- key 调：比如 C 大调，circle of fifths 五度圈
- word2vec：把词（这里是和弦）变成向量的模型
- ii-V（"two-five"）：二级和弦到五级和弦，最常见的和弦进行

## 8. Two levels, two domains: the map of this talk

The whole talk on one slide. Two levels of graph: level 1 is the model itself, level 2 is the knowledge it stores. Two domains: language and music. In language, Part 1, the delta graph shows how an edit rewires the model, and the knowledge graph links facts to facts. In music, Part 2, a note graph says which note follows which, and the open question is whether there is a graph inside MusicGen. Language has answers. Music is where the open questions are.

- level 1 / level 2 第一层 / 第二层：模型内部的图 / 模型存的知识的图
- domain 领域
- delta graph 差分图：编辑前后模型内部连接的变化

## 9. A released model is not left alone. Seven kinds of surgery.

Once a model is released, people keep operating on it. Edited: rewrite one wrong fact. Stitched: the bottom of one model with the top of another. Merged: average two models into one. Pruned: delete parts and see what breaks. Steered: push the internal state while it runs. Unlearned: make it forget, or only hide. And fine tuned, the most common surgery of all. Every one of these is accepted by an exam that only looks at answers, and every one, written down, is something added to the model.

- fine-tuning 微调，pruning 剪枝，merging 模型合并
- steering 引导：运行时往内部状态上加一个方向
- unlearning 遗忘：让模型"忘掉"某些内容
- stitching 拼接：一个模型的下半截接另一个的上半截

## 10. Today we change and explain models with vectors

Four ways we change a model, each drawn as what it adds: a steering vector, a rank one matrix, LoRA, and fine tuning as a full matrix of small changes. All the same kind of object. Below, every dot is something the model knows. An edit moves one fact, Seattle to Paris. That arrow is the vector we added. The ripple effect: related facts should move, France and euro, and they do not. Locality: unrelated facts should stay, and some drift. A vector says what we changed. Only a graph can say where it went.

- vector 向量，rank one matrix 秩一矩阵（u 乘 v 转置）
- LoRA [LOR-ah] 低秩适配：用两个瘦长矩阵相乘做微调
- locality 局部性：不相关的事实应该不动
- linear probe 线性探针，sparse autoencoder 稀疏自编码器（解释模型常用的工具）

## 11. Merging: add two fine tunes and get both skills

This only works for fine tunes of the same base model. A fine tune can be treated as an arrow: the fine tuned weights minus the base weights. Add two arrows and the model has both skills with no retraining. Subtract one and a skill fades. The open model community merges this way all the time. The catch: merge an aligned chemistry expert with a math expert that lost its safety training. The merge passes both exams and now explains how to make a poison. The exams never asked.

- task vector 任务向量：微调后权重减去原始权重
- base model 基础模型
- aligned 对齐的：经过安全训练、会拒绝有害请求
- TIES：一种减少合并冲突的方法（被问到再说）

## 12. Steering: clean for some behaviors, unreliable for others

Steering adds a direction to the activations at one layer while the model runs, nothing is retrained. The clean case: the refusal direction is the average activation on harmful prompts minus harmless ones. Remove it and the model almost never refuses. The general case: Tan and colleagues built one vector per behavior, for 40 behaviors, and checked input by input. For some behaviors almost no input goes the wrong way. For others close to half do, a coin flip. A vector works when the behavior is one clean direction.

- refusal direction 拒绝方向：模型"拒绝回答"对应的那个方向
- activation 激活，behavior 行为
- steerability 可引导性
- coin flip 抛硬币：一半对一半错

## 13. Removing a behavior: hidden, not deleted

The model is GPT-2 medium. First, find the toxic neurons: a probe gives a toxic direction, and the MLP neurons closest to it write swear words. Toxicity 0.45. Second, train with DPO to prefer polite text. Toxicity drops to 0.21, but those neurons barely change. An earlier layer shifts the input so it no longer triggers them, a detour. Third, multiply the keys of seven toxic neurons by ten, no training. Toxicity is back to 0.46. Unlearning shows the same: a little fine tuning brings forgotten facts back.

- toxicity 毒性：脏话、攻击性内容的比例
- probe 探针：一个小分类器，读出某个概念的方向
- DPO 直接偏好优化：一种对齐训练方法
- key / value 键 / 值：MLP 神经元的"什么时候触发"和"触发后写什么"
- detour 绕道

## 14. Knowledge editing bypasses the old fact instead of removing it

This is the main point, say it slowly. The gray line is the old path from training. The edit does not touch it. It adds a shortcut at one layer. The test prompt goes through the shortcut: Paris, the exam passes. Ask a little differently, mention Seattle first, and the old path lights up again. This is measured: crafted prompts recover the original answers. And the shortcut fires too often: after editing Microsoft's founder to Steve Jobs, ask which college the founder of Microsoft attended, and the model answers Steve Jobs 41 percent of the time.

- bypass 旁路 / 绕行，shortcut 捷径
- old path 旧路径：训练时学到的那条
- crafted prompt 精心构造的提示词

## 15. Every surgery: the exam passes, the inside tells another story

One table, the last four slides in one place. Merging: both exams pass, and the misalignment came along. Steering: clean for refusal, but for other behaviors up to half the inputs go the wrong way. Removing a behavior: toxicity drops from 0.45 to 0.21, and the swear neurons are still there behind a detour. Editing, our topic: the new fact passes, and the old path is still there. The exam reads answers. The failure is a change inside that nobody looked at. We need to compare the inside before and after.

- misalignment 失对齐：安全性丢了
- exam 考试：这里指只看答案的评测

## 16. What is a delta graph?

We ask the model the same probe questions before and after the edit. A node is a block: the attention or MLP block of one layer. For each question we record how active each block is. Two blocks get an edge when they rise and fall together across questions, after removing what the other blocks explain. That is a partial correlation. One graph before, one after. Subtract: after minus before is the delta graph. A few numbers from it go into a small logistic model that gives each edit a risk score.

- partial correlation 偏相关：去掉其他变量影响后，两者还剩多少相关
- delta 差值（Δ）
- logistic regression 逻辑回归：输出一个 0 到 1 的风险分
- risk score 风险分

## 17. Reading the delta graph: smooth or sharp

The graph part, in four steps. The shape: the graph before the edit, and its Laplacian. The signal: for each block, how much its connections changed. The graph Fourier transform: the Laplacian's eigenvectors are like waves on the graph, slow and fast, and we project the signal onto them. The numbers we keep: energy in low, middle and high bands, spectral entropy, and Dirichlet energy. Low frequency means the change spreads along the wiring, high means a sharp local patch. On held out facts, AUC goes from 0.840 to 0.878.

- Laplacian [la-PLAH-see-an] 拉普拉斯矩阵
- eigenvector 特征向量，eigenvalue 特征值（这里就是"频率"）
- graph Fourier transform 图傅里叶变换 [FOR-ee-ay]
- spectral 谱的，spectral entropy 谱熵
- Dirichlet energy [dee-ree-KLAY] 狄利克雷能量：相连节点差别有多大
- AUC：排序好坏的指标，0.5 是瞎猜，1 是完美
- held out 留出的：没用来训练的数据

## 18. Results: same checking budget, more bad edits caught

A bad edit passes every exam question, but on new wordings it succeeds less than half the time. Out of 100 edits, 56 are bad, and we can afford to check only 20. Pick at random and about 11 of your 20 are bad. Rank by which editor and which model, and you get about 14. Rank by the delta graph, about 17. Same 20 checks, and the extra catches come only from how the inside changed. Published at SDM 2026.

- checking budget 检查预算：能人工检查的数量
- base rate 基础比例：随机抽中的比例
- prior 先验：只看用了哪个编辑方法、哪个模型
- SDM：SIAM 数据挖掘会议

## 19. A missing path in the record means a worse answer, for every model

Our CIKM 2026 paper. A question becomes a small graph with types, for example patient, admitted, admission, allergy. QGC asks whether this small graph maps into the patient record, every node to a node of the same type, every edge to an edge. If not, no model, however large, can answer faithfully from the record. On MIMIC-III, every one of five models is more accurate when the path exists, by 20 to 30 points. And a third of the questions have no path at all.

- QGC：我们的指标，问题图能不能嵌进记录图
- typed homomorphism 保类型同态：节点对节点、类型相同、边对边
- MIMIC-III：公开的重症监护病历数据库
- faithful 有据可依的：答案来自记录，不是来自记忆
- CIKM：信息与知识管理会议

## 20. Part 2. Hearing loss: a quiet epidemic

Part 2 starts with health. More than 1.5 billion people live with hearing loss, and WHO projects 2.5 billion by 2050, one in four. It is tied to dementia: mild hearing loss about twice the risk, moderate three times, severe five times. It is about 7 percent of all dementia, the largest risk we can change. And 47 percent higher odds of depression. These are associations, not proof of cause. Hearing aids can help some people. Yet fewer than one in three adults over 70 who could benefit has ever used one.

- hearing loss 听力损失，dementia 痴呆，depression 抑郁
- risk factor 风险因素，modifiable 可改变的
- association 相关（不等于因果 causation）
- hearing aid 助听器
- mild / moderate / severe 轻度 / 中度 / 重度

## 21. Music acts on the brain, and works as medicine

Music acts on the brain in ways we can measure. In EEG, the brain rhythm locks to the beat. In PET, dopamine is released at the peak of pleasure. And 40 hertz sound reduced amyloid in mouse brains. In clinical trials, music already works as medicine: Parkinson's, surgery, depression, dementia, pain. Pain alone has 97 trials and about one point less pain on a ten point scale. Most trials are small. And one story: Gabby Giffords lost her speech after being shot, and sang words before she could say them again.

- EEG 脑电图，PET 正电子发射断层扫描
- dopamine 多巴胺：和愉悦、奖励有关的神经递质
- amyloid 淀粉样蛋白：和阿尔茨海默病有关
- 40 Hz：每秒 40 次的声音节律
- clinical trial 临床试验，meta-analysis 荟萃分析（把很多试验合起来看）
- aphasia 失语症，melodic intonation therapy 旋律语调疗法

## 22. How NIH came to fund music and health

Four dates. 1950: music therapy becomes a profession in the US, with 85 members. Today there are more than ten thousand certified music therapists. 2017: Sound Health starts. It began in 2015 at a dinner in Washington, where the soprano Renée Fleming met NIH director Francis Collins, who had brought his guitar. 2019: the first research awards, 20 million dollars over five years. 2023: research networks for pain and dementia, to build shared methods. The music is old, the funding is new, and the methods are still being built.

- music therapy 音乐治疗，board certified 获得认证的
- soprano 女高音，Renée Fleming [ruh-NAY FLEM-ing]
- NIH 美国国立卫生研究院，Kennedy Center 肯尼迪表演艺术中心，NEA 美国国家艺术基金会
- NCCIH 国家补充与整合健康中心，NIA 国家老龄化研究所
- pilot study 预试验：小规模先试

## 23. Music, hearing and health, a few miles from here

Thirty seconds, just to share. Downtown is the Eastman School of Music. Along the river, the University of Rochester and its Medical Center, with a center for music and medicine, pilot awards for music and aging, and work on music and AI. South of the city, RIT: music and audio cognition, hearing aids, cognitive science, and NTID with deaf cognition and audiology. Rochester already has music, medicine, hearing and AI. If you work on any of this, talk to me.

- Eastman School of Music 伊士曼音乐学院
- URMC 罗切斯特大学医学中心
- NTID 国家聋人技术学院（RIT 的一部分）
- audiology 听力学，cognition 认知

## 24. A new idea is a new edge, and so is a new style of music

Four books on creativity over seventy years, and a study of millions of papers, say one thing: a new idea is a new combination of old ones, a new edge, A plus B. Music has a family tree too. Jazz came from blues, ragtime and brass bands. Rock and roll from rhythm and blues and country. Jazz plus rock gave fusion. In 2017 we asked if a model can draw such an edge. FusionGAN learns from jazz and folk melodies and generates a style in between. Listen to the three clips.

- creativity 创造力，combination 组合
- genre / style 风格，fusion 融合（爵士摇滚融合）
- blues 布鲁斯，ragtime 拉格泰姆，folk 民谣，bossa nova 巴萨诺瓦
- GAN 生成对抗网络：一个生成器，一个判别器，互相较劲
- ICDM：数据挖掘国际会议

## 25. A tiny graph is enough to represent a piece of music

This is Für Elise by Beethoven. Each circle is a note. Watch the ball: as the melody plays, every move from one note to the next draws an arrow. That is a Markov chain graph, which note follows which, and how often. Then the graph composes on its own, walking the arrows by their probabilities. It is not a toy. The same kind of graph, 144 numbers per piece, names the tradition of a piece it has never seen about 70 percent of the time.

- Für Elise [fyoor ay-LEE-zuh] 《致爱丽丝》
- Markov chain 马尔可夫链：下一个状态只看当前状态
- transition 转移，transition probability 转移概率
- melody 旋律，compose 作曲
- tradition 传统 / 曲库来源（比如巴赫众赞歌、民歌）

## 26. Fold 88 keys into 12 scale degrees, and a melody becomes 144 numbers

A piano has 88 keys, but the same 12 notes repeat in every octave. And a melody in C and the same melody in G should look the same. So we fold octaves together and count from the home note of the key. That gives 12 scale degrees, and a 12 by 12 table: each row says where the melody goes next from that note. Laid end to end, 144 numbers. Play the second clip: it uses only these numbers, and sounds like the right notes in the wrong sentences.

- scale degree 音级：一个音在调里排第几，1 是主音
- tonic / home note 主音：一首曲子的"家"
- transpose 移调：整体升高或降低，旋律不变
- 12 × 12 matrix 12 乘 12 矩阵，flatten 展平

## 27. Occam's razor: the simplest graph already names the tradition

992 melodies from six public corpora, Bach chorales, Essen folk songs, Monteverdi, Palestrina, a collection of fiddle tunes, and Trecento music. Six styles, so chance is 17 percent. Counting only which notes appear, with no order, gives 41.9 percent. The note transition graph, 144 numbers and a plain logistic regression, gives about 70 percent. The order of notes adds almost 30 points. No tuning, the script is public. Occam's razor: the simplest graph already carries the style.

- Occam's razor 奥卡姆剃刀：能简单就别复杂
- corpus / corpora 语料库（复数）
- chorale 众赞歌，Trecento 14 世纪意大利音乐
- chance level 随机水平
- classifier 分类器

## 28. A note transition graph predicts the listening brain

IDyOM is a note transition graph with several memory lengths. It gives every note a surprise value: how unexpected is this note, given the ones before. Di Liberto and colleagues played Bach to 20 people wearing EEG. The sound alone predicts part of the brain response. Adding the surprise predicts more, within 350 milliseconds of each note, in 16 of 20 listeners. Remember the Für Elise graph? IDyOM is the same kind of graph, with a longer memory. The listening brain tracks a graph of note transitions.

- IDyOM [ID-ee-om]：音乐预期模型，变长 Markov 模型
- surprise 意外值（信息论里的 −log 概率）
- expectation 预期
- millisecond 毫秒（ms）

## 29. Live demo: what MusicGen expects, next to what listeners' brains do

Leonard Meyer, a music theorist, said in 1956 that emotion in music comes from expectation, held back or broken. So does the listening brain track how surprising each note is? Here the surprise comes from MusicGen-large, the same test as IDyOM on the last slide. Pick a song and press play: the score, the model's surprise for every note, and the listeners' average EEG scroll together. Jump to a surprising note and watch the EEG. Below, across 29 listeners, the front center of the scalp turns more positive about 0.2 seconds after a surprising note.

- Leonard Meyer 伦纳德·迈尔，音乐理论家
- score 乐谱，scalp potential 头皮电位
- 0.2 s 后前中部变红 = 头皮电压更正，不等于某个脑区"被激活"
- control / random model 对照 / 没学过音乐的随机模型
- in progress 进行中，不是结论

## 30. The brain is read as a graph, too

A note lasts 0.2 to 0.4 seconds. Which tool keeps up? EEG samples every few milliseconds and is quiet, so it sees every note, but where is blurry. fMRI sees where to a few millimeters, but takes one image every one to two seconds, lags about five seconds, and the scanner is loud. Both are read as graphs. For EEG, a node per electrode, an edge where signals stay in step. For fMRI, a node per brain region. People use them to find seizures, read emotion, and tell people apart. For music, note by note, people prefer EEG.

- fMRI 功能磁共振成像：看血氧变化
- temporal resolution 时间分辨率，spatial resolution 空间分辨率
- electrode 电极，brain region 脑区，atlas 脑图谱
- phase locking 相位锁定：两路信号节奏保持一致
- seizure 癫痫发作，default mode network 默认模式网络（发呆时最活跃的脑区网络）
- connectome 连接组：整个大脑的连接图

## 31. Look for the graph, in language and in music

To close. In language: facts are triples, and an edit adds a bypass while the old path stays. Our delta graph finds 17 bad edits in 20 checks, SDM 2026. And QGC shows a missing path means a worse answer for every model, CIKM 2026. In music: music theory is a graph, and models learn its geometry. A small note graph names the style, and the brain tracks its surprise. And our FusionGAN made a new style as a new edge, ICDM 2017. Coming next: my keynote at AI4BioSig, The Music That Plays the Brain. Thank you.

- geometry 几何结构
- keynote 主题报告
- AI4BioSig：IEEE BIBM 2026 的 AI for Bio Signals workshop
- 结束后停在这页答问，二维码打开这套幻灯片
