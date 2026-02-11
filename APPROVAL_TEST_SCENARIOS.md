# 🎯 Loan Approval Test Scenarios

## The Problem (Fixed!)

The original logic was **way too strict**:
- Required monthly income to be 2x the TOTAL loan amount
- For a $50,000 loan, you'd need $100,000/month income!

## The Fix

Changed to **realistic industry standards**:
- Annual income should be 2.5x the loan amount
- Loan amount should not exceed 40% of annual income
- Credit score 650+ is acceptable (medium or low risk)
- Disposable income must be positive (income > expenses)

---

## ✅ Scenario 1: STRONG APPROVAL (High Confidence)

**Profile**: High earner with excellent credit

```
Applicant ID: APPROVE001
Name: Sarah Johnson
Loan Amount: 30000
Monthly Income: 8000
Monthly Expenses: 3000
```

**Why it works**:
- Annual income: $96,000
- Income to loan ratio: 96,000 / 30,000 = 3.2x ✅ (> 2.5x required)
- Disposable income: $5,000/month ✅
- Credit score: 650-798 (medium to low risk) ✅
- **Expected: APPROVE with HIGH confidence**

---

## ✅ Scenario 2: MODERATE APPROVAL (Medium Confidence)

**Profile**: Average earner, borderline case

```
Applicant ID: APPROVE002
Name: Michael Chen
Loan Amount: 40000
Monthly Income: 9000
Monthly Expenses: 4000
```

**Why it works**:
- Annual income: $108,000
- Income to loan ratio: 108,000 / 40,000 = 2.7x ✅ (> 2.5x required)
- Disposable income: $5,000/month ✅
- Credit score: 650-798 (medium to low risk) ✅
- **Expected: APPROVE or REVIEW**

---

## ✅ Scenario 3: IDEAL CANDIDATE

**Profile**: Perfect applicant

```
Applicant ID: APPROVE003
Name: Emily Rodriguez
Loan Amount: 25000
Monthly Income: 10000
Monthly Expenses: 2500
```

**Why it works**:
- Annual income: $120,000
- Income to loan ratio: 120,000 / 25,000 = 4.8x ✅ (well above 2.5x)
- Disposable income: $7,500/month ✅
- Credit score: 650-798 (medium to low risk) ✅
- **Expected: APPROVE with HIGH confidence**

---

## ❌ Scenario 4: REJECTION (Too Much Loan)

**Profile**: Loan too large for income

```
Applicant ID: REJECT001
Name: John Smith
Loan Amount: 80000
Monthly Income: 6000
Monthly Expenses: 3000
```

**Why it fails**:
- Annual income: $72,000
- Income to loan ratio: 72,000 / 80,000 = 0.9x ❌ (< 2.5x required)
- Loan is 111% of annual income (way over 40% limit)
- **Expected: REJECT**

---

## ❌ Scenario 5: REJECTION (High Expenses)

**Profile**: Income too low after expenses

```
Applicant ID: REJECT002
Name: David Lee
Loan Amount: 50000
Monthly Income: 7000
Monthly Expenses: 6500
```

**Why it fails**:
- Annual income: $84,000
- Income to loan ratio: 84,000 / 50,000 = 1.68x ❌ (< 2.5x required)
- Disposable income: $500/month (too tight)
- **Expected: REJECT**

---

## 🔄 Scenario 6: REVIEW (Borderline)

**Profile**: Right on the edge

```
Applicant ID: REVIEW001
Name: Lisa Wang
Loan Amount: 45000
Monthly Income: 9500
Monthly Expenses: 5000
```

**Why it's borderline**:
- Annual income: $114,000
- Income to loan ratio: 114,000 / 45,000 = 2.53x ⚠️ (just above 2.5x)
- Disposable income: $4,500/month ✅
- Credit score: varies (could be medium risk)
- **Expected: REVIEW or APPROVE**

---

## 📊 Quick Reference: Approval Criteria

| Criteria | Requirement | Weight |
|----------|-------------|--------|
| **Credit Score** | 650+ (medium or low risk) | HIGH |
| **Income to Loan Ratio** | Annual income ≥ 2.5x loan | HIGH |
| **Disposable Income** | Income > Expenses | MEDIUM |
| **Loan to Income %** | Loan ≤ 40% of annual income | HIGH |

---

## 🧪 How to Test

1. Go to http://localhost:3000
2. Click "Submit Application" tab
3. Enter one of the scenarios above
4. Click "Submit Application"
5. Copy the Workflow ID
6. Go to "Review Loan" tab
7. Paste the Workflow ID and click "Fetch Details"
8. Check the AI recommendation!

---

## 💡 Tips

- **Credit scores are random** from Mockoon (640-798), so results may vary slightly
- **Try Scenario 3 first** - it's the most likely to approve
- If you still get rejections, the AI might be adding additional reasoning
- Check the "AI Analysis Summary" to see the detailed reasoning

---

## 🔧 What Was Changed

**File**: `backend/classes/agents/bedrock_agent.py`

**Changes**:
1. Changed income calculation from monthly to annual
2. Changed ratio requirement from 2.0x to 2.5x
3. Updated system prompt with realistic criteria
4. Added annual_income to the response

**Before**:
```python
income_ratio = income / amount  # Monthly income vs total loan
affordability_ok = income_ratio >= 2.0  # Impossible!
```

**After**:
```python
annual_income = income * 12
income_ratio = annual_income / amount  # Annual income vs loan
affordability_ok = income_ratio >= 2.5  # Realistic!
```

---

**Now try Scenario 1 or 3 - you should get an APPROVAL!** 🎉
