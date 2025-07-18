# Benchmarking Results: RAG vs SQL Agent

| # | Query | RAG Output | SQL Agent Output | Correct? | Notes |
|---|-------|------------|-----------------|----------|-------|
| 1 | List all products that are currently in stock | Correct SQL & results | Correct JSON result | ✅ | Both correct |
| 2 | Show all customers from 'sao paulo' | SQL for 'sao bernardo do campo' (context confusion) | Correct customer list for 'sao paulo' | ❌/✅ | RAG context confusion |
| 3 | List all reviews with a score of 5 | Correct SQL & results | Correct JSON result | ✅ | Both correct |
| 4 | Show the most recent order for customer_id ... | Correct SQL & result | Correct summary | ✅ | Both correct |
| 5 | What is the average order value for customers in 'rio de janeiro'? | Refuses (missing schema) | Refuses (missing column) | ❌ | Both limited by schema |
| 6 | Show the top 5 products by number of orders | Refuses (missing schema) | Refuses (missing column) | ❌ | Both limited by schema |
| 7 | Which city has the highest number of delivered orders? | Refuses (missing schema) | Refuses (missing column) | ❌ | Both limited by schema |
| 8 | Find the top 3 customers by total order value | Correct SQL & results | Refuses (missing column) | ✅/❌ | SQL Agent limited by schema |
| 9 | Which customers have not placed any orders? | Refuses (missing schema) | Returns list of customers | ❌/✅ | RAG limited by schema |
| 10 | What is the total revenue from orders with a 5-star review? | Refuses (missing schema) | Refuses (missing column) | ❌ | Both limited by schema |
