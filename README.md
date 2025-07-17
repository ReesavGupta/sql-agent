# Quick Commerce SQL Agent

A modern price comparison and analytics platform for quick commerce apps (Blinkit, Zepto, Instamart, BigBasket Now, etc.), enabling real-time tracking of pricing, discounts, and availability across thousands of products using natural language queries.

---

## 🚀 Project Overview

This project provides:
- A robust backend SQL agent with semantic table/column selection, multi-step query planning, and real-time data simulation.
- A modern, responsive frontend (React + Tailwind) for natural language queries and interactive results.
- Modular, extensible architecture ready for large-scale, multi-platform commerce data.

---

## 🖼️ Frontend UI Preview

![Frontend Preview](/frontend/public/frontend-preview.png)

## ✨ Features & Deliverables

### 1. **Database Design**
- **Schema**: Based on the Olist dataset, extended with columns for `current_price`, `discount_percent`, and `in_stock` in the `products` table.
- **Extensible**: Modular design allows for easy addition of more tables/platforms.

### 2. **Data Integration**
- **Real-time Simulation**: Python script periodically updates prices, discounts, and stock status with dummy data to mimic real-world changes.

### 3. **SQL Agent**
- **Semantic Table/Column Selection**: Uses FAISS vector search and HuggingFace embeddings to select relevant schema parts for each query.
- **LLM-Driven Query Generation**: LLM (Groq) generates SQL using only relevant tables/columns, with prompt engineering for accuracy.
- **Multi-step Pipeline**: Query generation, execution, and answer synthesis are modular and extensible.
- **Pagination**: All queries support LIMIT/OFFSET for large result sets.
- **Caching**: In-memory caching for schema info and query results for performance.

### 4. **Performance**
- **Optimized for High-Frequency Updates**: Real-time simulation and caching ensure responsiveness.
- **Concurrent Queries**: FastAPI backend supports async requests.

### 5. **Web Interface**
- **Modern UI**: Built with React and Tailwind CSS.
- **Step-by-step Feedback**: Shows progress ("Thinking...", "Generating SQL...", etc.) for great UX.
- **Displays**: SQL query, raw SQL result (table), and LLM answer.
- **Pagination Controls**: Easily page through large result sets.

### 6. **Security**
- **CORS**: Configured for frontend-backend integration.
- **Rate Limiting**: (Can be added with FastAPI middleware if needed.)

### 7. **Documentation**
- **This README**: Explains architecture, setup, and design decisions.

---

## 🏗️ Architecture & Design Decisions

- **Modular Backend**: Separated into `services/llm.py`, `services/vectorstore.py`, `services/query.py`, and `api/` for clean, testable code.
- **Semantic Search**: FAISS + HuggingFace embeddings for fast, scalable schema/document retrieval.
- **LLM Summarization**: LLM generates human-readable schema summaries for focused, accurate SQL generation.
- **In-memory Caching**: For both schema and query results, balancing speed and simplicity.
- **Frontend/Backend Decoupling**: REST API with CORS for easy integration and future scaling.
- **Progressive UI Feedback**: Frontend shows each step of the pipeline for transparency and user trust.

---

## 🛠️ Setup & Usage

### 1. **Backend**
- **Install dependencies:**
  ```bash
  cd backend
  pip install -r requirements.txt
  pip install fastapi uvicorn faiss-cpu
  ```
- **Set environment variables:**
  - Create `.env` in `backend/` with your Groq API key and model:
    ```
    GROQ_API_KEY=your_groq_api_key
    GROQ_MODEL=llama3-8b-8192
    ```
- **Ensure database exists:**
  - Place your SQLite DB at `backend/e-commerce-data/olist.sqlite/olist.sqlite`.
  - Run the schema update and simulation scripts:
    ```bash
    python src/services/db_connection.py
    python src/services/simulate_realtime_updates.py
    ```
- **Start the API:**
  ```bash
  uvicorn src.api.main:app --reload
  ```
  - API docs: [http://localhost:8000/docs](http://localhost:8000/docs)

### 2. **Frontend**
- **Install dependencies:**
  ```bash
  cd frontend
  npm install
  # or
  yarn
  ```
- **Start the app:**
  ```bash
  npm run dev
  # or
  yarn dev
  ```
- **Open in browser:** [http://localhost:5173](http://localhost:5173)

---

## 🧑‍💻 API Usage

- **POST /query**
  - **Body:**
    ```json
    {
      "question": "Show products with more than 30% discount",
      "page": 1,
      "page_size": 10
    }
    ```
  - **Response:**
    ```json
    {
      "question": "...",
      "query": "...",
      "result": [...],
      "answer": "...",
      "page": 1,
      "page_size": 10
    }
    ```

---

## 📝 Sample Queries
- "Which app has cheapest onions right now?"
- "Show products with 30%+ discount on Blinkit"
- "Compare fruit prices between Zepto and Instamart"
- "Find best deals for ₹1000 grocery list"
- "List 10 products with their category, price, and discount"

---

## 📚 Extending & Customizing
- **Add new tables/columns**: Update the schema and rerun the vectorstore indexing.
- **Add new endpoints**: Extend `api/routes.py`.
- **Change LLM or embeddings**: Update `services/llm.py` or `services/vectorstore.py`.
- **Add rate limiting/security**: Use FastAPI middleware.

---

## 🏆 Decision Rationale
- **FAISS over SQLiteVec**: Chosen for speed, reliability, and no native extension requirement.
- **LLM Summarization**: Ensures only relevant schema is sent to the LLM, improving accuracy and reducing cost.
- **In-memory caching**: Simple, fast, and effective for development and moderate scale.
- **Modular codebase**: Enables rapid iteration and easy testing.
- **Frontend feedback**: Step-by-step UI progress for best-in-class UX.

---

## 📂 Repository Structure

```
backend/
  src/
    api/
      main.py
      routes.py
    services/
      db_connection.py
      llm.py
      query.py
      vectorstore.py
      simulate_realtime_updates.py
frontend/
  src/
    App.tsx
    ...
```

---

## 📄 License
MIT 
---

## 🙏 Acknowledgements
- [LangChain](https://github.com/langchain-ai/langchain)
- [FAISS](https://github.com/facebookresearch/faiss)
- [HuggingFace](https://huggingface.co/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Tailwind CSS](https://tailwindcss.com/) 