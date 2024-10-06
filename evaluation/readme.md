evaluation files for evaluating retrieval and RAG performance


Relevant part of the main README:



### ✅ Create Ground Truth data
*files: `./evaluation/ground_truth_data.ipynb`*

To evaluate retrieval & our query answers, we need some "ground truth" that we base our scores on. The ground truth consists of alternative questions that could be asked for the same answer.

### 📈 Evaluating Retrieval
*files: `./evaluation/evaluate-test.ipynb`, `./evaluation/evaluate-vector.ipynb`*

As a baseline, retrieval from text-based search was evaluated using hit rate and MRR.

**Hit rate** is a sort of a success score. It tells how often the chatbot finds a relevant answer from the FAQs when a user asks a question. A higher hit rate means the chatbot is doing a good job of retrieving the right answers.

**MRR (Mean Reciprocal Rank)** is a way to measure not just if the chatbot found a correct answer based on a user query, but also how much "on top" the correct answer was ranked. In my case, MRR (Mean Reciprocal Rank) measures how well the chatbot retrieves the right answers from the FAQs based on alternative ways of asking the same question. After generating similar questions, the chatbot searches for the best matches in our documents using ElasticSearch, and the top 5 results are ranked. MRR checks how high the correct document (question-answer-pair which the "alternative question" was based on) appears in those rankings—the sooner it shows up (like in the first or second position), the better the score. This way, you can tell how effectively the chatbot finds the right information, even with different ways of asking the question.

- Retrieval evaluation

  - for each record (Answer) in the FAQ, generate 5 questions which possibly address this answer.
  - Next, we input the questions into our search function to see if the desired answer would actually be among our top results
  - Use scoring algorithms to get an objective measure of retrieval quality
  - Caveat: We did not verify that the questions are actually valid, since we created the "ground truth" using an LLM. So we also have a bias due to inaccurate ground truth data, and what we measure might also reflect these inaccuracies during ground truth creation.

### 📊 Evaluating the RAG
*files: `./evaluation/offline-rag-evaluation.ipynb`

In this step, I generated answers based on the "ground truth" dataset, which consists of alternative ways of answering a question.

The goal was to see whether my RAG answers questions correctly if the questions are formulated in a different way.

We can compare the given answers to our alternative questions with the original answers in our dataset by using cosine similarity

<figure>
  <img src="assets/cosine-evaluation.png" alt="Monitoring data in the postgres database">
  <figcaption><em>Fig. 3: Monitoring data in the postgres database</em></figcaption>
</figure>
<br><br>

...or by using LLM-as-a-judge:

```
You are an expert evaluator for a Retrieval-Augmented Generation (RAG) system.
Your task is to analyze the relevance of the generated answer compared to the original answer provided.
Based on the relevance and similarity of the generated answer to the original answer, you will classify
it as "NON_RELEVANT", "PARTLY_RELEVANT", or "RELEVANT".
Please also take the generated question into account. If the generated Question is clearly not related to the original question, please classify relevance as "NA".

Here is the data for evaluation:

Original Question: {original_question}
Generated Question: {Question}
Original Answer: {answer_orig}
Generated Answer: {answer_llm}

Please analyze the content and context of the generated answer in relation to the original
answer and provide your evaluation in parsable JSON without using code blocks:

{{
  "Relevance": "NON_RELEVANT" | "PARTLY_RELEVANT" | "RELEVANT" | "NA",
  "Explanation": "[Provide a brief explanation for your evaluation]"
}}
```

<figure>
  <img src="assets/relevance.png" alt="Relevance of the given answers">
  <figcaption><em>Fig. 4: Relevance of the given answers</em></figcaption>
</figure>
<br><br>
<figure>
  <img src="assets/evaluation.drawio.png" alt="Evaluation in a chart">
  <figcaption><em>Fig. 5: Evaluation in a chart</em></figcaption>
</figure>
<br><br>
