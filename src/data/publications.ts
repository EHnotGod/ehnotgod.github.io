/**
 * 论文列表的唯一来源（single source of truth）。
 *
 * 中英文学术页都从这里取数据：
 *   - 共享：作者、年份、venue 类型、状态、**链接**（链接只维护这一份，避免两边写岔）
 *   - 分语言：标题、摘要、venue 显示名（如 Automation of Electric Power Systems / 电力系统自动化）
 *
 * 之前两份页面各写一遍数据，结果同一条 arXiv 链接在中文页被标成 website，
 * 还缺了 GitHub / ModelScope / ICML 入口——所以统一到这里。
 */

export interface PublicationLink {
  type: string
  href: string
}

export interface PublicationAuthor {
  name: string
  isMe?: boolean
  isEqual?: boolean
  isCoreContributor?: boolean
  role?: 'corresponding' | 'project-leader'
}

/** 同一个字段的中英文两版；zh 缺省时回退到 en */
export interface Bilingual {
  en: string
  zh?: string
}

export interface Publication {
  title: Bilingual
  authors: PublicationAuthor[]
  venue: Bilingual
  year: string
  type: 'conference' | 'journal' | 'workshop' | 'preprint'
  status: 'published' | 'accepted' | 'under-review' | 'preprint'
  links: PublicationLink[]
  abstract: Bilingual
}

export const publications: Publication[] = [
  {
    title: {
      en: 'TexEditor: Structure-Preserving Text-Driven Texture Editing',
      zh: 'TexEditor: Structure-Preserving Text-Driven Texture Editing'
    },
    authors: [
      { name: 'Bo Zhao' },
      { name: 'Yihang Liu', isMe: true },
      { name: 'Chenfeng Zhang' },
      { name: 'Huan Yang' },
      { name: 'Kun Gai' },
      { name: 'Wei Ji' }
    ],
    venue: { en: 'ICML', zh: 'ICML' },
    year: '2026',
    type: 'conference',
    status: 'accepted',
    links: [
      { type: 'arxiv', href: 'https://arxiv.org/abs/2603.18488' },
      { type: 'website', href: 'https://icml.cc/virtual/2026/poster/61988' },
      { type: 'github', href: 'https://github.com/KlingAIResearch/TexEditor' },
      { type: 'modelscope', href: 'https://www.modelscope.cn/datasets/zhaohhh2000/TexBench' }
    ],
    abstract: {
      en: 'Text-guided texture editing aims to modify object appearance while preserving the underlying geometric structure. However, our empirical analysis reveals that even SOTA editing models frequently struggle to maintain structural consistency during texture editing, despite the intended changes being purely appearance-related. Motivated by this observation, we jointly enhance structure preservation from both data and training perspectives, and build TexEditor, a dedicated texture editing model based on Qwen-Image-Edit-2509. Firstly, we construct TexBlender, a high-quality SFT dataset generated with Blender, which provides strong structural priors for a cold start. Secondly, we introduce StructureNFT, a RL-based approach that integrates structure-preserving losses to transfer the structural priors learned during SFT to real-world scenes. Moreover, due to the limited realism and evaluation coverage of existing benchmarks, we introduce TexBench, a general-purpose real-world benchmark for text-guided texture editing. Extensive experiments on existing Blender-based texture benchmarks and our TexBench show that TexEditor consistently outperforms strong baselines such as Nano Banana Pro. In addition, we assess TexEditor on the general purpose benchmark ImgEdit to validate its generalization. Our code and data are available at https://github.com/KlingAIResearch/TexEditor.',
      zh: '文本引导的纹理编辑旨在修改物体外观的同时保持其底层几何结构。然而，我们的实证分析表明，即使是 SOTA 编辑模型在纹理编辑中也常常难以保持结构一致性，尽管预期的修改纯粹与外观相关。基于这一观察，我们从数据和训练两个角度联合增强结构保持，构建了基于 Qwen-Image-Edit-2509 的专用纹理编辑模型 TexEditor。首先，我们构建了由 Blender 生成的高质量 SFT 数据集 TexBlender，为冷启动提供强结构先验；其次，我们引入基于强化学习的方法 StructureNFT，将结构保持损失整合进来，把 SFT 阶段学到的结构先验迁移到真实场景；此外，由于现有基准在真实性和评测覆盖上的局限，我们构建了面向文本引导纹理编辑的通用真实场景基准 TexBench。在现有基于 Blender 的纹理基准和我们的 TexBench 上的大量实验表明，TexEditor 一致地优于 Nano Banana Pro 等强基线；同时我们在通用基准 ImgEdit 上评估 TexEditor 以验证其泛化性。代码与数据见 https://github.com/KlingAIResearch/TexEditor。'
    }
  },
  {
    title: {
      en: 'GSE-Flow: Geometric SE(3)-Equivariant Flow Matching for 3D Trajectory Prediction',
      zh: 'GSE-Flow: Geometric SE(3)-Equivariant Flow Matching for 3D Trajectory Prediction'
    },
    authors: [
      { name: 'Junwei Wu' },
      { name: 'Yihang Liu', isMe: true },
      { name: 'Ruixuan Yu' },
      { name: 'Jian Sun' }
    ],
    venue: { en: 'ICML', zh: 'ICML' },
    year: '2026',
    type: 'conference',
    status: 'accepted',
    links: [
      { type: 'openreview', href: 'https://openreview.net/forum?id=EBujA4tldV' },
      { type: 'website', href: 'https://icml.cc/virtual/2026/poster/65379' },
      { type: 'github', href: 'https://github.com/aegine/GSE-Flow' }
    ],
    abstract: {
      en: 'Predicting 3D geometric trajectory requires capturing complex spatiotemporal dependencies while preserving physical symmetries. While flow matching offers a powerful generative paradigm, extending it to SE(3)-equivariant dynamics is challenging due to the inherent gap between deterministic history and stochastic evolving flows. To address this, we introduce GSE-Flow, an SE(3)-equivariant flow matching framework. We first propose a Coherent Sequence Encoding and Time-Modulated Embedding strategy that unifies historical and evolving streams, incorporating velocity and flow time via equivariant affine transformations to guide continuous evolution. We further design a Geometry-Feature Tensorization mechanism that projects node states into a tensor product space, enabling Context-Flow Fusion to guide trajectory evolution with historical context. GSE-Flow guarantees theoretical SE(3)-equivariance and achieves SOTA accuracy on MD17, MD22, and CMU MoCap benchmarks for geometric trajectory prediction, while demonstrating generality by enhancing deterministic baselines. Code is available at https://github.com/aegine/GSE-Flow.',
      zh: '3D 几何轨迹预测需要在保持物理对称性的同时捕获复杂的时空依赖。虽然 flow matching 提供了强大的生成范式，但由于确定性历史与随机演化流之间固有的差距，将其扩展到 SE(3)-等变动力学仍具挑战。为此，我们提出 GSE-Flow，一个 SE(3)-等变的 flow matching 框架。我们首先提出 Coherent Sequence Encoding 与 Time-Modulated Embedding 策略，通过等变仿射变换融合速度与流动时间来统一历史流与演化流，引导连续演化；随后设计 Geometry-Feature Tensorization 机制，将节点状态投影到张量积空间，借助 Context-Flow Fusion 用历史上下文引导轨迹演化。GSE-Flow 在理论上保证 SE(3)-等变性，并在 MD17、MD22 与 CMU MoCap 几何轨迹预测基准上取得 SOTA 精度，同时通过增强确定性基线展示了其通用性。代码见 https://github.com/aegine/GSE-Flow。'
    }
  },
  {
    title: {
      en: 'A Critical Look at Prompt-Level Performance Prediction "Illusion" in Modern T2I Models',
      zh: '对现代 T2I 图像生成模型中提示级性能预测「幻象」的审视'
    },
    authors: [{ name: 'Yihang Liu', isMe: true }],
    venue: { en: 'ICLR', zh: 'ICLR' },
    year: '2027',
    type: 'conference',
    status: 'under-review',
    links: [],
    abstract: {
      en: 'An auditing framework covering models such as Qwen, FLUX and Boogu under various sampling configs, jointly analyzing GM/AM scores, R² across samples, extreme-sample detection and budget-constrained routing. Finds that high overall R² largely comes from coarse recognition of clearly-failed samples.',
      zh: '构建覆盖 Qwen、FLUX、Boogu 等模型及多种采样配置的审计框架，联合分析 GM/AM 评分、全样本与中间区间 R²、极端样本检测及预算约束路由。发现较高的整体 R² 主要来自对明显失败样本的粗粒度识别。'
    }
  },
  {
    title: {
      en: 'LLM-based Operational Risk Assessment and Inference for Power Systems',
      zh: '基于大语言模型的电力系统运行风险评估与推演方法'
    },
    authors: [
      { name: 'Wenqi Huang' },
      { name: 'Bo Zhao' },
      { name: 'Yihang Liu', isMe: true },
      { name: 'Qiaoqiao Li' },
      { name: 'Jiaxuan Hou' },
      { name: 'Rui Su' },
      { name: 'Zhen Zhao' }
    ],
    venue: { en: 'Automation of Electric Power Systems', zh: '电力系统自动化' },
    year: '2026',
    type: 'journal',
    status: 'published',
    links: [
      {
        type: 'website',
        href: 'https://kns.cnki.net/kcms2/article/abstract?v=jXpGf_Tis3BO7y3TyZruUOK4DTQA5k7-c4YVlxn6-g-K10dRgZu67wrfTJA6yg9exDs8aiF8MkQYtZG6msQfv2aAIrUdzYJ3XCLsVKbu95n9RK-sOUDFGXVJNUCFpZp1LUMV2DieHCFFuMYHbu2Y00Yfd-KSRAf_&uniplatform=NZKPT'
      }
    ],
    abstract: {
      en: 'Under high-penetration renewable energy integration, the uncertainty and complexity of power system operation increase significantly, with long risk chains and many interacting factors; traditional rule-based and expert-experience-driven risk assessment methods struggle to meet the real-time operational needs of cross-scenario, strongly-constrained environments. General large language models show strong comprehension and generation in Q&A domains, but face high reliance on manual experience, low professional semantic accuracy, and insufficient understanding of grid topology in power system risk assessment, making them hard to adapt to the safe operation and flexible dispatch of new power systems. To this end, we propose an operational risk assessment and inference method for power systems based on knowledge transfer and structured chain-of-thought enhancement. The method first constructs multi-scenario datasets covering topology disturbances and risk grading via auxiliary annotation and expert-rule constraints, enabling efficient transfer from general models to the power domain; second, it adopts textual topology injection to improve topology awareness and constraint consistency; then, it designs programmable reward signals based on Group Relative Policy Optimization to jointly optimize inference-chain completeness, terminology consistency, and grading accuracy; finally, ablation and comparison experiments validate the effectiveness of the proposed method. Results show that the method outperforms existing large language models in both multi-step inference coherence and risk-grading accuracy, providing intelligent support for the safe and stable operation of new power systems.',
      zh: '高比例新能源接入背景下电力系统运行的不确定性与复杂性显著增加，电力系统运行风险链条长且关联因素多，传统依赖于规则库与专家经验的风险评估方法难以适应跨场景、强约束的实时运行需求。通用大语言模型在问答领域展现出较强理解与生成能力，但在电力系统风险评估任务中，面临人工经验依赖度高、专业语义准确率低、电网拓扑理解不足等问题，难以适应新型电力系统的安全运行与灵活调度需求。为此，提出一种基于知识迁移与思维链结构化增强的电力系统运行风险评估与推演方法。该方法首先通过辅助标注与专家规则约束，构建覆盖拓扑扰动和风险定级的多场景数据集，实现通用模型向电力领域的高效迁移；其次，采用文本化拓扑注入方式提升模型的拓扑感知与约束一致性；然后，基于组相对策略优化方法设计可编程奖励信号，对推演链完整性、术语一致性和定级准确率进行联合优化；最后，通过消融实验与对比实验验证了所提方法的有效性。结果表明，该方法在多步推演的连贯性与风险定级的准确性方面均优于现有大语言模型，能够为新型电力系统的安全稳定运行提供智能化支撑。'
    }
  },
  {
    title: {
      en: 'ClinKD: Cross-Modal Clinical Knowledge Distiller For Multi-Task Medical Images',
      zh: 'ClinKD: Cross-Modal Clinical Knowledge Distiller For Multi-Task Medical Images'
    },
    authors: [
      { name: 'Hongyu Ge' },
      { name: 'Longkun Hao' },
      { name: 'Zihui Xu' },
      { name: 'Zhenxin Lin' },
      { name: 'Bin Li' },
      { name: 'Shoujun Zhou' },
      { name: 'Hongjin Zhao' },
      { name: 'Yihang Liu', isMe: true }
    ],
    venue: { en: 'arXiv', zh: 'arXiv' },
    year: '2025',
    type: 'preprint',
    status: 'preprint',
    links: [
      { type: 'arxiv', href: 'https://arxiv.org/abs/2502.05928' },
      { type: 'github', href: 'https://github.com/overloadedHenry/ClinKD' }
    ],
    abstract: {
      en: 'Medical Visual Question Answering (Med-VQA) represents a critical and challenging subtask within the general VQA domain. Despite significant advancements in general VQA, multimodal large language models (MLLMs) still exhibit substantial limitations when handling multi-task VQA scenarios. These limitations manifest through erroneous spatial localization and misinterpretation of medical images, which primarily arise from two fundamental issues: inadequate image-text alignment and insufficient domain-specified knowledge for medical applications. To address these issues, we introduce the Cross-Modal Clinical Knowledge Distiller (ClinKD), an innovative framework designed to enhance image-text alignment and establish more effective medical knowledge transformation mechanisms, which enables MLLMs to perform better even when lacking prior medical knowledge. Our extensive experimental evaluations demonstrate that the ClinKD achieves state-of-the-art performance on several datasets which are challenging for Med-VQA task. The results indicate that our approach not only significantly improves image-text alignment but also effectively enables MLLMs to adapt to the medical knowledge. The source code for ClinKD is available at https://github.com/overloadedHenry/ClinKD.',
      zh: '医学视觉问答（Med-VQA）是通用 VQA 领域中一个关键且具挑战性的子任务。尽管通用 VQA 已取得显著进展，多模态大语言模型（MLLM）在处理多任务 VQA 场景时仍存在明显局限，主要表现为对医学图像的错误空间定位与误读，这主要源于两个根本问题：图像-文本对齐不足，以及医学应用领域知识缺乏。为解决这些问题，我们提出跨模态临床知识蒸馏器 ClinKD，一个旨在增强图像-文本对齐、建立更有效的医学知识转化机制的创新框架，使 MLLM 即便缺乏先验医学知识也能表现得更好。大量实验评估表明，ClinKD 在多个具有挑战性的 Med-VQA 数据集上达到 SOTA 性能，不仅显著改善了图像-文本对齐，还使 MLLM 能有效适配医学知识。源码见 https://github.com/overloadedHenry/ClinKD。'
    }
  }
]

/** 按语言把双语字段展开成 PublicationSection 需要的扁平结构 */
export function localizePublications(locale: string | undefined) {
  const isZh = locale === 'zh'
  return publications.map((pub) => ({
    ...pub,
    title: isZh ? (pub.title.zh ?? pub.title.en) : pub.title.en,
    venue: isZh ? (pub.venue.zh ?? pub.venue.en) : pub.venue.en,
    abstract: isZh ? (pub.abstract.zh ?? pub.abstract.en) : pub.abstract.en
  }))
}
