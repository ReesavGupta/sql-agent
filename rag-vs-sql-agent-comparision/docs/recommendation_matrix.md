# Recommendation Matrix: RAG vs SQL Agent

| Query Type | RAG | SQL Agent | Notes |
|------------|-----|-----------|-------|
| Simple SELECT (e.g., "List all products in stock") | ✅ Good | ✅ Good | Both systems return correct results |
| Requires JOIN or aggregation | ❌ Limited | ✅ Good | RAG often fails if schema context is missing or not retrieved |
| Schema not in vector store | ❌ Fails | ✅ Good | RAG cannot answer, SQL Agent can if schema is present |
| Requires post-processing (e.g., top-N) | ❌/Partial | ✅ Good | RAG may not generate correct SQL, SQL Agent does |
| Natural language explanation | ✅ Good | ✅/Partial | RAG provides more verbose explanations, SQL Agent is more direct |
| Missing schema columns | ❌ Fails | ❌ Fails | Both fail, but SQL Agent gives more actionable error |
