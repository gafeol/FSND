# Sample curl commands:

```bash
curl -X DELETE http://localhost:5000/questions/20

curl -X POST http://localhost:5000/questions -d '{"question": "a", "answer": "b", "difficulty": 1, "category": 2}' -H "Content-Type: application/json"
```