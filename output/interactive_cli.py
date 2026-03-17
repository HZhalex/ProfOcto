"""
Interactive Refinement CLI
Allow PhD students to interactively explore and refine gap analysis.
"""

from rich.prompt import Prompt
from rich.table import Table
from output.terminal_renderer import console
from agents.gap_ranker import (
    rank_gaps, generate_comparison_table, identify_pareto_frontier,
    recommend_based_on_constraints, analyze_gap_portfolio
)
from utils.logger import get_logger


class InteractiveRefinementCLI:
    """Interactive CLI for exploring and refining gap analysis results."""
    
    def __init__(self, readiness_scores):
        self.readiness_scores = readiness_scores
        self.logger = get_logger()
        self.selected_gap = None
    
    def run(self):
        """Main interactive loop."""
        console.print("\n[bold cyan]━━━ Interactive Gap Analysis & Refinement ━━━[/bold cyan]\n")
        
        while True:
            console.print("[bold]What would you like to do?[/bold]\n")
            console.print("1. [green]Compare gaps[/green] - View side-by-side comparison")
            console.print("2. [cyan]Rank gaps[/cyan] - Sort by different criteria")
            console.print("3. [magenta]Find best choice[/magenta] - Based on your constraints")
            console.print("4. [yellow]Analyze portfolio[/yellow] - Overall gap landscape")
            console.print("5. [blue]View gap details[/blue] - Deep dive into one gap")
            console.print("6. [white]Export & exit[/white] - Save results and exit\n")
            
            choice = Prompt.ask("[bold]Choose[/bold]", choices=["1", "2", "3", "4", "5", "6"])
            
            if choice == "1":
                self._compare_gaps()
            elif choice == "2":
                self._rank_gaps()
            elif choice == "3":
                self._find_best_fit()
            elif choice == "4":
                self._analyze_portfolio()
            elif choice == "5":
                self._view_gap_details()
            elif choice == "6":
                console.print("\n[green]✓ Analysis complete. Results exported.[/green]\n")
                break
            
            console.print()
    
    def _compare_gaps(self):
        """Show comparison table."""
        console.print("\n[bold cyan]Gap Comparison Table[/bold cyan]\n")
        table_str = generate_comparison_table(self.readiness_scores)
        console.print(table_str)
    
    def _rank_gaps(self):
        """Rank gaps by different criteria."""
        console.print("\n[bold cyan]Rank Gaps By:[/bold cyan]\n")
        console.print("1. Novelty (maximize ICLR impact)")
        console.print("2. Feasibility (quick wins)")
        console.print("3. Balanced (Pareto-optimal)")
        console.print("4. Impact (combined novelty + advisor fit)")
        console.print("5. Speed (fast first results)\n")
        
        criteria_choice = Prompt.ask("Choose ranking", choices=["1", "2", "3", "4", "5"])
        
        criteria_map = {
            "1": "novelty",
            "2": "feasibility",
            "3": "balanced",
            "4": "impact",
            "5": "speed"
        }
        criteria = criteria_map[criteria_choice]
        
        ranked = rank_gaps(self.readiness_scores, criteria)
        
        console.print(f"\n[bold cyan]Top gaps by '{criteria}':[/bold cyan]\n")
        for title, score, rank in ranked[:5]:
            console.print(f"{rank}. [green]{title}[/green] (score: {score:.1f})")
    
    def _find_best_fit(self):
        """Interactive constraint-based recommendation."""
        console.print("\n[bold cyan]Let's find gaps matching your constraints[/bold cyan]\n")
        
        timeline = Prompt.ask("Max timeline (months)", default="12")
        novelty = Prompt.ask("Min novelty needed (0-100)", default="60")
        risk = Prompt.ask("Max acceptable risk (Low/Medium/High/VeryHigh)", default="High")
        
        try:
            constraints = {
                "max_timeline_months": int(timeline),
                "min_novelty": int(novelty),
                "max_risk": risk
            }
            
            candidates = recommend_based_on_constraints(self.readiness_scores, constraints)
            
            if candidates:
                console.print(f"\n[green]✓ Found {len(candidates)} feasible gaps:[/green]\n")
                for title, score, status in candidates[:5]:
                    console.print(f"  • {title} (score: {score:.1f})")
            else:
                console.print("\n[yellow]⚠ No gaps match your constraints. Try relaxing them.[/yellow]")
        
        except ValueError:
            console.print("[red]Invalid input. Please try again.[/red]")
    
    def _analyze_portfolio(self):
        """Show portfolio analysis."""
        console.print("\n[bold cyan]Gap Portfolio Analysis[/bold cyan]\n")
        
        analysis = analyze_gap_portfolio(self.readiness_scores)
        
        console.print(f"Total gaps: {analysis.get('total_gaps', 0)}")
        console.print(f"Average novelty: {analysis.get('average_novelty', 0):.0f}/100")
        novelty_range = analysis.get('novelty_range', (0, 0))
        console.print(f"  Range: {novelty_range[0]:.0f} - {novelty_range[1]:.0f}")
        
        console.print(f"\nAverage timeline: {analysis.get('average_timeline_months', 0):.0f} months")
        timeline_range = analysis.get('timeline_range', (0, 0))
        console.print(f"  Range: {timeline_range[0]:.0f} - {timeline_range[1]:.0f} months")
        
        risk_dist = analysis.get('risk_distribution', {})
        if risk_dist:
            console.print(f"\nRisk distribution:")
            for risk, count in risk_dist.items():
                console.print(f"  {risk}: {count} gap(s)")
        
        # Pareto frontier
        frontier = identify_pareto_frontier(self.readiness_scores)
        if frontier:
            console.print(f"\n[bold]Pareto frontier ({len(frontier)} gaps):[/bold]")
            for gap in frontier:
                console.print(f"  ✓ {gap}")
        
        # Recommendations
        portfolio = analysis.get('recommended_portfolio', {})
        if portfolio.get('high_impact'):
            console.print(f"\n[bold]High-impact gaps:[/bold]")
            for gap in portfolio['high_impact']:
                console.print(f"  🎯 {gap}")
        
        if portfolio.get('quick_wins'):
            console.print(f"\n[bold]Quick wins:[/bold]")
            for gap in portfolio['quick_wins']:
                console.print(f"  ⚡ {gap}")
    
    def _view_gap_details(self):
        """View full details of a selected gap."""
        console.print("\n[bold cyan]Select a gap to view details:[/bold cyan]\n")
        
        for i, gap in enumerate(self.readiness_scores, 1):
            console.print(f"{i}. {gap.get('gap_title', 'Unknown')}")
        
        try:
            choice = int(Prompt.ask("\nChoice"))
            if 1 <= choice <= len(self.readiness_scores):
                gap = self.readiness_scores[choice - 1]
                self._display_gap_details(gap)
            else:
                console.print("[red]Invalid choice.[/red]")
        except ValueError:
            console.print("[red]Invalid input.[/red]")
    
    def _display_gap_details(self, gap):
        """Display detailed information about a gap."""
        console.print(f"\n[bold cyan]═══ {gap.get('gap_title', 'Unknown')} ═══[/bold cyan]\n")
        
        # Readiness
        console.print(f"[bold]Readiness Assessment[/bold]")
        console.print(f"  Score: {gap.get('iclr_readiness_score', 0):.0f}/100")
        console.print(f"  Recommendation: {gap.get('recommendation', '?')}")
        console.print(f"  Confidence: {gap.get('recommendation_confidence', 0):.0%}\n")
        
        # Timeline
        timeline = gap.get("timeline_assessment", {})
        if timeline:
            console.print(f"[bold]Timeline[/bold]")
            console.print(f"  Total: ~{timeline.get('total_timeline_months', 0):.0f} months")
            console.print(f"  Research phase: {timeline.get('research_phase', '?')}")
            console.print(f"  Publication: {timeline.get('publication_phase', '?')}\n")
        
        # Risk
        risk = gap.get("risk_assessment", {})
        if risk:
            console.print(f"[bold]Risk Assessment[/bold]")
            console.print(f"  Level: {risk.get('risk_level', '?')}")
            risks = risk.get('major_risks', [])
            if risks:
                console.print(f"  Major risks:")
                for r in risks[:3]:
                    console.print(f"    ⚠ {r}")
            print()
        
        # Action items
        actions = gap.get("action_items", [])
        if actions:
            console.print(f"[bold]Action Items[/bold]")
            for item in actions[:5]:
                console.print(f"  [{item.get('priority')}] {item.get('action')}")
                console.print(f"      Timeline: {item.get('timeline')}")
            print()
        
        # Verdict
        verdict = gap.get("final_verdict", "")
        if verdict:
            console.print(f"[bold]Summary[/bold]")
            console.print(f"  {verdict}")


def launch_interactive_cli(readiness_scores):
    """Launch the interactive refinement CLI."""
    if not readiness_scores:
        console.print("[yellow]No gaps to analyze. Run Phase 5 first.[/yellow]")
        return
    
    cli = InteractiveRefinementCLI(readiness_scores)
    cli.run()
