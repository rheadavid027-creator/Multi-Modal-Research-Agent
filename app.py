from agent import run_research_pipeline
topic = input("Enter research topic: ").strip()

latex = run_research_pipeline(topic)

    # Save to file
    
filename = f"{'_'.join(topic.split()[:4])}.tex"
with open(filename, "w", encoding="utf-8") as f:
    f.write(latex)

print(f"\n[bold green]✅ Saved to {filename}[/bold green]")
print("\n[dim]--- LaTeX Preview (first 500 chars) ---[/dim]")
print(latex[:500])
