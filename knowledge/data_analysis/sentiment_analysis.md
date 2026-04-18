# 📈 情感分析指南 (Sentiment Analysis Guide)

## 概述

情感分析用于检测文本中的情绪倾向，帮助理解群聊氛围和成员情绪状态。

## 分析方法

### 1. 基础情绪分类
- **积极 (Positive)**: 表达喜悦、赞同、兴奋等正面情绪
- **消极 (Negative)**: 表达愤怒、失望、悲伤等负面情绪
- **中性 (Neutral)**: 客观陈述，无明显情绪倾向

### 2. 情绪强度评分
使用 0-1 的分数表示情绪强度：
- 0.0-0.3: 弱情绪
- 0.3-0.7: 中等情绪
- 0.7-1.0: 强烈情绪

### 3. 应用场景

#### 群聊氛围监控
```python
# 伪代码示例
def analyze_chat_mood(messages):
    positive_count = 0
    negative_count = 0
    for msg in messages:
        sentiment = get_sentiment(msg)
        if sentiment > 0:
            positive_count += 1
        elif sentiment < 0:
            negative_count += 1
    
    if positive_count > negative_count * 2:
        return "欢乐和谐 😊"
    elif negative_count > positive_count:
        return "紧张需要关注 ⚠️"
    else:
        return "平静正常 🙂"
```

#### 情绪变化追踪
- 记录每个时间段的情绪分布
- 识别情绪转折点
- 关联特定事件与情绪变化

## 注意事项

1. **上下文理解**: 同一句话在不同语境下可能有不同情绪
2. **讽刺检测**: 注意识别反讽和黑色幽默
3. **文化差异**: 不同文化背景的表达方式可能不同

## 工具推荐

- Python: `textblob`, `vaderSentiment`, `transformers`
- API: Google Cloud NLP, AWS Comprehend

---
*由 NovaMind 编写*
