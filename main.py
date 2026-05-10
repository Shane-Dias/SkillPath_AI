"""
Main Application - AI-Based Skill Gap & Career Path Advisor
"""

from skill_gap_analyzer import SkillGapAnalyzer
import json
from datetime import datetime

class CareerAdvisorApp:
    def __init__(self):
        self.analyzer = SkillGapAnalyzer()
        
    def get_user_input(self) -> tuple:
        print("\n" + "="*70)
        print(" AI-BASED SKILL GAP & CAREER PATH ADVISOR")
        print("="*70)
        
        available_jobs = list(self.analyzer.expert_system.job_requirements.keys())
        print("\n Available Career Paths:")
        for i, job in enumerate(available_jobs, 1):
            print(f"   {i}. {job}")
        
        while True:
            print("\n Tip: You can enter exact job title or number")
            choice = input("\n Enter your dream job (title or number): ").strip()
            
            if choice.isdigit() and 1 <= int(choice) <= len(available_jobs):
                dream_job = available_jobs[int(choice) - 1]
                break
            elif choice in available_jobs:
                dream_job = choice
                break
            else:
                print(f" Job not found. Choose from: {', '.join(available_jobs)}")
        
        print(f"\n Let's assess your current skills for {dream_job}")
        print("   (Enter skills one by one, type 'done' when finished)")
        print("   Example skills: Python, SQL, Machine Learning, Communication")
        
        current_skills = {}
        skill_levels = ["beginner", "intermediate", "advanced"]
        
        while True:
            skill = input("\n   Enter a skill you have (or 'done'): ").strip().lower()
            if skill == 'done':
                break
            if skill:
                print(f"   Proficiency levels: {', '.join(skill_levels)}")
                level = input(f"   Your level in {skill} (beginner/intermediate/advanced): ").strip().lower()
                if level in skill_levels:
                    current_skills[skill] = level
                else:
                    print(f"    Invalid level. Setting to 'beginner'")
                    current_skills[skill] = "beginner"
        
        return current_skills, dream_job
    
    def run(self):
        try:
            current_skills, dream_job = self.get_user_input()
            
            if not current_skills:
                print("\n No skills entered. Using default skills...")
                current_skills = {"python": "beginner"}
            
            print("\n Analyzing your skills using Expert System...")
            print("   (Applying inference rules to identify skill gaps)")
            analysis = self.analyzer.analyze_skills(current_skills, dream_job)
            
            self.analyzer.display_analysis(analysis)
            
            save_choice = input("\n Save detailed report? (yes/no): ").strip().lower()
            if save_choice == 'yes':
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"career_report_{timestamp}.json"
                with open(filename, 'w') as f:
                    json.dump(analysis, f, indent=2)
                print(f"\n Report saved to {filename}")
            
            print("\n Analysis complete! Good luck with your career journey! ")
            
        except KeyboardInterrupt:
            print("\n\n Goodbye!")
        except Exception as e:
            print(f"\n Error: {e}")

def demo_mode():
    print("\n" + "" * 35)
    print("RUNNING IN DEMO MODE - Sample Analysis")
    print("" * 35)
    
    analyzer = SkillGapAnalyzer()
    
    print("\n Sample: Beginner Data Scientist Aspirant")
    sample_skills = {
        "python": "beginner",
        "statistics": "beginner"
    }
    dream_job = "Data Scientist"
    
    analysis = analyzer.analyze_skills(sample_skills, dream_job)
    analyzer.display_analysis(analysis)
    
    print("\n" + "="*70)
    print(" KNOWLEDGE REPRESENTATION (CO3)")
    print("="*70)
    print("This expert system demonstrates CO3 through:")
    print("• Facts: Declarative knowledge representation")
    print("  - SkillFact(name='python', level='beginner')")
    print("  - JobGoalFact(title='Data Scientist')")
    print("  - MissingSkillFact(name='ML', importance='critical')")
    print("\n• Rules: Production rules for inference")
    print("  - IF skill_level < required_level THEN declare missing_skill")
    print("  - IF missing_skill THEN suggest_learning_resources")
    print("\n• Knowledge Base: Structured domain knowledge")
    print("  - Job requirements database (8+ careers)")
    print("  - Learning resources catalog (15+ resources)")
    print("  - Career progression paths")

if __name__ == "__main__":
    print("\n" + "" * 35)
    print("AI LAB MINI PROJECT - SKILL GAP & CAREER ADVISOR")
    print("Course Outcomes: CO3 (Knowledge Representation) & CO4 (Expert System)")
    print("" * 35)
    
    while True:
        print("\n MAIN MENU:")
        print("1. Interactive Mode (Enter your own skills)")
        print("2. Demo Mode (See sample analyses)")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1/2/3): ").strip()
        
        if choice == '1':
            app = CareerAdvisorApp()
            app.run()
        elif choice == '2':
            demo_mode()
        elif choice == '3':
            print("\n Thank you for using the Skill Gap Advisor!")
            break
        else:
            print(" Invalid choice. Please enter 1, 2, or 3.")
        
# commands:  .\skill_advisor_env\Scripts\activate
# python main.py
