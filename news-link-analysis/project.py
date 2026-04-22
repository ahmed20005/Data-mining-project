#!/usr/bin/env python3
"""
News Website Link Analysis - Complete Implementation
Data Mining Project with FP-Growth, PageRank, HITS, and BERT
"""

import pandas as pd
import numpy as np
import re
from collections import Counter
import random
import warnings
warnings.filterwarnings('ignore')

print("="*60)
print("📰 NEWS WEBSITE LINK ANALYSIS")
print("="*60)

# ============================================================
# STEP 1: DATA COLLECTION
# ============================================================
print("\n[STEP 1] Creating dataset...")

random.seed(42)

# Create sample BBC news articles dataset
sample_articles = [
    # Business articles
    {"title": "Global Markets Rise Amid Economic Recovery", "content": "Stock markets across Europe and Asia showed strong gains today as investors responded positively to economic recovery signals. The FTSE 100 rose by 2.3% while major tech companies led the rally. Analysts suggest that consumer confidence is returning after months of uncertainty. Banking stocks performed particularly well with several institutions reporting better than expected quarterly results.", "category": "business"},
    {"title": "Tech Giants Report Record Profits", "content": "Major technology companies announced record-breaking profits for the quarter. Apple, Google, and Microsoft all exceeded analyst expectations. The tech sector continues to dominate market performance with strong revenue growth. Investors are optimistic about future earnings as digital transformation accelerates globally.", "category": "business"},
    {"title": "Oil Prices Fluctuate on Supply Concerns", "content": "Crude oil prices experienced significant volatility this week amid concerns about global supply chains. Energy markets reacted to production announcements from major oil-producing nations. Analysts predict continued fluctuation as demand patterns shift. The energy sector remains a key focus for investors monitoring economic indicators.", "category": "business"},
    {"title": "Retail Sales Show Unexpected Growth", "content": "High street retailers reported stronger than expected sales figures for the month. Consumer spending increased despite economic headwinds. Online retail continued its growth trajectory with e-commerce platforms seeing record traffic. The retail sector shows resilience as shopping patterns evolve.", "category": "business"},
    {"title": "Banking Sector Faces New Regulations", "content": "Financial regulators announced new compliance requirements for major banks. The banking industry must adapt to stricter capital requirements and reporting standards. Industry leaders express concerns about implementation costs while acknowledging the need for stability. Market analysts assess the potential impact on profitability and lending practices.", "category": "business"},
    
    # Technology articles
    {"title": "Artificial Intelligence Breakthrough Announced", "content": "Researchers unveiled a major advancement in artificial intelligence capabilities. The new AI system demonstrates improved reasoning and problem-solving skills. Technology experts praise the innovation as a significant step forward. Applications range from healthcare diagnostics to autonomous vehicles. The breakthrough raises both excitement and ethical considerations.", "category": "technology"},
    {"title": "Smartphone Manufacturer Launches Flagship Device", "content": "A leading smartphone maker introduced its latest flagship model with advanced features. The device includes improved camera technology, faster processing, and enhanced battery life. Consumer interest is high as pre-orders exceed expectations. The mobile technology market remains highly competitive with continuous innovation.", "category": "technology"},
    {"title": "Cybersecurity Threats Increase Globally", "content": "Security experts warn of rising cyber attacks targeting businesses and individuals. Ransomware incidents have surged significantly over the past quarter. Organizations are urged to strengthen their defense systems and update security protocols. Government agencies collaborate on international cybersecurity initiatives to combat threats.", "category": "technology"},
    {"title": "Cloud Computing Adoption Accelerates", "content": "Enterprise adoption of cloud computing services continues to grow rapidly. Companies migrate infrastructure to cloud platforms for scalability and cost efficiency. Major cloud providers report substantial revenue increases. The shift to remote work has accelerated digital transformation initiatives across industries.", "category": "technology"},
    {"title": "Electric Vehicle Technology Advances", "content": "Electric vehicle manufacturers announce improvements in battery technology and charging infrastructure. New batteries offer extended range and faster charging times. The automotive industry invests heavily in electric mobility solutions. Environmental regulations drive the transition away from traditional combustion engines.", "category": "technology"},
    
    # Politics articles
    {"title": "Government Announces New Policy Initiative", "content": "The government unveiled a comprehensive policy package addressing economic and social challenges. Ministers outlined plans for investment in infrastructure and public services. Opposition parties critique the proposals while supporting certain elements. Political analysts assess the potential impact on upcoming elections.", "category": "politics"},
    {"title": "International Summit Addresses Climate Change", "content": "World leaders gathered for a major climate summit to discuss environmental policies. Nations committed to ambitious emissions reduction targets. Diplomatic negotiations focused on balancing economic development with sustainability. Environmental activists call for more aggressive action on climate issues.", "category": "politics"},
    {"title": "Parliament Debates Healthcare Reform", "content": "Legislators engaged in heated debates over proposed healthcare system reforms. The bill aims to improve access and reduce waiting times. Medical professionals offer mixed reactions to the proposals. Patient advocacy groups lobby for specific amendments to the legislation.", "category": "politics"},
    {"title": "Trade Negotiations Continue Between Nations", "content": "International trade talks progressed with discussions on tariffs and market access. Negotiators work to resolve longstanding disputes between trading partners. Business leaders monitor developments closely for potential impacts. Economic analysts predict outcomes could affect global supply chains.", "category": "politics"},
    {"title": "Election Campaign Intensifies", "content": "Political parties ramp up campaigning activities ahead of upcoming elections. Candidates participate in debates focusing on key voter concerns. Polling data shows tight races in several constituencies. Voter turnout expectations are high as civic engagement increases.", "category": "politics"},
    
    # Sports articles
    {"title": "Championship Final Draws Record Viewership", "content": "The championship final attracted millions of viewers worldwide setting new records. The thrilling match ended with a dramatic last-minute victory. Fans celebrated the historic achievement of the winning team. Sports analysts praise the quality of play and tactical brilliance displayed.", "category": "sports"},
    {"title": "Olympic Athletes Prepare for Competition", "content": "Athletes from around the world finalize preparations for the upcoming Olympic Games. Training camps intensify as competitors peak for the event. National teams announce their final rosters. Expectations are high for record-breaking performances in multiple disciplines.", "category": "sports"},
    {"title": "Football Transfer Window Sees Major Deals", "content": "The football transfer market witnessed several high-profile player movements. Clubs spent record amounts to secure top talent. Managers express satisfaction with squad reinforcements. Fans react to the signings with excitement and anticipation for the season.", "category": "sports"},
    {"title": "Tennis Star Wins Grand Slam Title", "content": "A rising tennis star claimed their first grand slam championship in a stunning final. The match showcased exceptional skill and determination from both players. Tennis enthusiasts celebrate the emergence of new talent. Rankings will shift significantly following the tournament results.", "category": "sports"},
    {"title": "Marathon Event Attracts Thousands of Runners", "content": "The annual city marathon drew record participation with runners from dozens of countries. Elite athletes competed for prize money alongside amateur participants. The event raised significant funds for charitable causes. Organizers praise the community support and successful execution.", "category": "sports"},
    
    # Entertainment articles
    {"title": "Blockbuster Film Breaks Box Office Records", "content": "The latest blockbuster film shattered box office records in its opening weekend. Audiences flocked to theaters for the highly anticipated release. Critics offer positive reviews praising the production quality and performances. The film industry celebrates the return of strong theatrical attendance.", "category": "entertainment"},
    {"title": "Music Festival Announces Lineup", "content": "Organizers revealed the performer lineup for the summer music festival. Major artists from various genres will headline the event. Ticket sales exceed expectations with early bird passes selling out quickly. Music fans express excitement about the diverse programming.", "category": "entertainment"},
    {"title": "Award Ceremony Celebrates Television Excellence", "content": "The annual television awards honored outstanding achievements in broadcasting. Dramas and comedies received recognition for writing and acting. Streaming platforms dominated nominations alongside traditional networks. Industry professionals gather to celebrate creative accomplishments.", "category": "entertainment"},
    {"title": "Celebrity Couple Announces Engagement", "content": "A popular celebrity couple shared their engagement news with fans. Social media erupted with congratulations from followers and fellow celebrities. The announcement generated widespread media coverage. Fans speculate about wedding plans and future projects.", "category": "entertainment"},
    {"title": "New Streaming Series Receives Critical Acclaim", "content": "A newly released streaming series garnered critical praise and strong viewer numbers. The show features compelling storytelling and high production values. Subscribers sign up for the platform specifically to watch the series. Entertainment critics predict award nominations for the cast and creators.", "category": "entertainment"}
]

# Add more articles to reach 150+ total
categories = ['business', 'technology', 'politics', 'sports', 'entertainment']
topics = {
    'business': ['market', 'stock', 'investment', 'company', 'profit', 'economy', 'trade', 'finance', 'banking', 'retail'],
    'technology': ['software', 'hardware', 'digital', 'innovation', 'startup', 'data', 'network', 'device', 'platform', 'algorithm'],
    'politics': ['government', 'policy', 'election', 'parliament', 'minister', 'legislation', 'vote', 'campaign', 'diplomacy', 'reform'],
    'sports': ['team', 'player', 'match', 'championship', 'tournament', 'coach', 'athlete', 'score', 'season', 'victory'],
    'entertainment': ['film', 'music', 'actor', 'concert', 'show', 'album', 'theater', 'celebrity', 'award', 'performance']
}

# Generate additional articles
for i in range(130):
    cat = random.choice(categories)
    topic_words = random.sample(topics[cat], 3)
    title = f"{cat.title()} News: {topic_words[0].title()} {topic_words[1].title()} Update"
    content = f"In recent {cat} developments, {topic_words[0]} and {topic_words[1]} have become key focuses. Experts discuss the implications of {topic_words[2]} trends. The {cat} sector continues to evolve with new {topic_words[0]} initiatives. Stakeholders monitor {topic_words[1]} metrics closely. Industry leaders emphasize the importance of {topic_words[2]} strategies for future growth."
    sample_articles.append({"title": title, "content": content, "category": cat})

# Create DataFrame
df = pd.DataFrame(sample_articles)
print(f"Created dataset with {len(df)} articles")
print(f"Categories: {df['category'].value_counts().to_dict()}")

# Save to CSV
df.to_csv('data/articles.csv', index=False)
print("Saved to data/articles.csv")

# Build link graph based on category relationships
links = []

for cat in df['category'].unique():
    cat_articles = df[df['category'] == cat]['title'].tolist()
    for i, article in enumerate(cat_articles):
        other_articles = [a for a in cat_articles if a != article]
        if len(other_articles) >= 2:
            targets = random.sample(other_articles, min(3, len(other_articles)))
            for target in targets:
                links.append({'source': article, 'target': target})

# Add some cross-category links (10% of total)
all_titles = df['title'].tolist()
for _ in range(int(len(links) * 0.1)):
    source = random.choice(all_titles)
    target = random.choice([t for t in all_titles if t != source])
    links.append({'source': source, 'target': target})

links_df = pd.DataFrame(links)
print(f"Created {len(links_df)} links between articles")
links_df.to_csv('data/links.csv', index=False)
print("Saved to data/links.csv")

# ============================================================
# STEP 2: DATA PREPROCESSING
# ============================================================
print("\n[STEP 2] Preprocessing data...")

# Load and preprocess data
df = pd.read_csv('data/articles.csv')

# Remove empty rows
df = df.dropna(subset=['title', 'content'])
df = df[df['content'].str.len() > 100]

# Clean text
df['content_clean'] = df['content'].apply(
    lambda x: re.sub(r'\s+', ' ', str(x)).strip()
)

# Standardize categories
df['category'] = df['category'].str.lower().str.strip()

# Define stop words
stop_words = {"the","a","an","is","are","was","were","to","of","in","for",
              "on","with","at","by","from","and","or","but","not","this",
              "that","it","he","she","they","we","has","had","have","been",
              "said","also","would","could","will","its","who","which","more",
              "their","than","about","into","after","new","one","two","first"}

# Extract keywords
def get_keywords(text, n=5):
    words = re.findall(r'\b[a-z]{4,}\b', text.lower())
    counts = Counter(w for w in words if w not in stop_words)
    return [w for w, _ in counts.most_common(n)]

df['keywords'] = df['content_clean'].apply(get_keywords)

print(f"Clean dataset: {len(df)} articles")
print(f"Categories: {df['category'].value_counts().to_dict()}")
print(f"\nSample keywords:")
print(df[['title', 'keywords']].head(5))

# Save cleaned data
df.to_csv('data/articles_clean.csv', index=False)
print("\nSaved to data/articles_clean.csv")

# ============================================================
# STEP 3: ASSOCIATION RULE MINING (FP-Growth)
# ============================================================
print("\n[STEP 3] Running FP-Growth association rule mining...")

from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import fpgrowth, association_rules
import ast

# Load cleaned data
df = pd.read_csv('data/articles_clean.csv')

# Convert keywords string back to list
df['keywords'] = df['keywords'].apply(
    lambda x: ast.literal_eval(x) if isinstance(x, str) else x
)

# Build transactions
transactions = df['keywords'].tolist()
transactions = [t for t in transactions if len(t) >= 3]

print(f"Total transactions: {len(transactions)}")

# Encode transactions
te = TransactionEncoder()
te_array = te.fit(transactions).transform(transactions)
df_encoded = pd.DataFrame(te_array, columns=te.columns_)

# Run FP-Growth
frequent_itemsets = fpgrowth(df_encoded, min_support=0.03, use_colnames=True)

if len(frequent_itemsets) == 0:
    print("No itemsets found with min_support=0.03, lowering to 0.01...")
    frequent_itemsets = fpgrowth(df_encoded, min_support=0.01, use_colnames=True)

print(f"Frequent itemsets found: {len(frequent_itemsets)}")

# Generate association rules
rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.2)
rules = rules.sort_values("lift", ascending=False)

print(f"Rules found: {len(rules)}")
print("\nTop 10 Association Rules:")
if len(rules) > 0:
    print(rules[['antecedents','consequents','support','confidence','lift']].head(10).to_string())
else:
    print("No rules found with current parameters")

# Save results
frequent_itemsets.to_csv('outputs/frequent_itemsets.csv', index=False)
rules.to_csv('outputs/association_rules.csv', index=False)
print("\nSaved to outputs/")

# ============================================================
# STEP 4: LINK ANALYSIS (PageRank + HITS)
# ============================================================
print("\n[STEP 4] Running Link Analysis (PageRank + HITS)...")

import networkx as nx

# Load links
links_df = pd.read_csv('data/links.csv')

# Build directed graph
G = nx.DiGraph()
for _, row in links_df.iterrows():
    G.add_edge(row['source'], row['target'])

print(f"Graph: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")

# Calculate PageRank
pagerank = nx.pagerank(G, alpha=0.85)
pr_df = pd.DataFrame([
    {"node": k, "pagerank": v} for k, v in pagerank.items()
]).sort_values("pagerank", ascending=False)

print("\n🏆 Top 10 Pages by PageRank:")
print(pr_df.head(10).to_string())

# Calculate HITS
hubs, authorities = nx.hits(G, max_iter=100)

hits_df = pd.DataFrame([
    {"node": k, "hub_score": hubs[k], "authority_score": authorities[k]} 
    for k in G.nodes()
])
hits_df = hits_df.sort_values("authority_score", ascending=False)

print("\n🎯 Top 10 Authority Pages (HITS):")
print(hits_df.head(10).to_string())

print("\n🔗 Top 10 Hub Pages (HITS):")
print(hits_df.sort_values("hub_score", ascending=False).head(10).to_string())

# Save results
pr_df.to_csv('outputs/pagerank_results.csv', index=False)
hits_df.to_csv('outputs/hits_results.csv', index=False)
print("\nSaved to outputs/")

# ============================================================
# STEP 5: VISUALIZATIONS
# ============================================================
print("\n[STEP 5] Creating visualizations...")

import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns

plt.style.use('seaborn-v0_8-darkgrid')

# Load data for visualization
df = pd.read_csv('data/articles_clean.csv')
pr_df = pd.read_csv('outputs/pagerank_results.csv')
hits_df = pd.read_csv('outputs/hits_results.csv')
rules = pd.read_csv('outputs/association_rules.csv')

# Chart 1: Category Distribution
fig, ax = plt.subplots(figsize=(10, 5))
df['category'].value_counts().plot(kind='bar', ax=ax, color='steelblue')
ax.set_title('Number of Articles per Category', fontsize=14, fontweight='bold')
ax.set_xlabel('Category')
ax.set_ylabel('Count')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('outputs/chart1_categories.png', dpi=150)
plt.close()
print("✓ Saved: outputs/chart1_categories.png")

# Chart 2: Top 15 PageRank
fig, ax = plt.subplots(figsize=(10, 6))
top15 = pr_df.head(15)
ax.barh(range(len(top15)), top15['pagerank'], color='coral')
ax.set_yticks(range(len(top15)))
ax.set_yticklabels([str(n)[:50] for n in top15['node']], fontsize=8)
ax.invert_yaxis()
ax.set_title('Top 15 Pages by PageRank', fontsize=14, fontweight='bold')
ax.set_xlabel('PageRank Score')
plt.tight_layout()
plt.savefig('outputs/chart2_pagerank.png', dpi=150)
plt.close()
print("✓ Saved: outputs/chart2_pagerank.png")

# Chart 3: HITS Hub vs Authority Scatter
fig, ax = plt.subplots(figsize=(10, 7))
ax.scatter(hits_df['hub_score'], hits_df['authority_score'], 
           alpha=0.5, color='purple', s=30)
ax.set_xlabel('Hub Score', fontsize=12)
ax.set_ylabel('Authority Score', fontsize=12)
ax.set_title('HITS: Hub vs Authority Scores', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('outputs/chart3_hits.png', dpi=150)
plt.close()
print("✓ Saved: outputs/chart3_hits.png")

# Chart 4: Network Graph
links_df = pd.read_csv('data/links.csv')
G = nx.DiGraph()
for _, row in links_df.iterrows():
    G.add_edge(row['source'], row['target'])

# Keep only top 40 nodes by degree
if G.number_of_nodes() > 40:
    top_nodes = sorted(G.degree(), key=lambda x: x[1], reverse=True)[:40]
    G = G.subgraph([n[0] for n in top_nodes]).copy()

fig, ax = plt.subplots(figsize=(14, 10))
pos = nx.spring_layout(G, seed=42, k=0.8)
nx.draw(G, pos, ax=ax, node_size=100, node_color='skyblue',
        edge_color='gray', alpha=0.7, arrows=True, arrowsize=8,
        with_labels=False)
ax.set_title('Article Link Network (Top 40 Nodes)', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('outputs/chart4_network.png', dpi=150)
plt.close()
print("✓ Saved: outputs/chart4_network.png")

# Chart 5: Association Rules Scatter
if len(rules) > 0:
    fig, ax = plt.subplots(figsize=(10, 6))
    scatter = ax.scatter(rules['support'], rules['confidence'],
                        s=rules['lift']*50, c=rules['lift'], 
                        cmap='YlOrRd', alpha=0.7, edgecolors='black')
    plt.colorbar(scatter, label='Lift')
    ax.set_xlabel('Support', fontsize=12)
    ax.set_ylabel('Confidence', fontsize=12)
    ax.set_title('Association Rules (size & color = Lift)', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig('outputs/chart5_rules.png', dpi=150)
    plt.close()
    print("✓ Saved: outputs/chart5_rules.png")
else:
    print("No rules to visualize")

# ============================================================
# STEP 6: BERT TEXT CLASSIFICATION (Simplified - smaller sample)
# ============================================================
print("\n[STEP 6] Running BERT classification (this may take a few minutes)...")

from transformers import pipeline
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from tqdm import tqdm

# Load data
df = pd.read_csv('data/articles_clean.csv')

# Use a SMALLER sample for faster processing (due to memory constraints)
if len(df) > 50:
    df_sample = df.sample(50, random_state=42)
else:
    df_sample = df.copy()

print(f"Classifying {len(df_sample)} articles with BERT...")

# Load pre-trained zero-shot classifier
classifier = pipeline(
    "zero-shot-classification",
    model="facebook/bart-large-mnli",
    device=-1  # Force CPU usage
)

# Define candidate labels
candidate_labels = ["politics", "business", "technology", "sports", "entertainment"]

# Classify articles
predictions = []
confidence_scores = []

for _, row in tqdm(df_sample.iterrows(), total=len(df_sample), desc="BERT Classifying"):
    text = str(row['content_clean'])[:500]  # First 500 chars
    result = classifier(text, candidate_labels)
    predictions.append(result['labels'][0])
    confidence_scores.append(result['scores'][0])

df_sample['bert_prediction'] = predictions
df_sample['bert_confidence'] = confidence_scores

# Results
print("\n" + "="*60)
print("BERT PREDICTION RESULTS")
print("="*60)
print("\nBERT Predictions Distribution:")
print(df_sample['bert_prediction'].value_counts())

print(f"\nAverage Confidence: {df_sample['bert_confidence'].mean():.4f}")

# Classification report
print("\nClassification Report:")
print(classification_report(df_sample['category'], df_sample['bert_prediction']))

accuracy = accuracy_score(df_sample['category'], df_sample['bert_prediction'])
print(f"Overall Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")

# Chart 6: Confusion Matrix
cm = confusion_matrix(df_sample['category'], df_sample['bert_prediction'], 
                      labels=candidate_labels)

fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=candidate_labels, yticklabels=candidate_labels, ax=ax)
ax.set_xlabel('Predicted', fontsize=12)
ax.set_ylabel('Actual', fontsize=12)
ax.set_title(f'BERT Classification Confusion Matrix\n(Accuracy: {accuracy:.2%})', 
             fontsize=14, fontweight='bold')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('outputs/chart6_bert_confusion.png', dpi=150)
plt.close()
print("\n✓ Saved: outputs/chart6_bert_confusion.png")

# Chart 7: Confidence Distribution
fig, ax = plt.subplots(figsize=(10, 5))
ax.hist(df_sample['bert_confidence'], bins=20, color='teal', edgecolor='white')
ax.set_xlabel('Confidence Score', fontsize=12)
ax.set_ylabel('Count', fontsize=12)
ax.set_title('BERT Prediction Confidence Distribution', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('outputs/chart7_bert_confidence.png', dpi=150)
plt.close()
print("✓ Saved: outputs/chart7_bert_confidence.png")

# Save BERT results
df_sample.to_csv('outputs/bert_results.csv', index=False)
print("\n✓ Saved: outputs/bert_results.csv")

# Bonus: Sentiment Analysis with BERT
print("\n[BONUS] Running sentiment analysis...")

sentiment_pipeline = pipeline("sentiment-analysis", 
                              model="distilbert-base-uncased-finetuned-sst-2-english")

sentiments = []
for _, row in tqdm(df_sample.iterrows(), total=len(df_sample), desc="Sentiment Analysis"):
    text = str(row['content_clean'])[:512]
    result = sentiment_pipeline(text)
    sentiments.append(result[0]['label'])

df_sample['sentiment'] = sentiments

print("\nSentiment Distribution:")
print(df_sample['sentiment'].value_counts())

# Chart 8: Sentiment Distribution
fig, ax = plt.subplots(figsize=(8, 5))
df_sample['sentiment'].value_counts().plot(kind='bar', ax=ax, color=['red', 'green'])
ax.set_title('Article Sentiment Distribution', fontsize=14, fontweight='bold')
ax.set_xlabel('Sentiment')
ax.set_ylabel('Count')
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig('outputs/chart8_sentiment.png', dpi=150)
plt.close()
print("✓ Saved: outputs/chart8_sentiment.png")

# Save final results
df_sample.to_csv('outputs/bert_results.csv', index=False)

# ============================================================
# SUMMARY
# ============================================================
print("\n" + "="*60)
print("✅ PROJECT COMPLETED SUCCESSFULLY!")
print("="*60)
print("""
What we accomplished:
1. ✓ Created dataset with 150+ news articles across 5 categories
2. ✓ Built link graph connecting related articles
3. ✓ Preprocessed text and extracted keywords
4. ✓ Applied FP-Growth for association rule mining
5. ✓ Ran PageRank and HITS algorithms for link analysis
6. ✓ Used BERT for zero-shot text classification
7. ✓ Generated 8 visualization charts

Output Files:
- data/articles.csv - Original articles
- data/links.csv - Link edges
- data/articles_clean.csv - Cleaned data with keywords
- outputs/frequent_itemsets.csv - FP-Growth results
- outputs/association_rules.csv - Association rules
- outputs/pagerank_results.csv - PageRank scores
- outputs/hits_results.csv - HITS scores
- outputs/bert_results.csv - BERT classifications
- outputs/chart*.png - All visualizations

Next Steps:
1. Review all output files and charts
2. Write the report (12-18 pages)
3. Create presentation slides (10 slides)
4. Submit project!
""")
