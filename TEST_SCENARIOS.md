# 🧪 Test Scenarios - Approval & Rejection Cases

## Quick Reference Guide for Testing

Use these exact values to test different outcomes!

---

## ✅ APPROVAL SCENARIOS

### Scenario 1: Strong Approval (High Confidence)
**Profile**: High earner with excellent financials

```
Applicant ID: APPROVE001
Name: Sarah Johnson
Loan Amount: 30000
Monthly Income: 8000
Monthly Expenses: 3000
```

**Why it approves:**
- Annual income: $96,000
- Income-to-loan ratio: 3.2x ✅ (> 2.5x required)
- Disposable income: $5,000/month ✅
- Credit score: 650-798 (random from Mockoon) ✅

**Expected Result:** ✅ **APPROVE** with HIGH confidence

---

### Scenario 2: Moderate Approval
**Profile**: Average earner, good financials

```
Applicant ID: APPROVE002
Name: Michael Chen
Loan Amount: 25000
Monthly Income: 7000
Monthly Expenses: 2500
```

**Why it approves:**
- Annual income: $84,000
- Income-to-loan ratio: 3.36x ✅ (> 2.5x required)
- Disposable income: $4,500/month ✅
- Credit score: 650-798 ✅

**Expected Result:** ✅ **APPROVE** with MEDIUM-HIGH confidence

---

### Scenario 3: Perfect Candidate
**Profile**: Ideal applicant

```
Applicant ID: APPROVE003
Name: Emily Rodriguez
Loan Amount: 20000
Monthly Income: 10000
Monthly Expenses: 2000
```

**Why it approves:**
- Annual income: $120,000
- Income-to-loan ratio: 6.0x ✅ (well above 2.5x)
- Disposable income: $8,000/month ✅
- Credit score: 650-798 ✅

**Expected Result:** ✅ **APPROVE** with HIGH confidence

---

### Scenario 4: Borderline Approval
**Profile**: Just meets requirements

```
Applicant ID: APPROVE004
Name: David Kim
Loan Amount: 35000
Monthly Income: 7500
Monthly Expenses: 3000
```

**Why it approves:**
- Annual income: $90,000
- Income-to-loan ratio: 2.57x ✅ (just above 2.5x)
- Disposable income: $4,500/month ✅
- Credit score: 650-798 ✅

**Expected Result:** ✅ **APPROVE** or **REVIEW** (borderline)

---

## ❌ REJECTION SCENARIOS

### Scenario 5: Loan Too Large
**Profile**: Loan exceeds income capacity

```
Applicant ID: REJECT001
Name: John Smith
Loan Amount: 80000
Monthly Income: 6000
Monthly Expenses: 3000
```

**Why it rejects:**
- Annual income: $72,000
- Income-to-loan ratio: 0.9x ❌ (< 2.5x required)
- Loan is 111% of annual income ❌
- Disposable income: $3,000/month (but ratio fails)

**Expected Result:** ❌ **REJECT** with HIGH confidence

---

### Scenario 6: High Expenses
**Profile**: Income too low after expenses

```
Applicant ID: REJECT002
Name: Lisa Wang
Loan Amount: 50000
Monthly Income: 7000
Monthly Expenses: 6500
```

**Why it rejects:**
- Annual income: $84,000
- Income-to-loan ratio: 1.68x ❌ (< 2.5x required)
- Disposable income: $500/month ❌ (too tight)
- High expense ratio

**Expected Result:** ❌ **REJECT** with HIGH confidence

---

### Scenario 7: Insufficient Income
**Profile**: Income doesn't support loan

```
Applicant ID: REJECT003
Name: Robert Taylor
Loan Amount: 60000
Monthly Income: 5000
Monthly Expenses: 2500
```

**Why it rejects:**
- Annual income: $60,000
- Income-to-loan ratio: 1.0x ❌ (< 2.5x required)
- Loan equals entire annual income ❌
- Disposable income: $2,500/month (but ratio fails)

**Expected Result:** ❌ **REJECT** with HIGH confidence

---

### Scenario 8: Negative Cash Flow
**Profile**: Expenses exceed income

```
Applicant ID: REJECT004
Name: Amanda Brown
Loan Amount: 40000
Monthly Income: 5000
Monthly Expenses: 5500
```

**Why it rejects:**
- Annual income: $60,000
- Income-to-loan ratio: 1.5x ❌ (< 2.5x required)
- Disposable income: -$500/month ❌ (negative!)
- Cannot afford current expenses

**Expected Result:** ❌ **REJECT** with HIGH confidence

---

## 🔄 REVIEW SCENARIOS (Manual Decision Needed)

### Scenario 9: Borderline Case
**Profile**: Mixed signals

```
Applicant ID: REVIEW001
Name: James Wilson
Loan Amount: 45000
Monthly Income: 9500
Monthly Expenses: 5000
```

**Why it needs review:**
- Annual income: $114,000
- Income-to-loan ratio: 2.53x ⚠️ (just above 2.5x)
- Disposable income: $4,500/month ✅
- Credit score: varies (could be medium risk)

**Expected Result:** ⚠️ **REVIEW** or **APPROVE** (depends on credit score)

---

### Scenario 10: High Loan, High Income
**Profile**: Large amounts, needs verification

```
Applicant ID: REVIEW002
Name: Patricia Martinez
Loan Amount: 75000
Monthly Income: 16000
Monthly Expenses: 4000
```

**Why it needs review:**
- Annual income: $192,000
- Income-to-loan ratio: 2.56x ⚠️ (just above 2.5x)
- Disposable income: $12,000/month ✅
- Large amounts need verification

**Expected Result:** ⚠️ **REVIEW** or **APPROVE**

---

## 📊 Quick Comparison Table

| Scenario | Applicant | Loan | Income | Expenses | Ratio | Expected |
|----------|-----------|------|--------|----------|-------|----------|
| **1** | Sarah Johnson | $30K | $8K | $3K | 3.2x | ✅ APPROVE |
| **2** | Michael Chen | $25K | $7K | $2.5K | 3.36x | ✅ APPROVE |
| **3** | Emily Rodriguez | $20K | $10K | $2K | 6.0x | ✅ APPROVE |
| **4** | David Kim | $35K | $7.5K | $3K | 2.57x | ✅ APPROVE |
| **5** | John Smith | $80K | $6K | $3K | 0.9x | ❌ REJECT |
| **6** | Lisa Wang | $50K | $7K | $6.5K | 1.68x | ❌ REJECT |
| **7** | Robert Taylor | $60K | $5K | $2.5K | 1.0x | ❌ REJECT |
| **8** | Amanda Brown | $40K | $5K | $5.5K | 1.5x | ❌ REJECT |
| **9** | James Wilson | $45K | $9.5K | $5K | 2.53x | ⚠️ REVIEW |
| **10** | Patricia Martinez | $75K | $16K | $4K | 2.56x | ⚠️ REVIEW |

---

## 🎯 Testing Instructions

### Step 1: Open the Application
```
http://localhost:3000
```

### Step 2: Submit an Application
1. Click **"Submit Application"** tab
2. Copy one of the scenarios above
3. Fill in the form
4. Click **"Submit Application"** (emerald button!)
5. **Copy the Workflow ID**

### Step 3: Wait for Processing
- Wait 10-15 seconds for AI processing
- Or check Temporal UI: http://localhost:8233

### Step 4: Review the Result
1. Click **"Review Loan"** tab
2. Paste the **Workflow ID**
3. Click **"Fetch Details"**
4. See the AI analysis!

### Step 5: Export Report (New Feature!)
1. Click **"📄 Export Report"** button
2. Check your downloads folder
3. Open the text file to see full report

### Step 6: Make Your Decision
1. Review the AI recommendation
2. Click **"Approve"** or **"Reject"**
3. See the confirmation!

---

## 🧪 Recommended Testing Order

### Quick Test (5 minutes):
1. ✅ **Scenario 3** (Perfect - should approve)
2. ❌ **Scenario 5** (Too large - should reject)

### Full Test (15 minutes):
1. ✅ **Scenario 1** (Strong approval)
2. ✅ **Scenario 3** (Perfect approval)
3. ❌ **Scenario 5** (Loan too large)
4. ❌ **Scenario 6** (High expenses)
5. ⚠️ **Scenario 9** (Borderline review)

### Complete Test (30 minutes):
- Test all 10 scenarios
- Export reports for each
- Compare AI reasoning
- Check approval rates in stats API

---

## 📈 Expected Results Summary

### Approval Rate:
- **Scenarios 1-4**: Should approve (4/10 = 40%)
- **Scenarios 5-8**: Should reject (4/10 = 40%)
- **Scenarios 9-10**: May vary (2/10 = 20%)

### AI Confidence:
- **High confidence**: Clear approve/reject cases
- **Medium confidence**: Borderline cases
- **Low confidence**: Edge cases needing review

---

## 🎨 Visual Indicators

### In the UI:
- ✅ **Green** = Approved
- ❌ **Red** = Rejected
- ⚠️ **Yellow** = Review needed
- 🔵 **Teal** = Processing

### In the Report:
- **Decision**: APPROVE/REJECT/REVIEW
- **Confidence**: HIGH/MEDIUM/LOW
- **Reasoning**: Detailed explanation

---

## 💡 Pro Tips

### For Best Results:
1. ✅ Test approval cases first (builds confidence)
2. ❌ Then test rejection cases (shows it works)
3. ⚠️ Finally test borderline cases (shows intelligence)

### For Screenshots:
1. 📸 Capture the new emerald/teal theme
2. 📸 Show an approval with green indicators
3. 📸 Show a rejection with red indicators
4. 📸 Show the export report feature

### For Demos:
1. 🎯 Start with Scenario 3 (perfect approval)
2. 🎯 Show Scenario 5 (clear rejection)
3. 🎯 Demonstrate export feature
4. 🎯 Show statistics API

---

## 🔍 What to Look For

### In AI Analysis:
- ✅ Income-to-loan ratio calculation
- ✅ Disposable income assessment
- ✅ Credit score evaluation
- ✅ Clear reasoning provided

### In Your Report:
- ✅ All applicant details
- ✅ AI assessments for each category
- ✅ Final recommendation
- ✅ Timestamp and workflow ID

### In Statistics:
```bash
curl http://localhost:8000/stats
```
- ✅ Total applications count
- ✅ Approval rate percentage
- ✅ Your name in system_info!

---

## 🎉 Success Criteria

Your system is working perfectly if:
- ✅ Scenarios 1-4 get approved
- ❌ Scenarios 5-8 get rejected
- ⚠️ Scenarios 9-10 show thoughtful analysis
- 📄 Export button downloads reports
- 🎨 UI shows emerald/teal theme
- 📊 Stats API returns your name

---

**Ready to test? Start with Scenario 3 (Perfect Candidate)!** 🚀

**Developed by Norvin Samson Anthony**
