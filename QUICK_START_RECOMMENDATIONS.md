# Quick Start Guide - Smart Recommendations

## 🚀 Getting Started

### 1. Install Dependencies (if not already done)

```bash
pip install -r requirements.txt
```

### 2. Start the Server

```bash
python main.py
```

The server will start at `http://localhost:8000`

### 3. Open the Web UI

Navigate to: `http://localhost:8000/static/index.html`

## 💬 Try the Recommendation Feature

### Example Conversations

#### Health Insurance

```
You: "I'm looking for health insurance"
Bot: [Asks about age, employment, family size, etc.]
You: [Answer each question]
Bot: [Provides 3 personalized recommendations with match scores]
```

#### Quick Triggers

These phrases will start the recommendation flow:

- "recommend health insurance"
- "which life insurance should I get?"
- "help me choose auto insurance"
- "I need home insurance recommendations"
- "suggest a plan for me"
- "what's best for my situation?"

## 🧪 Test Examples

### Health Insurance (Young Professional)

1. Say: "recommend health insurance"
2. Answer:
   - Age: 28
   - Employment: employed
   - Family size: 1
   - Pre-existing conditions: no
   - Budget: 300
   - Preference: low_cost

**Expected**: Basic Health Plan (high match score)

### Life Insurance (Family Person)

1. Say: "which life insurance is best for me?"
2. Answer:
   - Age: 35
   - Dependents: 2
   - Annual income: 80000
   - Existing coverage: no
   - Health: good
   - Goal: income_replacement

**Expected**: Family Protection Plan or Premium Whole Life

### Auto Insurance (Multi-Vehicle)

1. Say: "help me choose auto insurance"
2. Answer:
   - Age: 40
   - Driving experience: 22 years
   - Violations: none
   - Vehicles: 3
   - Vehicle age: 4-7 years
   - Value: 25000
   - Coverage: full_coverage

**Expected**: Family Auto Bundle (top recommendation)

### Home Insurance (Luxury)

1. Say: "I need home insurance"
2. Answer:
   - Property type: estate
   - Age: 5 years
   - Value: 2000000
   - High risk area: no
   - Mortgage: no
   - Contents value: 500000

**Expected**: Luxury Estate Protection

## 🔍 Verify It's Working

### Check Database

```bash
# After running some recommendations
sqlite3 insurance_assistant.db "SELECT * FROM recommendations;"
```

### View API Response

```bash
curl -X POST http://localhost:8000/api/v1/chat \
  -H 'Content-Type: application/json' \
  -d '{
    "message": "recommend health insurance",
    "session_id": "test123"
  }'
```

### Get Recommendation History

```bash
curl http://localhost:8000/api/v1/recommendations/test123
```

## 🎯 What to Look For

### ✅ Success Indicators

1. **Question Format**

   - You should see "📋 Question X of Y"
   - Clear options for choice questions
   - Range hints for number questions

2. **Recommendations Display**

   - Medal emojis (🥇🥈🥉) for top 3
   - Match percentage badges
   - "Why this is a good fit" section
   - Key features listed

3. **Data Persistence**
   - Answers remembered during conversation
   - Can view history via API
   - Session maintained across messages

### 🐛 Troubleshooting

**Q: Bot doesn't start asking questions**

- Make sure you use trigger words like "recommend", "suggest", "which", "help me choose"
- Try: "I'm looking for [insurance type]"

**Q: "Invalid answer" message**

- Check the accepted values shown in the question
- For numbers, stay within the shown range
- For choices, pick exactly one of the options

**Q: No recommendations returned**

- Verify your age is within product eligibility
- Check if budget/requirements are reasonable
- Try adjusting some answers

**Q: Server won't start**

- Run: `pip install -r requirements.txt`
- Check port 8000 is not in use: `lsof -i :8000`
- Look at terminal for error messages

## 📊 Testing the Recommendation Engine

### Run Automated Tests

```bash
pytest tests/test_recommendations.py -v
```

You should see **24 tests pass** ✅

### Manual Testing Checklist

- [ ] Trigger recommendation flow with different phrases
- [ ] Complete full questionnaire for each insurance type
- [ ] Test invalid answers (wrong age, invalid choice)
- [ ] View formatted recommendations in UI
- [ ] Check match percentages make sense
- [ ] Verify reasons are relevant to answers
- [ ] Test with different customer profiles
- [ ] Check session persistence across messages

## 🎓 Learning More

- Full documentation: `SMART_RECOMMENDATIONS_FEATURE.md`
- Product catalog: `data/product_catalog.py`
- Recommendation logic: `app/services/recommendation_service.py`
- API docs: http://localhost:8000/docs (when server running)

## 💡 Tips

1. **Be Specific**: The more detail in your answers, the better the recommendations
2. **Try Different Profiles**: Test with young/old, single/family, low/high budget
3. **Check Reasoning**: The "why this is good" section explains the scoring
4. **Save Sessions**: Use the same session_id to maintain history
5. **Provide Feedback**: Use the feedback API to mark accepted/rejected recommendations

---

**Ready to try it?** Start the server and say: _"I'm looking for health insurance"_ 🎉
