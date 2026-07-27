"""Curriculum map + practice-problem bank for Krish Naik's
'Complete Generative AI with LangChain & HuggingFace' (56 sections / 257 lectures).

Ordered list of sections. Each section:
  id         - stable slug
  title      - human readable
  stage      - foundations | core-genai | agents | advanced | deployment
  optional   - True for sections a proficient learner may skip (won't be nagged about)
  keywords   - lowercase tokens; if a pushed notebook's name or content
               contains any, the section counts as 'covered'
  problems   - practice tasks (concept / code / mini-project)
  checkpoints- quick self-check questions

Edit freely - the generator only relies on these keys.
"""

CURRICULUM = [
    # ---------------- FOUNDATIONS: Python (you skipped these) ----------------
    {
        "id": "python-basics",
        "title": "Python Basics (syntax, variables, datatypes, operators)",
        "stage": "foundations", "optional": True,
        "keywords": ["python-basics", "variables", "datatypes", "operators", "syntax"],
        "problems": [
            "Skim-check: write a one-cell cheat-sheet of Python truthiness, mutable vs immutable types, and slicing.",
        ],
        "checkpoints": ["Mutable vs immutable - name two of each and one gotcha."],
    },
    {
        "id": "python-oop",
        "title": "Python OOP (classes, inheritance, polymorphism, magic methods)",
        "stage": "foundations", "optional": True,
        "keywords": ["oop", "class", "inheritance", "polymorphism", "encapsulation", "magic-method", "dunder"],
        "problems": [
            "Skim-check: implement a class with __init__, __repr__, __eq__ and one @property, then subclass it and override a method.",
        ],
        "checkpoints": ["What do __repr__ and __eq__ let you do that a plain class can't?"],
    },

    # ---------------- FOUNDATIONS: NLP ----------------
    {
        "id": "nlp-preprocessing",
        "title": "NLP Text Preprocessing (tokenization, stemming, lemmatization, stopwords, POS, NER)",
        "stage": "foundations", "optional": False,
        "keywords": ["tokeniz", "stemming", "lemmatiz", "stopword", "nltk", "pos-tag", "named-entity", "ner", "preprocess"],
        "problems": [
            "Take one paragraph. Run tokenization, stemming (Porter), and lemmatization (WordNet) with NLTK. Put the three outputs side by side in a table and explain where stemming and lemmatization disagree and why.",
            "Do POS tagging + Named Entity Recognition on a news sentence. List every entity NLTK finds and its type; note one it gets wrong.",
            "Write a reusable clean_text(text) function: lowercase -> remove punctuation -> tokenize -> drop stopwords -> lemmatize. Run it on 3 messy sentences.",
        ],
        "checkpoints": [
            "Stemming vs lemmatization: which is faster, which is more correct, and why?",
            "Why remove stopwords for BoW/TF-IDF but NOT before feeding a transformer?",
        ],
    },
    {
        "id": "text-representation",
        "title": "Text Representation (One-Hot, BoW, N-grams, TF-IDF)",
        "stage": "foundations", "optional": False,
        "keywords": ["one-hot", "bag-of-words", "bow", "n-gram", "ngram", "tf-idf", "tfidf", "countvectorizer"],
        "problems": [
            "On a tiny corpus (4-5 sentences), build BoW with CountVectorizer and TF-IDF with TfidfVectorizer. Print both matrices and explain why the same word gets different weights across documents in TF-IDF.",
            "Turn on bigrams (ngram_range=(1,2)) and show how the vocabulary and matrix change. Give one example where a bigram captures meaning a unigram loses.",
            "Explain in a markdown cell the biggest weakness shared by OHE, BoW and TF-IDF (hint: they know nothing about meaning) - this motivates embeddings.",
        ],
        "checkpoints": [
            "What does the IDF term actually penalize?",
            "Why does BoW vocabulary size blow up, and what does that cost you?",
        ],
    },
    {
        "id": "word-embeddings",
        "title": "Word Embeddings & Word2Vec (CBOW, Skip-gram, Avg Word2Vec)",
        "stage": "foundations", "optional": False,
        "keywords": ["word2vec", "word embedding", "cbow", "skip-gram", "skipgram", "gensim", "avgword2vec"],
        "problems": [
            "Train (or load a pretrained) Word2Vec with gensim. Find the 5 nearest words to 3 query words and try the classic king - man + woman analogy. Record what works and what doesn't.",
            "Explain CBOW vs Skip-gram in a markdown cell: what predicts what in each, and which handles rare words better.",
            "Build an Average-Word2Vec sentence vector by averaging word vectors, then rank a few sentences by cosine similarity to a query sentence.",
        ],
        "checkpoints": [
            "Why can Word2Vec do analogies (king-man+woman) when TF-IDF cannot?",
            "What is the core limitation of a STATIC embedding (one vector per word regardless of context)?",
        ],
    },

    # ---------------- FOUNDATIONS: Deep Learning for NLP ----------------
    {
        "id": "ann-basics",
        "title": "ANN Fundamentals & Classification/Regression Project",
        "stage": "foundations", "optional": False,
        "keywords": ["ann", "neural-network", "keras", "tensorflow", "optimizer", "loss-function", "backprop"],
        "problems": [
            "Build an ANN classifier in Keras on a tabular dataset: feature-transform with sklearn, pick an optimizer + loss, train, and plot train vs val loss. Diagnose over/underfitting from the curves.",
            "Do a grid search over number of hidden layers and neurons. Record which config wins and by how much.",
            "Wrap the trained model in a tiny Streamlit app that takes inputs and returns a prediction.",
        ],
        "checkpoints": [
            "What does the optimizer do vs what the loss function does?",
            "How do you read overfitting off a train/val loss plot?",
        ],
    },
    {
        "id": "rnn",
        "title": "RNNs (forward/backprop through time, problems with RNN) + Embedding/Simple-RNN project",
        "stage": "foundations", "optional": False,
        "keywords": ["rnn", "recurrent", "simplernn", "embedding-layer", "imdb", "bptt", "sequence"],
        "problems": [
            "Train a Simple RNN with a Keras Embedding layer on IMDB sentiment. Report accuracy and show 3 predictions with their probabilities.",
            "In a markdown cell, explain the vanishing-gradient problem: why long sequences break plain RNN training. Reference backprop-through-time.",
            "Deploy the trained RNN as a Streamlit app that classifies a pasted review.",
        ],
        "checkpoints": [
            "Why do RNNs struggle with long-range dependencies?",
            "What does the Embedding layer learn that one-hot input can't give you?",
        ],
    },
    {
        "id": "lstm-gru",
        "title": "LSTM & GRU (gates, architecture, variants) + Next-Word project",
        "stage": "foundations", "optional": False,
        "keywords": ["lstm", "gru", "forget-gate", "input-gate", "output-gate", "next-word", "bidirectional"],
        "problems": [
            "Build a next-word predictor with an LSTM. Train it on a text corpus and generate 20 words from a seed phrase.",
            "In a markdown cell, walk through the forget / input / output gates: what each decides and how they fix the RNN gradient problem.",
            "Swap the LSTM for a GRU on the same task. Compare parameter count, training time, and quality.",
        ],
        "checkpoints": [
            "What does the forget gate do, concretely?",
            "GRU vs LSTM: what does GRU trade away for speed?",
        ],
    },
    {
        "id": "seq2seq-attention",
        "title": "Encoder-Decoder (Seq2Seq) & Attention Mechanism",
        "stage": "foundations", "optional": False,
        "keywords": ["encoder-decoder", "seq2seq", "sequence-to-sequence", "attention", "context-vector"],
        "problems": [
            "In a markdown cell + a simple diagram, explain the encoder-decoder bottleneck (one fixed context vector) and how attention removes it.",
            "Implement or trace a toy attention weight computation over a 5-token input for one decoder step. Show which input tokens get the most weight.",
            "Give one concrete task (e.g. translation) and explain what attention 'looks at' when producing a specific output word.",
        ],
        "checkpoints": [
            "What is the single fixed-size bottleneck in vanilla seq2seq?",
            "In one sentence: what does an attention weight represent?",
        ],
    },
    {
        "id": "transformers",
        "title": "Transformers (self-attention, multi-head, positional encoding, layer norm, encoder/decoder)",
        "stage": "foundations", "optional": False,
        "keywords": ["transformer", "self-attention", "multi-head", "positional-encoding", "layer-norm", "masked-attention"],
        "problems": [
            "Explain self-attention with the Q/K/V analogy in your own words, then compute a single self-attention output for a 3-token toy example by hand (or in numpy).",
            "Why positional encoding? Show what information is lost if you remove it, and describe how sinusoidal encoding injects order.",
            "Diagram the full encoder block (multi-head attention -> add&norm -> FFN -> add&norm) and explain what masked multi-head attention adds in the decoder.",
        ],
        "checkpoints": [
            "What are Q, K, and V, and how do they produce attention weights?",
            "Why is multi-head attention better than a single attention head?",
            "What does the decoder's causal mask prevent?",
        ],
    },

    # ---------------- CORE GEN AI: LangChain ----------------
    {
        "id": "genai-intro",
        "title": "Generative AI Intro (AI vs ML vs DL vs GenAI, how LLMs are trained)",
        "stage": "core-genai", "optional": False,
        "keywords": ["generative-ai", "genai", "llm-training", "pretraining", "evolution-of-llm"],
        "problems": [
            "Write a one-page markdown cell placing AI > ML > DL > GenAI as nested sets, with one example each.",
            "Summarize how an LLM like GPT/Llama is trained: pretraining objective -> fine-tuning -> alignment (RLHF/DPO). One paragraph each.",
        ],
        "checkpoints": [
            "What is the self-supervised pretraining objective of a base LLM?",
            "Why isn't a base (pretrained) model directly a helpful chatbot?",
        ],
    },
    {
        "id": "langchain-core",
        "title": "LangChain Core (ecosystem, OpenAI/Groq, LCEL, prompts, output parsers, LangServe)",
        "stage": "core-genai", "optional": False,
        "keywords": ["langchain", "lcel", "prompt", "stroutput", "output-parser", "groq", "langserve", "langsmith"],
        "problems": [
            "Build prompt | model | StrOutputParser with LCEL against a Groq (Llama3) model. Invoke it on 3 inputs.",
            "Add a Pydantic structured-output parser so the model returns validated JSON {answer, confidence, sources}. Handle a parse failure gracefully.",
            "Expose one chain as an API with LangServe (or describe the /invoke and /stream routes if you can't run a server now). Enable LangSmith tracing and note what the trace shows.",
        ],
        "checkpoints": [
            "What does the | operator do in LCEL and what interface makes it composable?",
            "What does LangSmith give you that print-debugging does not?",
        ],
    },
    {
        "id": "data-ingestion-splitting",
        "title": "Data Ingestion & Text Splitting (loaders, recursive/char/HTML/JSON splitters)",
        "stage": "core-genai", "optional": False,
        "keywords": ["loader", "ingestion", "text-split", "recursive", "chunk", "document-loader"],
        "problems": [
            "Load a PDF, a web page, and a JSON file with three different loaders. Print len(docs) and metadata for each.",
            "Split one long doc with RecursiveCharacterTextSplitter at (500/50) then (1000/200). Compare chunk counts and inspect a boundary to see overlap in action.",
            "Write ingest_folder(path) that chunks every PDF in a folder and tags each chunk with its source filename.",
        ],
        "checkpoints": [
            "Why is chunk overlap useful for retrieval?",
            "When would you pick the HTML-header splitter over the recursive character splitter?",
        ],
    },
    {
        "id": "embeddings-vectorstores",
        "title": "Embeddings & Vector Stores (OpenAI/Ollama/HuggingFace, FAISS, ChromaDB)",
        "stage": "core-genai", "optional": False,
        "keywords": ["faiss", "chroma", "chromadb", "vectorstore", "vector store", "ollama embedding", "huggingface embedding"],
        "problems": [
            "Embed 5 sentences (2 sport, 2 cooking, 1 mixed) and print the pairwise cosine similarity matrix. Confirm same-topic pairs score higher.",
            "Build a FAISS index and a Chroma store from the same chunks, run the same 3 queries against both, and compare retrieved chunks.",
            "Persist Chroma to disk, restart the kernel, reload and query WITHOUT re-embedding. Prove re-embedding didn't happen.",
        ],
        "checkpoints": [
            "One sentence: what is an embedding and why do similar meanings sit close?",
            "FAISS vs Chroma - when do you reach for each?",
        ],
    },
    {
        "id": "rag",
        "title": "RAG Document Q&A (retrievers, chains, Groq+Llama3)",
        "stage": "core-genai", "optional": False,
        "keywords": ["rag", "retrieval augmented", "document q&a", "retriever", "retrieval-augmented"],
        "problems": [
            "Build an end-to-end RAG chain (loader->split->embed->vectorstore->retriever->prompt->LLM) and ask 3 questions answerable only from your document.",
            "Ask a question NOT in the document, then add a prompt instruction forcing 'I don't know' when context is insufficient. Show before/after.",
            "Print retrieved chunks next to the final answer so you can audit which context drove it. Try k=2 vs k=6 and note the trade-off.",
        ],
        "checkpoints": [
            "What does RAG solve that a bare LLM can't?",
            "How does retriever k trade recall against prompt bloat/cost?",
        ],
    },
    {
        "id": "chatbots-memory",
        "title": "Chatbots with Message History & Conversational Q&A",
        "stage": "core-genai", "optional": False,
        "keywords": ["chatbot", "message history", "conversational", "session_id", "session-id", "runnablewithmessagehistory"],
        "problems": [
            "Build a chatbot with RunnableWithMessageHistory that remembers earlier turns. Prove it by referencing something said 2 messages ago.",
            "Add per-session history keyed by session_id so two users get independent conversations in one process.",
            "Build a conversational RAG bot: it should use chat history to resolve a follow-up like 'and what about the second one?'.",
        ],
        "checkpoints": [
            "How is 'memory' actually implemented (it's not hidden state)?",
            "As history grows, what happens to cost/latency and how do you bound it?",
        ],
    },

    # ---------------- AGENTS ----------------
    {
        "id": "tools-agents",
        "title": "Tools & Agents (search engine, custom tools, agent executors)",
        "stage": "agents", "optional": False,
        "keywords": ["agent", "tool", "agent-executor", "wikipedia", "arxiv", "tavily", "search-engine"],
        "problems": [
            "Build an agent with 3 tools (Wikipedia, Arxiv, web search). Ask a question that forces it to pick the right tool; inspect its reasoning trace.",
            "Write your own @tool (calculator or word-counter) and force the agent to call it.",
            "Ask something no tool can answer and add a guardrail so it stops instead of looping.",
        ],
        "checkpoints": [
            "How does an agent DECIDE which tool to call?",
            "Chain vs agent - what's the core difference?",
        ],
    },
    {
        "id": "sql-agent",
        "title": "Chat with SQL Databases (SQLite, MySQL, SQL toolkit)",
        "stage": "agents", "optional": False,
        "keywords": ["sql", "sqlite", "mysql", "sql-toolkit", "text-to-sql", "database"],
        "problems": [
            "Point a SQL agent at a SQLite DB and ask 3 natural-language questions; inspect the generated SQL each time.",
            "Add a read-only safeguard so it can never DELETE/DROP. Try to trick it and confirm the guard holds.",
            "Compare accuracy with clear column names vs cryptic ones - note how schema naming affects text-to-SQL.",
        ],
        "checkpoints": [
            "Why is read-only enforcement critical here?",
            "How does the model learn the schema before writing SQL?",
        ],
    },
    {
        "id": "summarization",
        "title": "Text Summarization (stuff / map-reduce / refine) + YouTube/URL & Math projects",
        "stage": "agents", "optional": False,
        "keywords": ["summariz", "map-reduce", "stuff-chain", "refine", "youtube", "gemma"],
        "problems": [
            "Summarize a long doc three ways (stuff, map_reduce, refine). Compare quality and token usage in a table.",
            "Summarize a doc far longer than the context window; explain why 'stuff' fails but map_reduce works.",
            "Build a YouTube-transcript or website summarizer that outputs 5 bullets + a one-line TL;DR.",
        ],
        "checkpoints": [
            "When does map_reduce beat stuff, and what does it cost?",
            "What is the failure mode of 'stuff'?",
        ],
    },
    {
        "id": "langgraph",
        "title": "LangGraph (state, ReAct agents, memory, human-in-the-loop, multi-agent, MCP)",
        "stage": "agents", "optional": False,
        "keywords": ["langgraph", "langraph", "react-agent", "react agent", "state-graph", "stategraph", "human-in-the-loop"],
        "problems": [
            "Build a LangGraph with 3 nodes and a conditional edge that routes on state. Trace the path for two different inputs.",
            "Build a ReAct agent in LangGraph with one tool and persistent memory across turns.",
            "Add a human-in-the-loop interrupt before a 'dangerous' action, then a cycle (retry-until-valid) with a stop condition.",
        ],
        "checkpoints": [
            "What does LangGraph give you that plain LCEL chains don't?",
            "What is 'state' in a LangGraph and how do nodes mutate it?",
        ],
    },

    # ---------------- CORE PROJECTS & INTEGRATIONS ----------------
    {
        "id": "huggingface-integration",
        "title": "HuggingFace + LangChain Integration",
        "stage": "core-genai", "optional": False,
        "keywords": ["huggingface", "hf-endpoint", "hf-pipeline", "transformers-pipeline", "hub"],
        "problems": [
            "Run a HuggingFace pipeline for summarization + sentiment, comparing a hosted HuggingFaceEndpoint vs a local HuggingFacePipeline.",
            "Swap your vector store's embeddings from OpenAI to a HuggingFace sentence-transformers model and re-run a query; note any change.",
            "Build a small end-to-end app (LangChain + a HuggingFace model) that does one useful task start to finish.",
        ],
        "checkpoints": [
            "What lives on the HuggingFace Hub besides model weights?",
            "Why prefer an open HF embedding model over a paid embedding API sometimes?",
        ],
    },
    {
        "id": "pdf-rag-astradb",
        "title": "PDF Query RAG with AstraDB",
        "stage": "core-genai", "optional": False,
        "keywords": ["astradb", "astra", "cassandra", "pdf-rag"],
        "problems": [
            "Ingest a PDF into an AstraDB vector store and run RAG queries; confirm vectors persist across runs.",
            "Add metadata filtering (by page/section) to AstraDB retrieval.",
            "Compare AstraDB (managed, durable) vs local FAISS (in-memory) for the same PDF - list the trade-offs.",
        ],
        "checkpoints": [
            "Why use a managed vector DB over in-memory FAISS for a real app?",
            "What does metadata filtering enable that pure similarity search can't?",
        ],
    },
    {
        "id": "code-assistant",
        "title": "Multi-Language Code Assistant (CodeLlama)",
        "stage": "core-genai", "optional": False,
        "keywords": ["code-assistant", "codellama", "gradio", "code-generation"],
        "problems": [
            "Run CodeLlama (via Ollama) and ask for the same function in Python, JS, and Go. Verify each runs.",
            "Build a Gradio/Streamlit UI: paste code -> get an explanation back.",
            "Feed it buggy code and prompt for a fix; confirm the fix works.",
        ],
        "checkpoints": [
            "Why do code-specialized models beat general chat models at coding?",
            "What context makes a code assistant project-aware?",
        ],
    },
    {
        "id": "nvidia-nim",
        "title": "NVIDIA NIM RAG with LangChain",
        "stage": "advanced", "optional": True,
        "keywords": ["nvidia", "nim", "nim-endpoint"],
        "problems": [
            "Build a RAG Document Q&A using an NVIDIA NIM model and compare its output to your Groq/Ollama baseline on one query.",
            "Swap a NIM model into an existing RAG chain with minimal code change - note how provider abstraction helps.",
        ],
        "checkpoints": ["What does NIM package that raw weights don't?"],
    },
    {
        "id": "crewai",
        "title": "Multi-Agent Systems with CrewAI (YouTube -> Blog)",
        "stage": "advanced", "optional": False,
        "keywords": ["crewai", "crew", "multi-agent", "researcher", "writer"],
        "problems": [
            "Build a Researcher + Writer crew that turns a topic (or YouTube video) into a short blog post. Inspect how tasks pass between agents.",
            "Give the Researcher a web-search tool and observe how it changes the output.",
            "Give two agents conflicting goals, watch it break, then fix it with clearer task definitions.",
        ],
        "checkpoints": [
            "What does multi-agent buy you over one well-prompted agent?",
            "Agent vs task in CrewAI - what's the distinction?",
        ],
    },
    {
        "id": "hybrid-search",
        "title": "Hybrid Search RAG (Pinecone, Reciprocal Rank Fusion)",
        "stage": "advanced", "optional": False,
        "keywords": ["hybrid-search", "pinecone", "rrf", "reciprocal-rank", "bm25", "ensemble"],
        "problems": [
            "Build a hybrid retriever (dense embeddings + sparse BM25) with an EnsembleRetriever on Pinecone. Compare to dense-only on a keyword-heavy query.",
            "Explain Reciprocal Rank Fusion in a markdown cell and show how it merges two ranked lists.",
            "Find one query where BM25 wins and one where dense wins; explain why.",
        ],
        "checkpoints": [
            "What query type does keyword/sparse search handle better than embeddings?",
            "What does Reciprocal Rank Fusion actually combine?",
        ],
    },
    {
        "id": "graph-db",
        "title": "Graph DB with LangChain (Neo4j, Knowledge Graphs, Cypher)",
        "stage": "advanced", "optional": False,
        "keywords": ["neo4j", "graph-db", "cypher", "knowledge-graph", "graphqa", "auradb"],
        "problems": [
            "Create a Neo4j AuraDB instance, load some data, and write 3 Cypher queries by hand (node lookup, relationship traversal, aggregation).",
            "Use GraphCypherQAChain to answer natural-language questions; inspect the Cypher it generates.",
            "Extract (entity)-[relation]->(entity) triples from unstructured text with an LLM and build a tiny knowledge graph.",
        ],
        "checkpoints": [
            "When is a graph DB a better retrieval fit than a vector store?",
            "Node, relationship, property - define each in graph terms.",
        ],
    },
    {
        "id": "finetuning",
        "title": "Fine-Tuning LLMs (Quantization, LoRA/QLoRA, Gemma, Lamini)",
        "stage": "advanced", "optional": False,
        "keywords": ["finetun", "fine-tun", "quantiz", "lora", "qlora", "peft", "lamini", "gemma"],
        "problems": [
            "Markdown cell: explain quantization + the math intuition behind LoRA and QLoRA, and when to pick each vs full fine-tuning.",
            "Fine-tune a small model (Gemma or via Lamini) with LoRA/PEFT on a tiny custom dataset. Compare outputs before vs after.",
            "Quantize a model to 4-bit and measure the memory drop and any quality change.",
        ],
        "checkpoints": [
            "Why does LoRA let you fine-tune big models on modest hardware?",
            "When is fine-tuning the wrong tool and RAG the right one?",
        ],
    },

    # ---------------- DEPLOYMENT ----------------
    {
        "id": "deployment",
        "title": "Deployment (Streamlit Cloud, HuggingFace Spaces, AWS Bedrock/Lambda/SageMaker)",
        "stage": "deployment", "optional": False,
        "keywords": ["deploy", "streamlit-cloud", "huggingface-spaces", "aws", "bedrock", "lambda", "sagemaker"],
        "problems": [
            "Wrap a RAG app in Streamlit (input, submit, show retrieved sources) and run it locally.",
            "Deploy it to Streamlit Cloud or HuggingFace Spaces (or write every step + secrets handling if you can't deploy now).",
            "Markdown note: how you'd handle API keys, rate limits, and cost monitoring in production.",
        ],
        "checkpoints": [
            "How do you keep API keys safe in a public demo?",
            "Main cost drivers of a deployed GenAI app - name three and how to monitor them.",
        ],
    },

    # ---------------- ADVANCED AGENTS ----------------
    {
        "id": "claude-code",
        "title": "Claude Ecosystem & Claude Code (agents, hooks, skills, plugins)",
        "stage": "advanced", "optional": True,
        "keywords": ["claude-code", "claude", "hooks", "skills", "plugins", "agent-teams"],
        "problems": [
            "Set up Claude Code and build a simple agent for a repo task. Note what a hook lets you automate that a prompt can't.",
            "Create one custom skill and one hook; describe when each fires.",
        ],
        "checkpoints": ["What's the difference between a skill, a hook, and a plugin in Claude Code?"],
    },
    {
        "id": "deep-agents",
        "title": "Deep Agents (backends, context engineering, sub-agents)",
        "stage": "advanced", "optional": True,
        "keywords": ["deep-agent", "sub-agent", "context-engineering", "backend"],
        "problems": [
            "Build a Deep Agent with sub-agents and describe how context (input, memory, skills) is engineered for each.",
            "Compare Deep Agents vs the raw Claude SDK: what does the Deep Agents layer add?",
        ],
        "checkpoints": ["What problem does 'context engineering' solve as agents get complex?"],
    },
    {
        "id": "mcp",
        "title": "Model Context Protocol (MCP) - components, communication, Claude Desktop",
        "stage": "advanced", "optional": False,
        "keywords": ["mcp", "model-context-protocol", "mcp-server", "claude-desktop"],
        "problems": [
            "Explain MCP's components (host, client, server) and how they communicate, in a diagram + markdown.",
            "Wire up (or trace) an MCP server with Claude Desktop / LangGraph and call one of its tools.",
        ],
        "checkpoints": [
            "What problem does MCP standardize?",
            "What is an MCP server vs an MCP client?",
        ],
    },
    {
        "id": "capstone",
        "title": "Capstone: Personalized AI Tutor (LangChain + HuggingFace)",
        "stage": "advanced", "optional": False,
        "keywords": ["ai-tutor", "capstone", "personalized-tutor", "final-project"],
        "problems": [
            "Design the AI Tutor: which pieces from this course does it use (RAG for course notes? memory? agents/tools? a HF model)? Write the architecture first.",
            "Build a minimal version: ingest your own course notes, add memory, and let it quiz you on a topic and grade your answer.",
            "Add one 'wow' feature (e.g. it tracks which topics you get wrong and drills those more).",
        ],
        "checkpoints": [
            "Which single technique from this course does your tutor lean on most, and why?",
            "How would you evaluate whether the tutor is actually helping you learn?",
        ],
    },
]
