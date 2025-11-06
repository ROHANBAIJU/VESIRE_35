# 🧪 Quick Testing Guide

## Prerequisites
1. ✅ Backend running on `http://192.168.43.46:5000`
2. ✅ Flutter app configured with correct API URL
3. ✅ Physical device or emulator with camera permissions

---

## Step-by-Step Testing

### 1. Test Bounding Box Rendering
```
1. Open the app
2. Login/Skip to home
3. Tap "Scan" button
4. Position plant in camera frame
5. Tap capture button
6. ✓ EXPECT: Green bounding boxes around detected diseases
7. ✓ EXPECT: Disease name + confidence % label on each box
```

**Success Criteria:**
- Bright green boxes (#00FF00) visible
- Labels readable with black text on green background
- Boxes align with detected disease areas

---

### 2. Test Online/Offline RAG Indication
```
## Test Online Mode (with Internet):
1. Ensure device has internet connection
2. Scan a plant
3. Wait for diagnosis to load
4. ✓ EXPECT: Purple badge showing "🌐 Online AI (Gemini)"
5. ✓ EXPECT: Detailed, formatted diagnosis text

## Test Offline Mode (without Internet):
1. Turn off WiFi/Mobile data
2. Scan same plant again (or any plant)
3. ✓ EXPECT: Blue badge "💾 Cached Data" OR Grey badge "📱 Offline Data"
4. ✓ EXPECT: Diagnosis still appears (from cache)
```

**Success Criteria:**
- Source badge visible at top of diagnosis
- Correct badge color and icon for each mode
- Smooth fallback to offline data

---

### 3. Test Language-Specific Responses
```
## English Test:
1. Go to Settings
2. Select "English"
3. Scan a plant
4. ✓ EXPECT: All diagnosis text in English

## Hindi Test:
1. Go to Settings  
2. Select "हिंदी" (Hindi)
3. Scan a plant
4. ✓ EXPECT: Description, symptoms, treatment in Hindi
5. ✓ EXPECT: UI labels also in Hindi

## Kannada Test:
1. Go to Settings
2. Select "ಕನ್ನಡ" (Kannada)
3. Scan a plant
4. ✓ EXPECT: All content in Kannada
```

**Success Criteria:**
- Gemini generates response in selected language
- Plant disease names may stay in English (scientific)
- All descriptions and recommendations in target language

---

### 4. Test Markdown Formatting
```
1. Scan any plant (with internet for best results)
2. Read the diagnosis description
3. ✓ EXPECT: Key words in bold:
   - Disease names
   - Affected plant parts (leaves, stems, etc.)
   - Treatment actions (spray, remove, apply)
4. Check symptoms section
5. ✓ EXPECT: Important terms highlighted in bold
```

**Success Criteria:**
- Bold text clearly visible (darker/thicker font)
- Doesn't show literal **markdown** syntax
- Improves readability

---

### 5. Test 4-Point Care Recommendations
```
1. Scan a plant (online mode preferred)
2. Scroll to "🤖 AI Care Recommendations" section
3. Count the bullet points
4. ✓ EXPECT: EXACTLY 4 care recommendations
5. ✓ EXPECT: Purple background section
6. ✓ EXPECT: Purple bullet points
```

**Success Criteria:**
- Always 4 points (not 3, not 5)
- Each recommendation actionable and clear
- Special AI section styling (purple theme)

---

### 6. Test Analytics Screen Integration
```
1. Complete at least one plant scan
2. Navigate to Analytics tab
3. ✓ EXPECT: Loading indicator briefly appears
4. ✓ EXPECT: Last scanned plant info displayed:
   - Plant name from detection
   - Scan timestamp (e.g., "Nov 6, 2:30 PM")
   - Scientific name if available
5. Check AI Confidence Score card
6. ✓ EXPECT: Shows actual confidence % from last detection
7. Check AI Analysis section
8. ✓ EXPECT: Shows diagnosis description with markdown formatting
9. Check Health Pie Chart
10. ✓ EXPECT: Percentages calculated from detection history
11. Pull down to refresh
12. ✓ EXPECT: Data reloads with animation
```

**Success Criteria:**
- Real data matches last scan
- No mock/placeholder data visible
- Confidence score accurate
- Health percentages meaningful

---

### 7. Test Health Metrics Calculation
```
1. Perform 3-4 plant scans (healthy and diseased)
2. Go to Analytics tab
3. Check "Plant Health Status" pie chart
4. ✓ EXPECT: Healthy % + Unhealthy % = 100%
5. ✓ EXPECT: Disease Risk matches detection patterns
6. Check color coding:
   - Green: Low risk (<20%)
   - Orange: Medium risk (20-50%)
   - Red: High risk (>50%)
```

**Success Criteria:**
- Percentages change with new scans
- Reflects actual detection confidence
- Color indicators accurate

---

## Common Issues & Solutions

### Issue: Bounding boxes not showing
**Check:**
- Backend actually returned detections? (Check API response)
- Image dimensions being calculated? (Check console logs)
- Boxes might be off-screen? (Try different image angles)

### Issue: Always showing "Offline" mode
**Check:**
- Device has internet connectivity
- Backend can reach Gemini API
- `USE_ONLINE_RAG=True` in backend .env
- `GEMINI_API_KEY` is valid

### Issue: English responses despite language change
**Check:**
- Language provider updated? (Restart app)
- Backend receiving language parameter? (Check API logs)
- Gemini prompt includes language instruction? (Check backend code)

### Issue: Analytics shows "No Data Yet"
**Check:**
- At least one scan completed with `saveHistory=false` changed to `true`
- User ID matches between scans and analytics
- Backend /history endpoint working? (Test in browser)

### Issue: Markdown **text** showing literally
**Check:**
- MarkdownText widget being used (not regular Text widget)
- Widget imported correctly

---

## Quick Verification Checklist

Before considering testing complete:

- [ ] Bounding boxes visible and accurate ✅
- [ ] Confidence scores shown on boxes ✅
- [ ] Online mode shows purple "Online AI" badge ✅
- [ ] Offline mode shows blue/grey badge ✅
- [ ] Language switching works (test 2+ languages) ✅
- [ ] Bold formatting visible in diagnosis ✅
- [ ] Care recommendations always 4 points ✅
- [ ] Analytics loads real detection data ✅
- [ ] AI confidence score matches last scan ✅
- [ ] Health pie chart shows calculated %s ✅
- [ ] Pull-to-refresh works in analytics ✅
- [ ] App handles no-internet gracefully ✅

---

## Performance Testing

### Loading Times
- Camera initialization: < 2 seconds
- Image capture: < 1 second
- Detection API call: < 5 seconds
- Diagnosis API call: < 10 seconds (online), < 2 seconds (cached)
- Analytics load: < 3 seconds

### Memory Usage
- Camera preview: Monitor for leaks
- Image processing: Should release after detection
- Provider states: Check with Flutter DevTools

---

## API Testing Commands

### Test backend directly:
```bash
# Health check
curl http://192.168.43.46:5000/api/health

# Diagnose (check language support)
curl "http://192.168.43.46:5000/api/diagnose/Tomato%20leaf%20late%20blight?language=hi"

# Get history
curl "http://192.168.43.46:5000/api/history/user-123?limit=10"
```

---

## Success Report Template

After testing, fill this out:

```
✅ PASSED | ❌ FAILED | ⚠️ PARTIAL

[ ] Bounding Boxes: ___
[ ] RAG Online/Offline: ___
[ ] Language Switching: ___
[ ] Markdown Formatting: ___
[ ] 4-Point Recommendations: ___
[ ] Analytics Real Data: ___
[ ] Health Pie Chart: ___

Notes: ___
```

---

## Next Steps After Testing

1. If all tests pass → Deploy to production
2. If issues found → Document and prioritize fixes
3. Performance issues → Optimize API calls / caching
4. UI/UX feedback → Iterate on design

---

🎉 **Happy Testing!**
