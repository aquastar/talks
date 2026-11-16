# 音乐与大脑：系统调研

Nov 12, 2026 · @Zhiqian Chen

## 导读

**一句话结论**：音乐对大脑的作用在机制层面证据扎实（奖赏、预期、专门化皮层、记忆保留），在临床层面普遍只有短期、低到中等确定性的效果，而连接两者的计算层（用深度模型解释和预测脑响应）在 2023 年后才真正起步，这正是 CS 背景的人最有空间的地方。

**组织方式**：按"刺激 → 测量 → 模型 → 应用"排列。第 1 块讲大脑怎么处理音乐，第 2 块讲用什么看到，第 3、4 块讲怎样把音乐和脑信号对上，第 5 块是可用数据，第 6 块是临床证据，第 7 块是缺口和 keynote 骨架。

**证据标注约定**

| 标记 | 机制研究的含义 | 临床研究的含义 |
| --- | --- | --- |
| A | 多实验室、多方法反复复现 | Cochrane 或大型 Meta，GRADE 中等及以上 |
| B | 有高质量原始研究，复现有限 | GRADE 低，或结论存在方法学争议 |
| C | 单个研究、小样本或仍在争论 | GRADE 极低，或只有叙述性综述 |

标注"未本次核验"的条目来自我对经典文献的已有了解，本次没有重新打开原文，引用前请自己核对。

**对你最关键的三个发现**

1. 用生成模型解释脑响应已有两篇顶刊锚点：Brain2Music 于 2025 年底正式发表于 Nature Communications，Mesgarani 组 2025 年用生成式 music transformer 的层级表示预测 EEG 和 iEEG。你的切入点不是空白，但"打开模型内部机制"这一层仍然空着。
2. 临床证据的普遍短板是短期、无盲法、干预描述模糊。可解释的生成模型恰好能提供可控、可复现、可参数化的刺激，这是一个从方法学角度切入临床的角度。
3. 音乐选择性皮层的关键作者 Norman-Haignere 现在在 University of Rochester Medical Center，就在你本地。

## 1. 神经基础：大脑怎么处理音乐

音乐处理不是一个"音乐中枢"，而是一条从听觉皮层出发、分叉到运动、奖赏和记忆系统的通路。下表按通路上的环节排列，每行给最有代表性的证据。

| 环节 | 核心结论 | 代表工作 | 证据 |
| --- | --- | --- | --- |
| 专门化听觉皮层 | 非初级听觉皮层存在对音乐高度选择、且无法用声学特征解释的神经群体，与语音选择区在解剖上分开 | [Norman-Haignere 2015, Neuron](https://neurosciencenews.com/auditory-processing-music-neuroscience-3285/)：165 种自然声音，fMRI 体素分解得到 6 个成分 | A |
| 歌声子群体 | 音乐表征进一步分化，存在几乎只对带人声的音乐响应的成分，ECoG 单电极也可见 | [Norman-Haignere 2022, Curr Biol](https://cbmm.mit.edu/publications/neural-population-selective-song-human-auditory-cortex) | B |
| 半球分工 | 音乐偏右半球、语音偏左，iEEG 中右侧 STG 对音乐响应电极比例更高 | [Bellier 2023, PLOS Biol](https://www.nih.gov/news-events/nih-research-matters/scientists-translate-brain-activity-into-music)；Zatorre 频谱与时间分工假说（未本次核验） | A |
| 节奏与运动耦合 | 听节拍会激活基底节和辅助运动区，即使人不动 | Grahn & Brett 2007（未本次核验） | A |
| 预期与意外 | 皮层响应随旋律"意外程度"连续变化，可在自然聆听中用 EEG 测到 | [Di Liberto 2020, eLife](https://elifesciences.org/articles/51784)，见第 3 块 | A |
| 奖赏与多巴胺 | 强烈愉悦时纹状体释放多巴胺：尾状核对应"期待"，伏隔核对应"高潮时刻" | [Salimpoor 2011, Nat Neurosci](https://brams.org/2011/01/09/salimpoor/)，PET 加 fMRI | A |
| 奖赏价值 | 第一次听新歌时，伏隔核与听觉皮层的连接强度能预测人愿意花多少钱买这首歌 | [Salimpoor 2013, Science](https://www.zlab.mcgill.ca/publications/docs/Science-2013-Salimpoor-216-9.pdf) | B |
| 长期音乐记忆 | 长期熟悉的音乐由尾侧前扣带和腹侧 pre-SMA 编码，这些区域在 AD 中萎缩和代谢下降最少 | [Jacobsen 2015, Brain](https://neurosciencenews.com/musical-memory-alzheimers-2144/)：7T fMRI，32 名健康人加 20 名 AD 患者 | B |
| 训练可塑性 | 音乐家的听觉脑干编码（FFR）更精确，但"学音乐让孩子更聪明"的远迁移在高质量设计下趋近于零 | Kraus 组 FFR 系列（未本次核验）；[Sala & Gobet 2020](https://pmc.ncbi.nlm.nih.gov/articles/PMC7683441) | 近迁移 B，远迁移 A（阴性） |

**三点值得你记住的细节**

1. **奖赏的时间结构**：Salimpoor 的关键是把 PET 的化学特异性和 fMRI 的时间分辨率结合，证明期待和兑现由不同通路完成。这对生成模型有直接意义：如果能控制"期待在哪里建立、在哪里兑现"，就可能调控奖赏响应。
2. **AD 记忆保留的机制只是部分解释**：Jacobsen 发现这些区域萎缩和代谢下降少，但淀粉样蛋白沉积并不比其他区域少，作者解释为病程较晚到达。这意味着"音乐记忆永远保留"是过度简化。
3. **远迁移是个被高估的说法**：Sala & Gobet 发现研究设计越严格，效应越小，加入主动对照后效应接近零。有反驳者重新分析得到小的正效应（g 约 0.23）。在 keynote 里提到音乐训练的认知收益时要谨慎。

## 2. 测量手段：用什么看到反应

音乐是毫秒级变化的信号，而 fMRI 的血氧响应要几秒才出现，所以手段的选择决定了你能问什么问题。经验法则：问"哪里"用 fMRI，问"什么时候、跟着哪个音符"用 EEG 或 MEG，两者都要就只能靠 iEEG 患者数据。

| 手段 | 时间分辨率 | 空间分辨率 | 音乐研究中的典型用途 | 主要局限 |
| --- | --- | --- | --- | --- |
| EEG | 毫秒 | 厘米级，源定位不可靠 | 节拍同步、旋律预期、情绪、听觉辨别 | 信噪比低，跨被试差异大 |
| MEG | 毫秒 | 比 EEG 好 | 预期模型比较，如 Kern 2022 | 设备稀少，成本高 |
| fMRI | 秒级 | 毫米级 | 功能分区、encoding 模型、解码重建 | 扫描噪声干扰聆听，时间分辨率不适合音符级分析 |
| PET | 分钟级 | 毫米级 | 神经化学，如多巴胺释放 | 放射性，实验次数受限 |
| iEEG / ECoG | 毫秒 | 毫米级 | 高保真重建与精细定位 | 只能用癫痫手术患者，电极覆盖由临床决定 |

**EEG 里的几类音乐信号**（BIBM 听众最熟悉，你需要能说清楚它们的区别）

1. **ERP 成分**：失匹配负波（MMN）反映对偏离规则的自动检测，ERAN 反映和声违例，P3 反映注意性意外。传统范式靠重复短刺激叠加平均。
2. **神经同步（entrainment）**：皮层振荡相位跟随节拍，在节拍频率及其谐波上出现频谱峰，Nozaradan 等人的稳态诱发范式是代表（未本次核验）。
3. **频率跟随响应（FFR）**：脑干对声音周期的锁相响应，可以直接看出音高编码精度，常用于比较音乐家和听力损失人群（未本次核验）。
4. **连续聆听下的 TRF**：不再叠加重复刺激，而是用回归把整段自然音乐的特征映射到连续 EEG。这是从"实验室刺激"走向"真实音乐"的关键转变，第 3 块展开。

**一个判断**：你的主战场应该是 EEG 加 TRF。理由有三：它与 BIBM 生物信号主题最贴合，成本低到可以自己采数据，而且时间分辨率能对上生成模型逐 token 的表示。fMRI 适合作为第二验证源，借用公开数据即可。

## 3. 编码与解码：把音乐和脑信号对上

这一块是 keynote 的主体。核心方法只有两个方向：**encoding** 用音乐特征预测脑信号（问"大脑编码了什么"），**decoding** 用脑信号反推音乐（问"能读出多少"）。打个比方，encoding 像用乐谱预测指挥的手势，decoding 像看指挥的手势猜乐谱。

**3.1 Encoding：从声学到预期**

标准工具是时间响应函数（TRF），本质是带时滞的岭回归。判断某个特征是否"被大脑编码"的方法是看加入它之后预测准确率是否在声学基线之上显著提升。

| 工作 | 数据 | 关键发现 | 证据 |
| --- | --- | --- | --- |
| [Di Liberto 2020, eLife](https://elifesciences.org/articles/51784) | EEG 20 人约 75 分钟，ECoG 3 人各约 25 分钟，巴赫单声部钢琴 | 用变阶马尔可夫模型 IDyOM 计算的音高与起始时间意外度，在声学基线之上额外解释 EEG，效应集中在 350 毫秒内的颞平面和 Heschl 回 | A |
| [Kern 2022, eLife](https://elifesciences.org/articles/80935.pdf) | 复用上述 EEG，新采 MEG 35 人 | 比较 Gestalt 模型、IDyOM 和 Music Transformer 三种预期模型，结论是皮层反映基于长期经验的短程预测 | B |
| [Mischler 2025, Nat Commun](https://ideas.repec.org/a/nat/natcom/v16y2025i1d10.1038_s41467-025-63961-7.html) | 音乐家与非音乐家 EEG，6 名患者 iEEG，古典钢琴 | 用生成式 music transformer 的层级表示预测脑活动，离初级听觉皮层越远的位点编码越长的音乐上下文 | B |

**和你的工作最近的一点**：Di Liberto 用的 IDyOM 本质上就是一个马尔可夫转移模型，和你的 Markov graph 分析是同一家族。区别是他们只把它当"意外度计算器"，没有分析转移结构本身。

**3.2 Decoding：从脑信号重建音乐**

| 工作 | 手段 | 方法 | 结果与局限 | 证据 |
| --- | --- | --- | --- | --- |
| [Bellier 2023, PLOS Biol](https://escholarship.org/uc/item/4ms6t5cv) | iEEG，29 名患者，2,668 个电极 | 非线性回归重建频谱图，再合成音频 | 重建出可辨认的 Pink Floyd 片段。347 个显著电极，右 STG 贡献最大，发现一个对节奏调谐的 STG 子区。歌词基本听不清 | B |
| [Denk 2025, Nat Commun](https://arxiv.org/abs/2307.11078v1)（Brain2Music） | fMRI，5 人，540 段 GTZAN 音乐 | fMRI 线性映射到 128 维 MuLan 嵌入，再用 MusicLM 生成或检索 | 重建在流派、乐器、情绪层面相似，旋律和节奏不对齐。MusicLM 特征对初级听觉皮层的预测优于非音乐模型 | B |
| [CLAP 解码，2024 arXiv](https://arxiv.org/pdf/2406.15537) | 同一 fMRI 数据集 | 映射到 CLAP 嵌入做检索 | 报告了更高的识别准确率，属于检索而非生成 | C |

**关键的方法学提醒**：Brain2Music 一类工作的"重建"大部分质量来自生成模型本身的先验，fMRI 只提供了粗粒度的语义方向。BIBM 听众里会有人追问这一点，你需要能区分"大脑里读出了什么"和"生成模型补全了什么"。

**3.3 音乐想象**：解码"脑中想的音乐"而不是"耳朵听到的音乐"，OpenMIIR 数据集专为此设计（见第 5 块）。早期结果是部分被试的想象可以在二分类中区分，整体仍属探索阶段，证据 C。

**3.4 跨被试泛化**：几乎所有重建工作都按被试单独训练。Brain2Music 只有 5 名被试。跨被试共享表示是视觉解码领域近两年的热点，音乐领域基本空白。

## 4. 深度模型与大脑对齐：模型表示像不像大脑

这条线的逻辑来自视觉领域（Yamins 2014）和听觉领域（Kell 2018，未本次核验）：任务训练得好的深度网络，其层级表示会自然对齐到感觉皮层的层级。音乐上这条线近两年快速成形，但几乎所有工作都把模型当黑箱特征提取器。

**已经确立的三个结论**

1. **好模型更像大脑**：[Pepino 2025](https://arxiv.org/abs/2511.16849v1) 比较 36 个音频模型和两个 fMRI 数据集，下游任务综合表现与脑对齐度的相关超过 0.7，而且这种相似性在 EnCodecMAE 预训练早期就出现，并非刻意优化的结果。证据 B。
2. **音乐专用模型在初级听觉皮层更准**：[Denk 2025](https://acousticslab.org/RECA293/293Files/293Downloads/DenkEtAl2025_TextToMusic.pdf) 显示 MusicLM 的特征对初级听觉皮层的预测优于非音乐专用模型，而且只看文字描述得到的特征和音乐本身的特征可以预测大体重叠的体素。证据 B。
3. **模型层级对应皮层层级**：Mischler 2025 显示生成式 transformer 越深层的长上下文表示，越对应远离初级听觉皮层的位点。但 Denk 也指出，听觉皮层里低层与高层表示的分化不如视觉皮层明显。证据 B。

**仍然空着的地方**（你的机会集中在这里）

| 空白 | 为什么重要 | 你已有的资产 |
| --- | --- | --- |
| 只看相关，不做干预 | 现有工作全是"模型某层和脑区相关"，没人改动模型内部再看脑对齐是否变化 | MusicGen steering，Styles Are Islands 中的增删不对称 |
| 没有结构层的解释 | 只比较向量，不问模型内部是否有对应旋律转移或和声进行的结构 | Markov graph 分析，SDM26 的 delta graph 方法 |
| 声学基线控制不一 | 很多"深度特征胜出"可能只是吸收了更多声学信息 | 你计划中的 brain alignment scorer 正是"超出声学基线"的设计 |
| 只用健康年轻人 | 对齐度在老年、听力损失、人工耳蜗用户中是否改变，基本没人测 | 听力和 ADRD 方向的合作网络 |

**一个需要警惕的反方观点**：对齐度高不等于机制相同。两个系统都学到"音高很重要"就会相关，这不说明模型像大脑那样计算。在 keynote 里把对齐当作"筛选工具"而不是"机制证据"会更稳妥。

## 5. 数据集与基准

公开音乐脑数据的共同问题是被试少、刺激少、多数不附原始音频。按与你方向的契合度排序：

| 数据集 | 手段 | 规模 | 刺激 | 许可与获取 | 适合做什么 | 契合度 |
| --- | --- | --- | --- | --- | --- | --- |
| [Music Genre fMRI（Nakai）](https://zenodo.org/record/8275363) | fMRI | 5 人，3 天 | 540 段 GTZAN，10 种流派 | OpenNeuro ds003720，预处理版 9.2 GB | 生成模型 encoding，Brain2Music 复现基线 | 首选 |
| [NMED-T](https://purl.stanford.edu/jn859kj8079) | 128 通道 EEG | 20 人 | 10 首完整电子节拍歌曲，含敲拍行为数据 | Stanford 仓库，共 39 GB，音频不公开只给元数据 | 节拍同步、TRF、跨被试 | 首选 |
| [OpenMIIR](https://github.com/sstober/openmiir) | EEG | 10 人 | 12 段 7 到 16 秒名曲片段，聆听加想象 | 公有领域许可 | 音乐想象解码 | 备选 |
| MUSIN-G | EEG | 20 人 | 12 段不同流派，约 2 分钟 | [见 TU Delft 论文](https://repository.tudelft.nl/file/File_2b2665ad-fc99-4966-ba53-1c0a829a4558?preview=1) | 流派与歌曲识别 | 备选 |
| Di Liberto 巴赫数据 | EEG 加 ECoG | 20 人加 3 名患者 | 巴赫单声部钢琴，MIDI 可得 | 获取方式未本次核验 | 预期模型 TRF，最接近你的 Markov 方向 | 首选（需确认可得性） |
| DEAP | EEG 加外周生理 | 约 32 人（未本次核验） | 音乐视频 | 需申请 | 情绪识别 | 不推荐，视听混合 |
| Bellier iEEG | iEEG | 29 人 | 单首 Pink Floyd | 获取方式未本次核验 | 高保真重建 | 不推荐，单曲且难获取 |

**判断**：现有数据足够做"生成模型 vs 大脑"的 encoding 研究，但不足以做干预性实验。如果你想验证 steering 后的音乐会改变脑响应，必须自己采集。这是 future 部分最有说服力的一点，也是 NSF AI Datasets 那条线的自然延伸。

## 6. 临床与应用：证据等级逐项

总体结论：音乐干预在多个领域有**短期、小到中等**的效果，几乎没有一项达到"长期有效"的高确定性。共同的降级原因是无法对受试者设盲、干预描述不统一、随访短。

| 领域 | 最高等级证据 | 规模 | 有效的结局 | 无效或不确定的结局 | 等级 |
| --- | --- | --- | --- | --- | --- |
| 痴呆（含 AD） | [Cochrane 2025, van der Steen](https://www.healthday.com/healthpro-news/mental-health/music-based-interventions-may-help-short-term-depression-behavior-with-dementia) | 30 项研究，1,720 人，多在养老机构 | 抑郁症状轻度改善（中等确定性，9 项 441 人），整体行为问题（低确定性） | 激越与攻击性可能无效（中等确定性），认知、焦虑、情绪幸福感不确定，结束 4 周后无长期效果 | B |
| 抑郁 | [Cochrane 2017, Aalbers](https://pubmed.ncbi.nlm.nih.gov/29144545/) | 9 项研究，421 人 | 音乐治疗加常规治疗，短期患者自评抑郁 SMD 为 -0.85（中等质量） | 研究间异质性大，无不良事件和功能结局数据 | B |
| 自闭症 | [Cochrane 2022, Geretsegger](https://www.cochrane.org/zh-hans/evidence/CD004381_music-therapy-autistic-people) | 26 项研究，1,165 人 | 整体改善、生活质量、症状总严重度（中等确定性），不增加不良事件 | 社交互动和言语与非言语沟通不确定（低到极低） | B |
| 卒中等后天脑损伤 | [Cochrane 2017, Magee](https://www.mcmasteroptimalaging.org/full-article/187736bb18d817f875a2ae59bfb261e7) | 29 项试验，775 人，九成为卒中 | 节律听觉刺激（RAS）使步频平均提高 10.77 步每分钟（低质量） | 上肢功能和沟通证据极低质量，不足以改变临床实践 | B 到 C |
| 帕金森步态 | [Ye 2022 Meta](https://www.frontiersin.org/journals/neurology/articles/10.3389/fneur.2022.940419/pdf) | 18 项 RCT | 步长、步速、冻结步态和 UPDRS-III 改善 | 缺乏大样本双盲试验 | B |
| 失眠 | [Cochrane 2022, Jespersen](https://pubmed.ncbi.nlm.nih.gov/36000763/) | 13 项试验，1,007 人 | 主观睡眠质量改善（中等确定性） | 客观睡眠指标可能无改善（3 项 136 人），失眠严重度极低确定性 | B |
| 疼痛 | [2016 Meta，NCCIH 汇总](https://www.nccih.nih.gov/health/providers/digest/music-and-health-science) | 97 项 RCT，9,184 人 | 疼痛强度、疼痛相关痛苦和镇痛药用量下降 | 效应大小和偏倚细节未本次核验 | B |
| 人工耳蜗用户 | 叙述性综述，如 [Hsiao & Gfeller](https://pmc.ncbi.nlm.nih.gov/articles/PMC3587135) | 无汇总 RCT | 节奏感知基本保留 | 音高、旋律、和声、音色感知普遍差，训练效果证据零散 | C |

**三点批判性观察**

1. **主观与客观的分离反复出现**：失眠中主观睡眠质量改善而客观指标不变，痴呆中情绪改善而认知不变。这提示部分效果可能来自期待和情绪调节，而不是直接改变神经功能。脑信号测量恰好能区分这两者。
2. **RAS 是机制最清楚的一类**：它直接利用第 1 块的节奏与运动耦合，而且"有节拍的音乐优于单纯节拍器"这一亚组结果说明音乐成分本身有贡献。在 keynote 里它是从机制到临床最完整的例子。
3. **干预本身无法复现**：Cochrane 多次指出"音乐"在各研究中定义不一。可控、可参数化的生成音乐能把干预变成可报告、可复现的变量，这是你从 CS 切入临床最有说服力的论点。

**与你的 health 线的对应**：ADRD 方向的证据支持"情绪和行为"而非"认知"，提案里不要承诺认知改善。听力方向的证据最薄弱，C 级，这意味着空间大但需要自己生成基础数据。

## 7. 缺口、机会打分与 keynote 骨架

**打分标准**：重要性看领域是否真缺这块（1 到 5），可行性看你一到两年内用现有资产能否做出结果（1 到 5），契合度看与你已有工作和资助方向的连接（1 到 5）。总分用于排序，最终由你决定。

| 机会 | 对应缺口 | 重要性 | 可行性 | 契合度 | 总分 |
| --- | --- | --- | --- | --- | --- |
| 干预式对齐：steering 模型内部后，检验脑对齐和脑响应是否随之改变 | 第 4 块"只看相关，不做干预" | 5 | 3 | 5 | 13 |
| 超出声学基线的脑对齐评分器，以 EEG 为主 | 第 4 块基线控制不一 | 4 | 5 | 5 | 14 |
| 转移结构层的脑编码：比较 IDyOM 式意外度与转移图结构特征对 EEG 的解释力 | 第 3 块，IDyOM 只用意外度 | 4 | 5 | 4 | 13 |
| 可参数化的生成音乐作为标准化临床干预 | 第 6 块"干预无法复现" | 5 | 2 | 4 | 11 |
| 听力损失和人工耳蜗人群的音乐脑响应数据集 | 第 6 块 C 级证据，第 5 块无此类数据 | 5 | 2 | 5 | 12 |
| 主观与客观效果分离的脑信号解释 | 第 6 块观察 1 | 4 | 3 | 3 | 10 |
| 跨被试共享的音乐解码表示 | 第 3 块，几乎全按被试训练 | 3 | 3 | 2 | 8 |
| 音乐想象解码 | 第 3 块，探索阶段 | 3 | 2 | 2 | 7 |
| 老年人群中的模型脑对齐变化，连接 ADRD | 第 4 块只用年轻人 | 4 | 2 | 4 | 10 |

**建议的 keynote 骨架（45 分钟）**

1. **为什么是音乐**（5 分钟）：音乐是少数能被生成、被精确控制、又能直接测到大脑响应的刺激。用 Salimpoor 的期待与高潮两段多巴胺开场，听众马上有感觉。
2. **大脑里的音乐通路**（8 分钟）：专门化皮层、节奏与运动、奖赏、记忆，第 1 块的表格压成一张通路图。
3. **怎样对上：encoding 与 decoding**（12 分钟）：TRF 与预期模型，从 Pink Floyd 重建到 Brain2Music，点明"重建质量多来自生成模型先验"这一批判。这部分是主体。
4. **模型像不像大脑**（7 分钟）：三个已确立结论，加上"对齐不等于机制"的提醒，引出四个空白。
5. **临床证据的真实面貌**（6 分钟）：证据等级表的精简版，强调短期、主客观分离和干预不可复现。
6. **我们的切入与开放问题**（7 分钟）：Markov 转移结构、steering 不对称、脑对齐评分器作为三个例证，结尾给出上表前三项作为 future。

**两点讲法建议**：第一，听众是生物信号方向，第 2 块的 EEG 信号分类要讲得比 CS talk 更细，第 4 块的模型细节要讲得更粗。第二，你自己的工作放在第 6 部分而不是开头，keynote 的可信度来自先把领域讲清楚。

## 参考文献（本次检索已打开或核对）

- Salimpoor VN, et al. Anatomically distinct dopamine release during anticipation and experience of peak emotion to music. Nat Neurosci 14:257, 2011. [链接](https://brams.org/2011/01/09/salimpoor/)
- Salimpoor VN, et al. Interactions between the nucleus accumbens and auditory cortices predict music reward value. Science, 2013. [链接](https://www.zlab.mcgill.ca/publications/docs/Science-2013-Salimpoor-216-9.pdf)
- Norman-Haignere S, Kanwisher N, McDermott JH. Distinct cortical pathways for music and speech revealed by hypothesis-free voxel decomposition. Neuron, 2015. [链接](https://neurosciencenews.com/auditory-processing-music-neuroscience-3285/)
- Norman-Haignere SV, et al. A neural population selective for song in human auditory cortex. Curr Biol 32:1470, 2022. [链接](https://cbmm.mit.edu/publications/neural-population-selective-song-human-auditory-cortex)
- Jacobsen JH, et al. Why musical memory can be preserved in advanced Alzheimer's disease. Brain 138:2438, 2015. [链接](https://soundhealth.ucsf.edu/node/756)
- Di Liberto GM, et al. Cortical encoding of melodic expectations in human temporal cortex. eLife 9:e51784, 2020. [链接](https://elifesciences.org/articles/51784)
- Kern P, et al. Cortical activity during naturalistic music listening reflects short-range predictions based on long-term experience. eLife 11:e80935, 2022. [链接](https://elifesciences.org/articles/80935.pdf)
- Mischler G, Li YA, Bickel S, Mehta AD, Mesgarani N. Nat Commun 16, 2025. [链接](https://ideas.repec.org/a/nat/natcom/v16y2025i1d10.1038_s41467-025-63961-7.html)
- Bellier L, et al. Music can be reconstructed from human auditory cortex activity using nonlinear decoding models. PLoS Biol 21:e3002176, 2023. [链接](https://escholarship.org/uc/item/4ms6t5cv)
- Denk TI, Takagi Y, et al. Text-to-music generation models capture musical semantic representations in the human brain. Nat Commun 17:91, 2026 (arXiv 2307.11078). [链接](https://arxiv.org/abs/2307.11078v1)
- Music decoding from fMRI with CLAP, arXiv 2406.15537, 2024. [链接](https://arxiv.org/pdf/2406.15537)
- Pepino L, et al. Better audio representations are more brain-like. arXiv 2511.16849, 2025. [链接](https://arxiv.org/abs/2511.16849v1)
- Nakai T, Koide-Majima N, Nishimoto S. Music genre neuroimaging dataset. Data in Brief 40:107675, 2022. [链接](https://zenodo.org/record/8275363)
- Losorelli S, et al. NMED-T. ISMIR 2017. [链接](https://purl.stanford.edu/jn859kj8079)
- Stober S, et al. OpenMIIR. ISMIR 2015. [链接](https://github.com/sstober/openmiir)
- van der Steen JT, et al. Music-based therapeutic interventions for people with dementia. Cochrane CD003477.pub5, 2025. [链接](https://remix.berklee.edu/mhi-citations/1802)
- Aalbers S, et al. Music therapy for depression. Cochrane CD004517.pub3, 2017. [链接](https://pubmed.ncbi.nlm.nih.gov/29144545/)
- Geretsegger M, et al. Music therapy for autistic people. Cochrane CD004381.pub4, 2022. [链接](https://www.cochrane.org/zh-hans/evidence/CD004381_music-therapy-autistic-people)
- Magee WL, et al. Music interventions for acquired brain injury. Cochrane CD006787.pub3, 2017. [链接](https://www.cochrane.org/CD006787/STROKE_music-interventions-acquired-brain-injury)
- Ye X, et al. Rhythmic auditory stimulation promotes gait recovery in Parkinson's patients. Front Neurol, 2022. [链接](https://www.frontiersin.org/journals/neurology/articles/10.3389/fneur.2022.940419/pdf)
- Jespersen KV, et al. Listening to music for insomnia in adults. Cochrane CD010459.pub3, 2022. [链接](https://pubmed.ncbi.nlm.nih.gov/36000763/)
- NCCIH. Music and Health: What the Science Says. [链接](https://www.nccih.nih.gov/health/providers/digest/music-and-health-science)
- Sala G, Gobet F. Cognitive and academic benefits of music training with children. Mem Cogn 48:1429, 2020. [链接](https://pmc.ncbi.nlm.nih.gov/articles/PMC7683441)
- Hsiao F, Gfeller K. Music perception of cochlear implant recipients. Review. [链接](https://pmc.ncbi.nlm.nih.gov/articles/PMC3587135)

**未本次核验、引用前需核对**：Grahn & Brett 2007（节拍与基底节），Zatorre 半球分工，Nozaradan 稳态诱发节拍，Kraus FFR 系列，Yamins 2014，Kell 2018，DEAP 数据集。
