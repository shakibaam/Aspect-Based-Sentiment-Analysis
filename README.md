# Aspect-Based Sentiment Analysis (ABSA)- CS686 Course Project

This repository implements **Aspect-Based Sentiment Analysis (ABSA)** using End to End approach and also explores **prompt engineering with Gemini** for ABSA-related tasks. The End to end approach combines **BERT** for contextualized embeddings and **CRF** for sequence labeling.

### Key Features
- **End-to-End ABSA**: Leverages a unified tagging scheme with tags like `B-POS`, `I-NEG`, `E-NEU`, etc., for efficient representation of aspect terms and sentiments.
- **BERT + CRF Architecture**: Combines BERT for token embeddings and CRF for enforcing tag consistency in sequence labeling.
- **Prompt Engineering with Gemini**: Incorporates prompt-based approaches for ABSA tasks and evaluates Gemini's performance in generating responses tailored to engineering solutions.

### How It Works
1. **Input Representation**: Tokenized input with embeddings (token, position, and segment) passed through BERT's transformer layers for contextualized token representations.
2. **Sequence Labeling**: Contextualized embeddings are fed into a CRF layer to predict the tagging sequence.
3. **Prompt Engineering**: Evaluates the potential of Gemini in ABSA tasks through engineered prompts and response evaluation.

### Tags
- **B, I, E, S**: Represent token positions in aspect terms.
- **POS, NEG, NEU**: Sentiment labels.
- **O**: Tokens outside any aspect term.

---

Explore the `ABSA.ipynb` for implementation details, Gemini prompt engineering insights, and results.
