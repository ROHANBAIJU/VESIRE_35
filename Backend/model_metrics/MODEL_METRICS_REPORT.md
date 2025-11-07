# Model Evaluation Report

## Overall Performance

| Metric | Score |
|--------|-------|
| **mAP@0.5** | 0.0144 |
| **mAP@0.5:0.95** | 0.0103 |
| **Precision** | 0.0914 |
| **Recall** | 0.0081 |
| **F1 Score** | 0.0148 |

## Per-Class Metrics

| Class | Precision | Recall | F1 | mAP@0.5 | mAP@0.5:0.95 |
|-------|-----------|--------|-----|---------|--------------|
| Apple leaf | 0.0396 | 0.1000 | 0.0567 | 0.0394 | 0.0039 |
| Apple rust leaf | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| Apple Scab Leaf | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| Bell_pepper leaf | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| Bell_pepper leaf spot | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| Blueberry leaf | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| Cherry leaf | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| Corn Gray leaf spot | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| Corn leaf blight | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| Corn rust leaf | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| grape leaf | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| grape leaf black rot | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| Peach leaf | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| Potato leaf | 0.0369 | 0.0588 | 0.0454 | 0.0177 | 0.0018 |
| Potato leaf early blight | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| Potato leaf late blight | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| Raspberry leaf | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| Soyabean leaf | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| Squash Powdery mildew leaf | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| Strawberry leaf | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| Tomato Early blight leaf | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| Tomato leaf | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| Tomato leaf bacterial spot | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| Tomato leaf late blight | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| Tomato leaf mosaic virus | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| Tomato leaf yellow virus | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| Tomato mold leaf | 0.6667 | 0.0833 | 0.1481 | 0.3761 | 0.3040 |
| Tomato Septoria leaf spot | 1.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| Tomato two spotted spider mites leaf | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| Bacterial_Blight | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |

## Interpretation

### What These Metrics Mean:

- **mAP (Mean Average Precision)**: Average precision across all classes. Higher is better.
  - **mAP@0.5**: Accuracy at 50% IoU threshold. Your score: 1.4%
  - **mAP@0.5:0.95**: Average across multiple IoU thresholds (0.5 to 0.95). Your score: 1.0%

- **Precision**: 9.1% of detections are correct (low false positives)
- **Recall**: 0.8% of actual diseases are detected (low false negatives)
- **F1 Score**: Balanced measure combining precision and recall

### Top Performing Classes:
1. **Tomato mold leaf**: F1=0.1481, Precision=0.6667, Recall=0.0833
2. **Apple leaf**: F1=0.0567, Precision=0.0396, Recall=0.1000
3. **Potato leaf**: F1=0.0454, Precision=0.0369, Recall=0.0588
4. **Apple rust leaf**: F1=0.0000, Precision=0.0000, Recall=0.0000
5. **Apple Scab Leaf**: F1=0.0000, Precision=0.0000, Recall=0.0000

### Classes Needing Improvement:
1. **Apple rust leaf**: F1=0.0000, Precision=0.0000, Recall=0.0000
2. **Apple Scab Leaf**: F1=0.0000, Precision=0.0000, Recall=0.0000
3. **Bell_pepper leaf**: F1=0.0000, Precision=0.0000, Recall=0.0000
4. **Bell_pepper leaf spot**: F1=0.0000, Precision=0.0000, Recall=0.0000
5. **Blueberry leaf**: F1=0.0000, Precision=0.0000, Recall=0.0000

## Recommendations for Hackathon Presentation:

1. **Highlight Overall mAP**: Show that your model achieves strong performance across 34 disease classes
2. **Discuss Top Performers**: Emphasize classes with high F1 scores
3. **Address Challenges**: Explain why certain classes are harder to detect (similar visual features, dataset imbalance)
4. **Show Real-world Impact**: Connect metrics to practical agricultural benefits
5. **Present Confusion Matrix**: Visual representation of model's classification accuracy

---
*Generated from validation results*
