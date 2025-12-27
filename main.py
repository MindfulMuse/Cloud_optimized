
"""
Cloud Cost Optimizer - CLI Application
"""
import os
import json
from pathlib import Path
from dotenv import load_dotenv
from profile_extractor import extract_project_profile
from billing_generator import generate_mock_billing
from cost_analyser import analyze_costs_and_recommend
from utils import print_banner, print_menu, clear_screen

# Load environment variables
load_dotenv()

class CloudCostOptimizer:
    def __init__(self):
        self.data_dir = Path("data")
        self.data_dir.mkdir(exist_ok=True)
        
        self.project_desc_file = self.data_dir / "project_description.txt"
        self.profile_file = self.data_dir / "project_profile.json"
        self.billing_file = self.data_dir / "mock_billing.json"
        self.report_file = self.data_dir / "cost_optimization_report.json"
    
    def enter_project_description(self):
        """Allow user to enter project description"""
        clear_screen()
        print_banner("Enter Project Description")
        print("\nEnter your project description (multiple lines supported)")
        print("When finished, type 'DONE' on a new line and press Enter")
        print("-" * 70)
        print()
        
        lines = []
        while True:
            try:
                line = input()
                # Check if user typed DONE
                if line.strip().upper() == 'DONE':
                    break
                lines.append(line)
            except (EOFError, KeyboardInterrupt):
                break
        
        description = "\n".join(lines).strip()
        
        if not description:
            print("\n❌ No description entered!")
            input("\nPress Enter to continue...")
            return
        
        # Save to file
        try:
            with open(self.project_desc_file, 'w', encoding='utf-8') as f:
                f.write(description)
            
            print(f"\n✅ Project description saved!")
            print(f"   File: {self.project_desc_file}")
            print(f"   Length: {len(description)} characters")
        except Exception as e:
            print(f"\n❌ Error saving file: {str(e)}")
        
        input("\nPress Enter to continue...")
    
    def run_complete_analysis(self):
        """Run the complete cost analysis pipeline"""
        clear_screen()
        print_banner("Running Complete Cost Analysis")
        
        # Check if project description exists
        if not self.project_desc_file.exists():
            print("\n❌ No project description found! Please enter one first.")
            input("\nPress Enter to continue...")
            return
        
        try:
            # Step 1: Extract Project Profile
            print("\n" + "="*70)
            print("STEP 1/3: Extracting Project Profile")
            print("="*70)
            
            with open(self.project_desc_file, 'r', encoding='utf-8') as f:
                description = f.read()
            
            print(f"\nAnalyzing: {description[:100]}...")
            profile = extract_project_profile(description)
            
            with open(self.profile_file, 'w', encoding='utf-8') as f:
                json.dump(profile, f, indent=2)
            
            print(f"\n✅ Project profile extracted and saved")
            print(f"   → Project: {profile['name']}")
            print(f"   → Budget: ₹{profile['budget_inr_per_month']:,.2f}/month")
            
            # Step 2: Generate Mock Billing
            print("\n" + "="*70)
            print("STEP 2/3: Generating Synthetic Billing Data")
            print("="*70)
            
            billing_data = generate_mock_billing(profile)
            
            with open(self.billing_file, 'w', encoding='utf-8') as f:
                json.dump(billing_data, f, indent=2)
            
            print(f"\n✅ Mock billing data generated and saved")
            print(f"   → Records: {len(billing_data)}")
            
            total_cost = sum(r['cost_inr'] for r in billing_data)
            print(f"   → Total Cost: ₹{total_cost:,.2f}")
            
            # Step 3: Analyze and Generate Recommendations
            print("\n" + "="*70)
            print("STEP 3/3: Analyzing Costs & Generating Recommendations")
            print("="*70)
            
            report = analyze_costs_and_recommend(profile, billing_data)
            
            with open(self.report_file, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2)
            
            print(f"\n✅ Cost optimization report generated and saved")
            
            # Display summary
            print("\n" + "="*70)
            print("📊 ANALYSIS SUMMARY")
            print("="*70)
            
            analysis = report['analysis']
            print(f"\n💰 Cost Overview:")
            print(f"   Total Monthly Cost: ₹{analysis['total_monthly_cost']:,.2f}")
            print(f"   Budget:             ₹{analysis['budget']:,.2f}")
            print(f"   Variance:           ₹{analysis['budget_variance']:,.2f}")
            
            if analysis['is_over_budget']:
                print(f"   Status:             ⚠️  OVER BUDGET")
            else:
                print(f"   Status:             ✅ UNDER BUDGET")
            
            summary = report['summary']
            print(f"\n💡 Optimization Potential:")
            print(f"   Total Savings:      ₹{summary['total_potential_savings']:,.2f}")
            print(f"   Savings %:          {summary['savings_percentage']:.1f}%")
            print(f"   Recommendations:    {summary['recommendations_count']}")
            
            print("\n" + "="*70)
            print("✅ Complete analysis finished successfully!")
            print("="*70)
            
        except Exception as e:
            print(f"\n❌ Error during analysis: {str(e)}")
            print("\nDebug info:")
            import traceback
            traceback.print_exc()
        
        input("\nPress Enter to continue...")
    
    def view_recommendations(self):
        """Display cost optimization recommendations"""
        clear_screen()
        print_banner("Cost Optimization Recommendations")
        
        if not self.report_file.exists():
            print("\n❌ No report found! Please run the complete analysis first.")
            input("\nPress Enter to continue...")
            return
        
        try:
            with open(self.report_file, 'r', encoding='utf-8') as f:
                report = json.load(f)
            
            recommendations = report['recommendations']
            
            print(f"\n📋 Total Recommendations: {len(recommendations)}")
            print(f"💰 Total Potential Savings: ₹{report['summary']['total_potential_savings']:,.2f}")
            print(f"📊 Savings Percentage: {report['summary']['savings_percentage']:.1f}%")
            
            for idx, rec in enumerate(recommendations, 1):
                print(f"\n{'='*70}")
                print(f"#{idx}: {rec['title']}")
                print(f"{'='*70}")
                print(f"Service:            {rec['service']}")
                print(f"Current Cost:       ₹{rec['current_cost']:,.2f}")
                print(f"Potential Savings:  ₹{rec['potential_savings']:,.2f}")
                print(f"Type:               {rec['recommendation_type']}")
                print(f"Implementation:     {rec['implementation_effort'].upper()} effort")
                print(f"Risk Level:         {rec['risk_level'].upper()}")
                
                print(f"\n📝 Description:")
                print(f"   {rec['description']}")
                
                print(f"\n☁️  Cloud Providers: {', '.join(rec['cloud_providers'])}")
                
                print(f"\n📋 Implementation Steps:")
                for step_idx, step in enumerate(rec['steps'], 1):
                    print(f"   {step_idx}. {step}")
            
            print(f"\n{'='*70}")
            
        except Exception as e:
            print(f"\n❌ Error loading report: {str(e)}")
        
        input("\nPress Enter to continue...")
    
    def export_report(self):
        """Export report to a formatted file"""
        clear_screen()
        print_banner("Export Report")
        
        if not self.report_file.exists():
            print("\n❌ No report found! Please run the complete analysis first.")
            input("\nPress Enter to continue...")
            return
        
        try:
            export_file = self.data_dir / "cost_optimization_report_formatted.txt"
            
            with open(self.report_file, 'r', encoding='utf-8') as f:
                report = json.load(f)
            
            with open(export_file, 'w', encoding='utf-8') as f:
                f.write("="*80 + "\n")
                f.write("CLOUD COST OPTIMIZATION REPORT\n")
                f.write("="*80 + "\n\n")
                
                f.write(f"Project: {report['project_name']}\n")
                f.write(f"Generated: {self._get_timestamp()}\n\n")
                
                analysis = report['analysis']
                f.write("COST ANALYSIS\n")
                f.write("-"*80 + "\n")
                f.write(f"Total Monthly Cost: ₹{analysis['total_monthly_cost']:,.2f}\n")
                f.write(f"Budget: ₹{analysis['budget']:,.2f}\n")
                f.write(f"Variance: ₹{analysis['budget_variance']:,.2f}\n")
                f.write(f"Over Budget: {'Yes' if analysis['is_over_budget'] else 'No'}\n\n")
                
                f.write("Service Costs Breakdown:\n")
                for service, cost in sorted(analysis['service_costs'].items(), 
                                           key=lambda x: x[1], reverse=True):
                    f.write(f"  - {service}: ₹{cost:,.2f}\n")
                
                f.write("\n" + "="*80 + "\n")
                f.write("RECOMMENDATIONS\n")
                f.write("="*80 + "\n\n")
                
                for idx, rec in enumerate(report['recommendations'], 1):
                    f.write(f"{idx}. {rec['title']}\n")
                    f.write("-"*80 + "\n")
                    f.write(f"Service: {rec['service']}\n")
                    f.write(f"Current Cost: ₹{rec['current_cost']:,.2f}\n")
                    f.write(f"Potential Savings: ₹{rec['potential_savings']:,.2f}\n")
                    f.write(f"Type: {rec['recommendation_type']}\n")
                    f.write(f"Effort: {rec['implementation_effort']} | Risk: {rec['risk_level']}\n")
                    f.write(f"\nDescription: {rec['description']}\n")
                    f.write(f"\nCloud Providers: {', '.join(rec['cloud_providers'])}\n")
                    f.write(f"\nImplementation Steps:\n")
                    for step_idx, step in enumerate(rec['steps'], 1):
                        f.write(f"  {step_idx}. {step}\n")
                    f.write("\n")
                
                summary = report['summary']
                f.write("\n" + "="*80 + "\n")
                f.write("SUMMARY\n")
                f.write("="*80 + "\n")
                f.write(f"Total Potential Savings: ₹{summary['total_potential_savings']:,.2f}\n")
                f.write(f"Savings Percentage: {summary['savings_percentage']:.2f}%\n")
                f.write(f"Total Recommendations: {summary['recommendations_count']}\n")
                f.write(f"High Impact Recommendations: {summary['high_impact_recommendations']}\n")
            
            print(f"\n✅ Report exported successfully!")
            print(f"   File: {export_file}")
            print(f"   Size: {export_file.stat().st_size} bytes")
            
        except Exception as e:
            print(f"\n❌ Error exporting report: {str(e)}")
        
        input("\nPress Enter to continue...")
    
    def _get_timestamp(self):
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def run(self):
        """Main application loop"""
        while True:
            clear_screen()
            print_banner("Cloud Cost Optimizer")
            print("\n🤖 AI-Powered Cloud Cost Analysis & Optimization")
            
            print_menu([
                "Enter New Project Description",
                "Run Complete Cost Analysis",
                "View Recommendations",
                "Export Report",
                "Exit"
            ])
            
            choice = input("\nEnter your choice (1-5): ").strip()
            
            if choice == '1':
                self.enter_project_description()
            elif choice == '2':
                self.run_complete_analysis()
            elif choice == '3':
                self.view_recommendations()
            elif choice == '4':
                self.export_report()
            elif choice == '5':
                clear_screen()
                print("\n" + "="*70)
                print("👋 Thank you for using Cloud Cost Optimizer!")
                print("="*70)
                print()
                break
            else:
                print("\n❌ Invalid choice! Please enter a number between 1-5.")
                input("\nPress Enter to continue...")

if __name__ == "__main__":
    try:
        app = CloudCostOptimizer()
        app.run()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Fatal error: {str(e)}")
        import traceback
        traceback.print_exc()