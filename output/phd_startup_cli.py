"""
PhD Startup CLI - Hybrid Quick & Interactive Mode
Provides flexible startup: quick by default with option for deeper configuration.
"""

from typing import Dict, Any, Optional
import config
from utils.logger import get_logger


class PhDStartupCLI:
    """Handle startup configuration in hybrid mode."""
    
    def __init__(self):
        self.logger = get_logger()
        self.settings: Dict[str, Any] = {
            'topic': '',
            'field': 'General AI',
            'depth': 'quick',
            'output_style': 'minimal',
            'enable_phase5': True,
            'enable_phase6': True,
            'enable_interactive': True,
            'skip_optional': False
        }
    
    def startup(self) -> Dict[str, Any]:
        """
        Run startup sequence.
        
        Returns:
            Configured settings for debate pipeline
        """
        
        if not config.QUICK_START_MODE:
            return self._interactive_setup()
        
        # QUICK START: Minimal questions
        print("\n" + "="*70)
        print("🎓 ProfOcto - Research Gap Analyzer for PhD Students".center(70))
        print("="*70)
        print()
        
        # Question 1: Research Topic (required)
        topic = self._prompt_topic()
        self.settings['topic'] = topic
        
        # Show cost estimate
        from output.cost_estimator import estimate_cost_for_gaps, CostEstimator
        num_gaps = config.DEFAULT_NUM_GAPS
        estimate = estimate_cost_for_gaps(num_gaps)
        
        print(f"\n📊 Estimated Cost & Timeline:")
        print(f"  • API Cost: ${estimate['estimated_cost_usd']}")
        print(f"  • Runtime: {estimate['estimated_time_readable']}")
        print()
        
        # Quick mode: yes/no for Phase 5
        if config.ENABLE_PHASE5:
            response = input("🔬 Run advanced ICLR readiness analysis (Phase 5)? [Y/n]: ").strip().lower()
            self.settings['enable_phase5'] = response != 'n'
        
        # Optional: allow setup refinement before running
        if config.INTERACTIVE_SETUP:
            response = input("\n⚙️  Customize settings before running? [y/N]: ").strip().lower()
            if response == 'y':
                self.settings = self._refinement_menu()
        
        return self.settings
    
    def _interactive_setup(self) -> Dict[str, Any]:
        """Full interactive setup mode."""
        print("\n" + "="*70)
        print("🎓 ProfOcto - Research Gap Analyzer".center(70))
        print("Full Configuration Mode".center(70))
        print("="*70)
        print()
        
        # Topic
        self.settings['topic'] = self._prompt_topic()
        
        # Field
        print("\n📚 Research Field:")
        print("  1. General AI")
        print("  2. Machine Learning")
        print("  3. NLP")
        print("  4. Computer Vision")
        print("  5. Reinforcement Learning")
        print("  6. Other (custom)")
        
        choice = input("Select field (1-6) [1]: ").strip() or "1"
        fields = ["General AI", "Machine Learning", "NLP", "Computer Vision", "Reinforcement Learning"]
        
        if choice.isdigit() and 1 <= int(choice) <= 5:
            self.settings['field'] = fields[int(choice)-1]
        else:
            self.settings['field'] = input("Enter custom field: ").strip() or "General AI"
        
        # Depth
        print("\n⚡ Analysis Depth:")
        print("  1. Quick (debate only, ~2-3 min)")
        print("  2. Standard (debate + rigor checks, ~5-7 min)")
        print("  3. Deep (all phases including Phase 5, ~15-20 min)")
        
        choice = input("Select depth [2]: ").strip() or "2"
        depths = ["quick", "standard", "deep"]
        
        if choice.isdigit() and 1 <= int(choice) <= 3:
            self.settings['depth'] = depths[int(choice)-1]
        
        # Output style
        print("\n📄 Output Style:")
        print("  1. Minimal (key findings only)")
        print("  2. Detailed (full analysis)")
        print("  3. Both (toggle during analysis)")
        
        choice = input("Select style [3]: ").strip() or "3"
        
        if choice == "1":
            self.settings['output_style'] = 'minimal'
        elif choice == "2":
            self.settings['output_style'] = 'detailed'
        else:
            self.settings['output_style'] = 'both'
        
        return self.settings
    
    def _refinement_menu(self) -> Dict[str, Any]:
        """Post-startup refinement menu before running."""
        print("\n" + "─"*70)
        print("⚙️  Quick Settings Refinement".center(70))
        print("─"*70)
        
        while True:
            print(f"""
Current Settings:
  • Topic: {self.settings['topic']}
  • Field: {self.settings['field']}
  • Phase 5 (ICLR Analysis): {"Yes" if self.settings['enable_phase5'] else "No"}
  • Interactive Refinement: {"Yes" if self.settings['enable_interactive'] else "No"}

Options:
  [1] Change topic
  [2] Change field
  [3] Toggle Phase 5 analysis
  [4] Toggle interactive refinement
  [5] Skip optional features (fast mode)
  [0] Proceed to analysis
""")
            
            choice = input("Select option [0]: ").strip() or "0"
            
            if choice == "1":
                self.settings['topic'] = self._prompt_topic()
            elif choice == "2":
                self.settings['field'] = input("Enter field: ").strip() or self.settings['field']
            elif choice == "3":
                self.settings['enable_phase5'] = not self.settings['enable_phase5']
            elif choice == "4":
                self.settings['enable_interactive'] = not self.settings['enable_interactive']
            elif choice == "5":
                self.settings['skip_optional'] = True
                print("\n✅ Fast mode enabled - optional features will be skipped")
            elif choice == "0":
                break
        
        return self.settings
    
    def _prompt_topic(self) -> str:
        """Prompt for research topic."""
        print("\n🎯 Research Gap Analysis")
        print("What research topic or problem would you like to explore?")
        print("(Examples: 'How to improve transformer efficiency?',")
        print("          'Novel approaches to few-shot learning')")
        print()
        
        topic = input("Enter your topic: ").strip()
        
        if not topic:
            print("⚠️  Topic is required. Using default topic.")
            return "Research gaps in AI"
        
        return topic
    
    def show_summary(self) -> str:
        """Show summary of selected settings."""
        summary = f"""
╔{'═'*68}╗
║ {'STARTUP SUMMARY'.center(66)} ║
╠{'═'*68}╣
║ Topic: {self.settings['topic'][:60]:<60} ║
║ Field: {self.settings['field']:<60} ║
║ Analysis Depth: {self.settings['depth']:<45} ║
║ Output Style: {self.settings['output_style']:<46} ║
║ Phase 5 (ICLR): {"Enabled" if self.settings['enable_phase5'] else "Disabled":<47} ║
╚{'═'*68}╝

Starting analysis...
"""
        return summary


def run_startup() -> Dict[str, Any]:
    """Run startup CLI and return settings."""
    cli = PhDStartupCLI()
    settings = cli.startup()
    
    print(cli.show_summary())
    
    return settings


def show_startup_help() -> str:
    """Show help for startup options."""
    return """
ProfOcto Startup Options:

QUICK MODE (Recommended):
  - Asks for topic only
  - Shows cost estimate before running
  - Option to customize settings before analysis

INTERACTIVE MODE:
  - Configure all aspects before starting
  - Selected via command-line flag
  - Best for: Fine-tuning analysis parameters

FEATURES:
  ✅ Hybrid Mode: Quick first, refine anytime
  ✅ Cost Preview: Estimate before running
  ✅ Flexible Depth: Quick, standard, or deep analysis
  ✅ Output Toggle: Switch between minimal/detailed anytime

FAST MODE:
  - Skip optional Phase 6 features
  - Reduces runtime by 30-40%
  - Enabled via settings refinement menu
"""
