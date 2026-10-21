# Literature Review — AI Stock Market Intelligence

## 1. Overview

This literature review surveys existing research on NLP-driven stock market prediction, event-driven trading strategies, and the application of large language models (LLMs) to financial text analysis.

---

## 2. Sentiment Analysis for Stock Prediction

### 2.1 Early Work

Tetlock (2007) first demonstrated that media pessimism predicts downward pressure on stock prices using a bag-of-words approach on Wall Street Journal columns. This established the foundational link between textual sentiment and market movements.

Bollen et al. (2011) used Twitter sentiment to predict DJIA movements, achieving 87.6% accuracy — though this work has faced replication challenges.

### 2.2 Deep Learning Approaches

Ding et al. (2014, 2015) applied convolutional neural networks to financial news, representing events as structured tuples (Actor, Action, Object) and achieving significant improvements over bag-of-words baselines.

Hu et al. (2018) introduced the Hierarchical Complementary Attention Network (HAN) that jointly models news events and sequential stock movements, outperforming LSTM baselines.

---

## 3. Event-Driven Trading

### 3.1 Earnings Announcements

Ball and Brown (1968) established that earnings surprises drive abnormal returns. Modern systems extend this by predicting the *direction* and *magnitude* of the reaction using pre-announcement sentiment.

### 3.2 Merger and Acquisition Events

M&A announcements consistently create 20-30% abnormal returns for target companies. NLP models trained to detect acquisition language in news can identify these events before official confirmation.

---

## 4. Large Language Models in Finance

### 4.1 GPT-Based Approaches

Lopez-Lira and Tang (2023) showed that GPT-4 sentiment on financial news significantly predicts next-day stock returns, outperforming traditional sentiment dictionaries (Loughran-McDonald).

### 4.2 FinBERT

Araci (2019) fine-tuned BERT on financial texts to create FinBERT, which significantly outperforms general-purpose sentiment models on financial corpora. However, LLMs like GPT-4 have since surpassed FinBERT on most benchmarks.

---

## 5. Retrieval-Augmented Generation (RAG)

Lewis et al. (2020) introduced RAG, combining dense retrieval with generative models. In financial contexts, RAG enables finding historical news events analogous to current events — providing contextual grounding for predictions.

---

## 6. XGBoost for Financial Prediction

Chen and Guestrin (2016) introduced XGBoost, which remains highly competitive for tabular financial data despite the rise of deep learning. Its interpretability (via SHAP values) is particularly valuable for regulated financial applications.

---

## 7. Gaps Addressed by This Project

| Gap | Our Approach |
|-----|-------------|
| Black-box LLM predictions | XGBoost with SHAP explanations |
| Generic sentiment models | Per-ticker specialized models |
| Static historical analysis | Real-time live news processing |
| Single-score outputs | 5-dimensional score system |
| No historical context | RAG vector store retrieval |

---

## 8. References

1. Tetlock, P.C. (2007). Giving content to investor sentiment. *Journal of Finance*.
2. Bollen, J., Mao, H., Zeng, X. (2011). Twitter mood predicts the stock market. *Journal of Computational Science*.
3. Ding, X., et al. (2014). Using structured events to predict stock price movement. *EMNLP*.
4. Hu, Z., et al. (2018). Listening to chaotic whispers. *WSDM*.
5. Lopez-Lira, A., Tang, Y. (2023). Can ChatGPT forecast stock price movements? *SSRN*.
6. Lewis, P., et al. (2020). Retrieval-augmented generation for knowledge-intensive NLP tasks. *NeurIPS*.
7. Chen, T., Guestrin, C. (2016). XGBoost: A scalable tree boosting system. *KDD*.
