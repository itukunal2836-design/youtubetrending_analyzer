import argparse
import sys
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud


def load_data(path: Path) -> pd.DataFrame:
	"""Load CSV from path and return a DataFrame.

	Raises SystemExit with a friendly message when the file can't be found or read.
	"""
	# Resolve relative paths against the current working directory
	path = path if path.is_absolute() else (Path.cwd() / path)
	if not path.exists():
		print(f"Error: data file not found at: {path}")
		print(f"Current working directory: {Path.cwd()}")
		print("Files in working directory:")
		for p in sorted(Path.cwd().iterdir()):
			print(" -", p.name)
		print("\nYou can run this script with the CSV path, for example:")
		print("  python eda_analysis.py D:\\path\\to\\youtube_trending.csv")
		sys.exit(2)

	try:
		df = pd.read_csv(path)
	except Exception as e:
		print(f"Failed to read CSV ({path}): {e}")
		sys.exit(3)

	return df


def main():
	parser = argparse.ArgumentParser(description="Run EDA on YouTube trending CSV")
	parser.add_argument("csv", nargs="?", default="youtube_trending.csv", help="path to youtube_trending.csv")
	parser.add_argument("--quiet", action="store_true", help="suppress verbose output (info/head)")
	args = parser.parse_args()

	data_path = Path(args.csv)
	df = load_data(data_path)

	# Ensure publish_time exists and is parsed
	if 'publish_time' in df.columns:
		df['publish_time'] = pd.to_datetime(df['publish_time'], errors='coerce')

	if not args.quiet:
		print("Basic Info:")
		print(df.info())
		print("\nTop 5 Rows:\n", df.head())

	# 1️⃣ Views vs Likes
	if {'views', 'likes'}.issubset(df.columns):
		sns.scatterplot(x='views', y='likes', data=df)
		plt.title("Views vs Likes")
		plt.show()

	# 2️⃣ Correlation
	corr_cols = [c for c in ('views', 'likes', 'comments') if c in df.columns]
	if len(corr_cols) >= 2:
		sns.heatmap(df[corr_cols].corr(), annot=True, cmap='coolwarm')
		plt.title("Feature Correlation")
		plt.show()

	# 3️⃣ WordCloud of Video Titles
	if 'title' in df.columns:
		text = " ".join(df['title'].astype(str))
		wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
		plt.imshow(wordcloud, interpolation='bilinear')
		plt.axis('off')
		plt.title("Common Words in Trending Titles")
		plt.show()

	# 4️⃣ Publish Time Distribution
	if 'publish_time' in df.columns:
		df['hour'] = df['publish_time'].dt.hour
		sns.histplot(df['hour'].dropna(), bins=24, kde=True)
		plt.title("Publish Time Distribution by Hour")
		plt.show()


if __name__ == '__main__':
	main()
