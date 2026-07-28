# Research Proposal for PhD Studies

## Adaptive Edge AI: Efficient Targeted Model Adaptation under Concept Drift on Resource-Constrained Devices

**Candidate:** Soham Deshmukh
**Supervisor:** Dr. Stefan Kuhn, Chair of Distributed Systems, Institute of Computer Science, University of Tartu
**Proposed Duration:** 4 years (August 2027 – July 2031)
**Funding Track:** State-funded Junior Research Fellow position, University of Tartu

---

## 1. Problem Statement

Edge AI systems are deployed on resource-constrained devices — microcontrollers with 264 KB of RAM, limited battery budgets, and intermittent connectivity. These systems run machine learning models that make predictions on sensor data in real time. In laboratory conditions, they perform well. In the field, they degrade silently over time.

This degradation occurs because edge environments are non-stationary. Sensors age, producing biased readings. Lighting and weather conditions shift. User behavior evolves. These changes cause a phenomenon called *concept drift*: the statistical relationship between input data and target labels changes, so the deployed model's predictions become less reliable [6]. A fixed model, frozen at deployment time, cannot adapt to these shifts. It either violates its accuracy requirements silently, or it violates its energy and latency budgets by attempting expensive retraining.

Recent work has established that Edge AI in realistic deployments is necessarily adaptive [18]. Pittorino and Roveri introduce an Agent-System-Environment (ASE) lens that formalizes what changes, what is observable, and what can be reconfigured over time. Among the ten research challenges they identify, two are directly relevant to this proposal:

**C3 — Fault/Anomaly-Driven Targeted Updates.** When utility drops, can the system infer *why* it degraded (sensor fault, distribution shift, hardware issue) and apply the *smallest effective intervention* that restores performance? Current approaches trigger blanket retraining or full parameter updates, which is wasteful and often infeasible on constrained devices.

**C7 — Lifecycle Efficiency.** Over a long deployment horizon, the cost of *maintaining* a model (monitoring for drift, retraining, updating) can exceed the cost of running inference. The field has optimized inference efficiency extensively through quantization, pruning, and hardware acceleration. But the total cost of ownership for adaptive edge systems — the sum of execution and reconfiguration costs over time — remains understudied.

The core problem this PhD addresses is: **How can an edge device detect concept drift, attribute it to a specific cause, and apply a minimal, targeted model update — all within a memory budget of 264 KB and an energy budget of millijoules per day?**

---

## 2. State of the Art and Identified Gaps

### 2.1 Concept Drift Detection on the Edge

Concept drift detection is well established for server-class systems. DDM [6], ADWIN (Adaptive Windowing) [3], and Page-Hinkley test [20] are standard algorithms. On the edge, two landmark works demonstrate feasibility:

- **Disabato and Roveri (2022)** proposed TML-CD, the first concept drift adaptation system for Tiny Machine Learning on ARM Cortex-M microcontrollers [5]. It uses a deep feature extractor with a k-NN classifier and a hybrid passive-active adaptation module. This proved that drift handling *can* fit on MCUs, but the adaptation mechanism resets the full knowledge base — it does not perform targeted, minimal updates.

- **Yamada and Matsutani (2023)** proposed a fully sequential drift detection method cooperating with on-device sequential learning (OS-ELM) [22]. On a Raspberry Pi Pico (264 KB RAM), they achieved 88.9–96.4% memory reduction over batch-based methods with only 3.8–4.3% accuracy loss. Again, adaptation is global — the entire model is updated when drift is detected.

### 2.2 Resource-Constrained Adaptation

- **Piaseczny et al. (2025)** introduced RCCDA, the first theoretically grounded adaptive update policy with provable resource guarantees using a Lyapunov drift-plus-penalty framework [17]. This is a significant advance, but it targets edge-server class devices, not microcontroller-class hardware. It also treats adaptation as a global model update, not a selective intervention.

### 2.3 Distributed Adaptation

- **FedConD** [15] and **FL-HVD** [21] address concept drift in federated learning settings, but they assume coordinated training across nodes with periodic aggregation. No existing work addresses the scenario where individual edge nodes experience *different* drifts at *different* times and must coordinate minimal, targeted updates without a central aggregator.

### 2.4 Reversible Neural Networks and Efficient Updates

Reversible neural networks (RevNets, i-RevNets) [8, 9] are architectures where each layer's activations can be reconstructed from the next layer's output. This property, originally developed for memory-efficient training, has a natural application to adaptive systems: if a model is designed to be invertible, individual components can be updated or rolled back without affecting the rest of the network. **Stefan Kuhn has published on reversible neural network architectures** [11, 13], including conditional invertible neural networks (cINNs) for bidirectional inference. This work has not been applied to concept drift adaptation.

### 2.5 Identified Gap

The literature shows an opportunity at the intersection of four areas that have not been combined:

| Area | Existing Work | Gap |
|------|--------------|-----|
| Drift detection on MCUs | Disabato & Roveri (2022), Yamada & Matsutani (2023) | Full-reset adaptation, not targeted |
| Provable resource guarantees | RCCDA (Piaseczny et al., 2025) | Targets server-class, not MCUs |
| Reversible neural networks | Kuhn et al. (2025, 2026), Gomez et al. (2017) | Never applied to drift adaptation |
| Distributed targeted updates | None | No existing work |

This proposal aims to fill this gap by combining lightweight concept drift detection on MCUs with selective, targeted model updates enabled by reversible neural network architectures, within a lifecycle-efficiency framework that accounts for both execution and maintenance costs.

---

## 3. Research Objectives and Questions

### Objective 1: Lightweight Drift Detection with Fault Attribution

**Research Question:** Can we design a drift detection and attribution method that identifies not only *that* drift occurred, but *which sensor, feature, or module* caused it, while operating within 264 KB memory and O(1) per-sample computation?

Current drift detectors (DDM, ADWIN) output a binary signal: drift or no drift. They do not localize the cause. The C3 challenge requires attribution: is the utility drop caused by sensor drift, a distribution shift in a specific feature, or a hardware fault? We propose to extend lightweight distribution-based detection methods [22] with per-feature drift scores and change localization, inspired by multivariate fault attribution techniques [12, 23].

**Methodology:**
- Implement and benchmark ADWIN2, DDM, Page-Hinkley, and KSWIN on a Raspberry Pi Pico-class device using River library [19], TensorFlow Lite Micro [1], and the MOA framework [4] for reproducibility
- Extend these methods with per-feature drift attribution using an incremental feature-wise change test
- Evaluate on real sensor datasets with labeled fault sources: environmental drift, sensor aging, and hardware faults
- Metrics: detection delay, attribution accuracy (precision/recall per fault source), memory footprint, energy per detection

### Objective 2: Targeted Model Updates via Reversible Neural Network Architectures

**Research Question:** Can reversible neural network architectures enable selective, minimal model updates that recover accuracy after drift while using an order of magnitude less energy than full retraining?

The key insight is that invertible architectures (RevNets, i-RevNets) maintain a bijective mapping between layers. If a specific module or feature space has drifted, the corresponding invertible block can be updated independently without propagating changes through the full network. This enables *surgical* model repair: identify which part of the network is affected by the attributed drift source, and update only that part.

**Methodology:**
- Design a compact reversible architecture suitable for MCU-class devices (inspired by i-RevNet [9] and Kuhn's cINN work [11])
- Implement selective block-level fine-tuning: when drift is attributed to feature group X, update only the invertible block processing X
- Compare against full model fine-tuning, incremental learning [24], and knowledge-reset baselines [5, 22]
- Evaluate on TinyML benchmarks [2] with controlled drift injection
- Metrics: accuracy recovery, energy per update, number of parameters modified, memory overhead for reversibility

### Objective 3: Lifecycle-Efficient Distributed Adaptation

**Research Question:** In a multi-node edge deployment where different nodes experience different drifts, what coordination strategy minimizes total lifecycle cost (execution + reconfiguration) while maintaining system-level accuracy?

Edge deployments are distributed by nature. A fleet of 10–100 sensor nodes may experience heterogeneous drift patterns. Sharing update information across nodes could improve accuracy and reduce per-node computation, but it costs bandwidth and energy. This tension mirrors the communication-efficiency problem in federated learning [16], but with the added constraint that each node's drift profile is unique.

**Methodology:**
- Simulate a multi-node edge deployment (10–50 nodes) with heterogeneous drift injections
- Implement coordination strategies: independent adaptation, peer-to-peer update sharing, and lightweight federated aggregation of selective updates
- Leverage the reversible update mechanism from Objective 2: nodes share only the affected invertible blocks, not full model parameters
- Evaluate communication cost, energy per node, system accuracy, and adaptation latency
- Metrics: total lifecycle energy (Σ C_run + Σ C_change per node), Energy-to-Recover [18], communication bytes per accuracy recovered

### Objective 4: Evaluation Framework for Lifecycle-Efficient Adaptive Edge AI

**Research Question:** How should adaptive edge systems be evaluated to capture long-horizon behavior, transients, and total cost of ownership?

Pittorino and Roveri's C7 and C10 challenges [18] call for new evaluation protocols. Current practice reports accuracy at a snapshot. Adaptive systems fail during transitions, not in steady state. We propose to implement and validate the ASE reporting standard (Table II in [18]) on real hardware.

**Methodology:**
- Implement the full ASE evaluation protocol: time-series reporting of U(t), C_run(t), C_chg(t), V(t) [7]
- Compute lifecycle metrics: Energy-to-Recover (E2R), Time-to-Recover (T2R), Stability Score (SS) [18]
- Publish benchmark streams with declared drift/intervention scripts for reproducibility
- Evaluate all three objectives under a unified protocol
- Compare against static deployment, full-retraining, and periodic-update baselines

---

## 4. Novel Contributions

This PhD is expected to make the following contributions:

1. **First drift detection method with integrated fault attribution** for MCU-class devices, enabling targeted (not blanket) adaptation
2. **First application of reversible neural network architectures to concept drift adaptation**, enabling selective, minimal model updates with provably bounded side effects
3. **First distributed coordination protocol for heterogeneous edge drift**, enabling lifecycle-efficient fleet-wide adaptation
4. **First comprehensive implementation of the ASE evaluation protocol** (C7/C10 from [18]) on real embedded hardware
5. **Open-source benchmark suite** for lifecycle-efficient adaptive edge AI, including drift injection scripts, evaluation metrics, and reference implementations

---

## 5. Research Plan and Timeline

### Year 1 (2027–2028): Foundations and Baseline

| Quarter | Activities | Deliverables |
|---------|-----------|-------------|
| Q1 | Literature deep dive: concept drift detection, online learning, TinyML, reversible NNs | Reading notes, annotated bibliography |
| Q2 | Implement drift detection benchmarks on laptop using River: ADWIN2, DDM, Page-Hinkley, KSWIN | Benchmarking code and results |
| Q3 | Port promising detectors to Raspberry Pi Pico (TFLite Micro); measure memory, latency, energy | Ported detector, measurements |
| Q4 | Design and implement per-feature drift attribution; evaluate on synthetic and real sensor data | Attribution method prototype, paper draft |

**Milestone:** Conference paper on lightweight drift detection with fault attribution (target: IEEE ICMLA, ECML-PKDD, or ACM SenSys)

### Year 2 (2028–2029): Targeted Updates via Reversible Architectures

| Quarter | Activities | Deliverables |
|---------|-----------|-------------|
| Q1 | Study reversible NN architectures (i-RevNet, RevNet, cINN); design compact MCU-scale version | Architecture design |
| Q2 | Implement selective block-level fine-tuning for reversible NNs | Implementation |
| Q3 | Benchmark selective vs. full updates under drift; measure energy per update | Benchmark results |
| Q4 | Integrate with drift attribution from Year 1; end-to-end C3 system on single MCU | Integrated prototype |

**Milestone:** Paper on reversible-NN-based targeted model updates for edge drift adaptation (target: IEEE TNNLS, NeurIPS, or DAC)

### Year 3 (2029–2030): Distributed Coordination

| Quarter | Activities | Deliverables |
|---------|-----------|-------------|
| Q1 | Simulate multi-node edge deployment; implement heterogeneous drift injection | Simulation framework |
| Q2 | Implement coordination strategies: independent, peer-to-peer, federated aggregation of selective updates | Coordination implementations |
| Q3 | Benchmark communication cost, energy, accuracy under different drift patterns | Benchmark results |
| Q4 | Design adaptive coordination strategy that selects update-sharing policy based on drift characteristics | Adaptive coordination policy |

**Milestone:** Paper on distributed lifecycle-efficient adaptation (target: ACM/IEEE IoTDI, IEEE INFOCOM, or ACM MobiCom)

### Year 4 (2030–2031): Integration, Evaluation, and Thesis

| Quarter | Activities | Deliverables |
|---------|-----------|-------------|
| Q1 | Implement full ASE evaluation protocol; compute lifecycle metrics (E2R, T2R, SS) | Evaluation suite |
| Q2 | Publish benchmark suite with drift injection scripts and reference implementations | Open-source benchmark |
| Q3 | Run long-horizon evaluations (30+ day deployments); finalize experiments | Experimental results |
| Q4 | Write and defend thesis | PhD thesis |

**Milestone:** PhD thesis defense; open-source benchmark suite publication

---

## 6. Supervision and Alignment

Dr. Stefan Kuhn's research spans distributed systems, reversible computation, and machine learning. His recent work includes:

- **Reversible deep learning architectures** — implementing reversible neural networks (i-RevNet-based) for NMR structure-spectrum prediction [11, 13]
- **Federated learning for IoT security** — comparing FL approaches for distributed malware detection across edge devices [14]
- **Bio-inspired optimization for edge AI** — hybrid optimization methods for real-time IoT intrusion detection [10]
- **Distributed systems infrastructure** — reversible debugging for MPI parallel applications [12]

His expertise in **reversible computation** is the specific bridge to this proposal. Reversible neural networks provide a natural architecture for selective, targeted model updates: because the mapping between layers is bijective, individual blocks can be updated or rolled back independently. This is precisely the mechanism needed for the C3 challenge. His distributed systems background is essential for Objective 3, where coordination across edge nodes requires communication-efficient protocols.

The proposal extends his reversible NN work into a new application domain (concept drift adaptation on edge devices) while building on his distributed systems experience for the multi-node coordination aspects.

---

## 7. Candidate Background

I am a DevOps engineer with three years of production experience at Wipro Ltd. I build monitoring and auto-remediation systems that detect anomalies and respond automatically in real time. This experience gives me an operational intuition for the problem this PhD addresses: I know what real anomalies look like outside curated datasets.

**Relevant technical experience:**

- **Monitoring and anomaly detection** — Built production monitoring pipelines using LogicMonitor, Prometheus, Grafana, and BigPanda for event correlation. Reduced manual incident handling by approximately 40% through event-driven Ansible automation. This experience maps directly to the drift detection and anomaly attribution challenges in Objective 1.

- **Efficient ML (quantization)** — Self-studied post-training quantization, mixed-precision quantization, and INT8 quantization applied to MobileNetV2 on CIFAR-10. Documented accuracy-F1-size-latency trade-offs systematically. This experience is relevant to Objective 2, where efficient model updates are the core challenge.

- **Edge deployment** — Built a real-time gesture recognition pipeline using MediaPipe, OpenCV, pyFirmata, and Arduino UNO to control home appliances. This project required working within hardware constraints (128 KB Flash, 2 KB SRAM on the Arduino), teaching me the practical realities of inference on resource-limited devices.

- **Programming** — Python (primary), Bash, Ansible (YAML), basic C/C++ for Arduino. Familiar with PyTorch, TensorFlow Lite, Jupyter for experimentation.

**Academic background:** MCA (Master of Computer Applications), CGPA 7.74. BCS (Bachelor of Computer Science), CGPA 8.63. Microsoft Certified: Azure Fundamentals (AZ-900). LogicMonitor Certified Professional.

**Strengths relevant to this PhD:** Practical systems building, anomaly detection intuition from production experience, self-directed learning in efficient ML, comfort with hardware-software co-design.

**Areas for growth:** I have no publications and no formal research training. I have been studying concept drift, adaptive systems, and edge AI for four months (mid-2026 onward). I plan to spend 2026–2027 building the theoretical foundations needed for this PhD through independent reading, the River library experiments, and collaboration with Dr. Kuhn on a pilot study before the PhD start date.

---

## 8. Timeline and Feasibility

The PhD is proposed for four years (August 2027 – July 2031), aligned with the standard University of Tartu junior research fellow contract.

**Risk assessment:**

| Risk | Likelihood | Mitigation |
|------|-----------|------------|
| MCU memory constraints too tight for reversible NN architecture | Medium | Start with simplest architectures (single invertible block); iterate toward full RevNet if feasible |
| Drift attribution accuracy insufficient for selective updates | Medium | Evaluate multiple attribution methods; fall back to block-level updates (coarser granularity) |
| Distributed coordination costs exceed benefits | Low | Theoretical analysis before implementation; use simulation to find regimes where coordination helps |
| Evaluation protocol adoption by community | Low | Publish open-source tools; the ASE framework has momentum from Roveri's group |

**Resources required:**
- Raspberry Pi Pico / ESP32-S3 / STM32 development boards
- Sensor kits for real-world drift data collection
- Standard compute hardware for simulation experiments
- Access to University of Tartu Distributed Systems Chair infrastructure

---

## 9. Expected Outcomes and Impact

### Scientific Impact
- First demonstration of targeted, attribution-driven model updates for MCU-class devices
- First application of reversible neural networks to concept drift adaptation
- New evaluation standard for lifecycle-efficient adaptive edge AI

### Practical Impact
- Open-source benchmark suite enabling reproducible comparison of adaptive edge systems
- Reference implementations deployable on $4 microcontrollers
- Design principles for industrial edge deployments where reliability over time is critical

### Career Impact
- The PhD produces a researcher who can bridge ML systems and distributed systems — a skills profile in high demand for MLOps, edge AI, and AI infrastructure roles at companies deploying ML in production.

---

## 10. References

[1] M. Abadi et al. TensorFlow: A system for large-scale machine learning. 12th USENIX OSDI, 2016.

[2] C. R. Banbury et al. MLPerf Tiny: Benchmarking machine learning on the edge. NeurIPS Datasets and Benchmarks, 2021.

[3] A. Bifet and R. Gavalda. Learning from time-changing data with adaptive windowing. SIAM International Conference on Data Mining, 2007.

[4] A. Bifet et al. Machine Learning for Data Streams with MOA. MIT Press, 2018.

[5] S. Disabato and M. Roveri. Tiny machine learning for concept drift. IEEE Transactions on Neural Networks and Learning Systems, 35(6):8470–8481, 2022.

[6] J. Gama et al. A survey on concept drift adaptation. ACM Computing Surveys, 46(4):1–37, 2014.

[7] J. Gama et al. On evaluating stream learning algorithms. Machine Learning, 90(3):317–346, 2013.

[8] A. N. Gomez et al. The reversible residual network: backpropagation without storing activations. NeurIPS, 2017.

[9] J.-H. Jacobsen et al. i-RevNet: Deep invertible networks. ICLR, 2018.

[10] T. A. L. Ibaisi, M. Kazim, S. Kuhn, M. Kaiiali, M. U. Rehman. A hybrid bio-inspired encoding and feature selection for real-time IoT network intrusion detection using deep learning framework. Internet of Things (Elsevier), 101957, 2026.

[11] S. Kuhn, V. Dwarka, P. K. Grenda, E. Vainikko. Reversible deep learning for 13C NMR in chemoinformatics: On structures and spectra. arXiv:2602.03875, 2026.

[12] S. Kuhn, M. Tiks, O. K. Martens, E. Vainikko. A reversible debugger for MPI applications with flexible backends. Future Generation Computer Systems, 181:108418, 2026.

[13] S. Kuhn et al. Implementing reversible neural networks. 17th International Conference on Reversible Computation (RC 2025), LNCS 15716, pp. 155–161, 2025.

[14] T. A. L. Ibaisi, S. Kuhn, M. Kazim, I. Kara, T. Altindag, M. U. Rehman. A comparative study of federated learning and amino acid encoding with IoT malware detection as a case study. Big Data and Cognitive Computing, 10(4):111, 2026.

[15] Z. Li et al. FedConD: Concept drift detection in federated learning for IoT. IEEE International Conference on Big Data, 2023.

[16] B. McMahan et al. Communication-efficient learning of deep networks from decentralized data. AISTATS, 2017.

[17] A. Piaseczny, M. K. C. Shisher, S. Wang, C. G. Brinton. RCCDA: Adaptive model updates in the presence of concept drift under a constrained resource budget. NeurIPS, 2025.

[18] F. Pittorino and M. Roveri. Position paper: From edge AI to adaptive edge AI. arXiv:2604.07360, 2026.

[19] River: online machine learning in Python. https://riverml.xyz/

[20] E. S. Page. Continuous inspection schemes. Biometrika, 41(1–2):100–115, 1954.

[21] V. Tolpegin et al. FL-HVD: Heterogeneous virtual drift detection in federated learning. IEEE Transactions on Dependable and Secure Computing, 2023.

[22] T. Yamada and H. Matsutani. A lightweight concept drift detection method for on-device learning on resource-limited edge devices. IEEE IPDPSW, 2023.

[23] M. Liu et al. Root cause analysis of anomalies in multivariate time series. ACM SIGMOD, 2021.

[24] R. Elwell and R. Polikar. Incremental learning of concept drift in nonstationary environments. IEEE Transactions on Neural Networks, 22(10):1517–1531, 2011.
