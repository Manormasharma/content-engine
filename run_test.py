from app.tasks import run_content_pipeline

if __name__ == "__main__":
    print("🚀 Triggering Autonomous Research Engine with Gemini...")
    result = run_content_pipeline(
        topic="The evolution of multi-agent orchestration frameworks in software engineering",
        output_format="Blog Post"
    )
    print("\n\n=== FINAL OUTPUT ===")
    print(result)